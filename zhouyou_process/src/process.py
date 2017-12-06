import pandas as pd
import numpy as np
import re

def load_class2room():
    """
    load class to room mapping, return a dict obj
    :return:
    """
    class_room_df = pd.read_csv(data_path+"classroom_mzzx_clean.csv")
    room_no, class_no = list(class_room_df["Room No."]), list(class_room_df["Class No."])
    class2room = {}
    for i in range(0, len(room_no)):
        k, v = class_no[i], room_no[i]
        class2room[k] = v
    return class2room


def split_class_teacher(df):
    """
    split class and teacher infomation

    :param df: schedule column, looks like "语文\r(吴昌梅)" or "思想品德教育"
    :return: a class_type dateframe and teacher dataframe
    """
    class_arr, teacher_arr = [], []
    for elm in df:
        elm = str(elm).replace("\r", "")
        if "(" not in elm and "（" not in elm:
            class_arr.append(elm)
            teacher_arr.append("")
        else:
            class_type, teacher = re.match(r"(.*)\((.*)\)", elm).groups()
            class_arr.append(class_type)
            teacher_arr.append(teacher)
    return pd.DataFrame(class_arr, columns=["科目"]), pd.DataFrame(teacher_arr, columns=["老师"])

def get_time_df(df):
    """
    split time span into starting time nad end time data frame
    """
    start_arr, end_arr = [], []
    for time in df:
        start, end = str(time).split("~")
        start_arr.append(start)
        end_arr.append(end)
    return pd.DataFrame(start_arr, columns=["开始时间"]), pd.DataFrame(end_arr, columns=["结束时间"])


def load_class_schedule(class_no):
    """
    give a class number, read its schedule and generate a combined & comprehensive output
    :param class_no: class number, correspond to a class schduel csv file
    :return: a combined dataframe contains [班号，教室，星期，时间，科目，老师]
    """
    sched_df = pd.read_csv(data_path+str(class_no)+".csv")
    class_room = class2room[class_no]
    start_time_df, end_time_df = get_time_df(sched_df["时间"])
    num_of_row = len(start_time_df)
    class_df = pd.DataFrame(np.repeat(class_no, num_of_row), columns=["班号"])
    class_room_df = pd.DataFrame(np.repeat(class_room, num_of_row), columns=["教室"])

    class_schedule_df = pd.DataFrame()
    for day in dat_of_week:
        day_of_week_df = pd.DataFrame(np.repeat(day, num_of_row), columns=["星期"])
        c_df, t_df = split_class_teacher(sched_df[day])
        result = pd.concat([class_df, class_room_df, day_of_week_df, start_time_df, end_time_df, c_df, t_df], axis=1)
        class_schedule_df = class_schedule_df.append(result, ignore_index=True)
    return class_schedule_df


# 1. specify configuration
data_path = "../preprocess/mzzx/"
output_path = "../output/mzzx/"
dat_of_week = ["星期一", "星期二", "星期三", "星期四", "星期五"]
class_no_start = 129
class_no_end = 140

# 2. read schedule for each class, and merge them together
class2room = load_class2room()
result_df = pd.DataFrame()
for class_no in range(class_no_start, class_no_end+1):
    schedule_df = load_class_schedule(class_no)
    result_df = result_df.append(schedule_df, ignore_index=True)

# 3. write to file
result_df.to_csv(output_path+"result.csv", encoding='utf-8')
