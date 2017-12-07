import pandas as pd
import numpy as np
import re

def load_classroom():
    """
    load class to room mapping, return a dict obj
    :return:
    """
    classroom_df = pd.read_csv(data_path+"classroom_%s_clean.csv"%schl)
    clrm = list(classroom_df["clrm"])
    class_n = list(classroom_df["class"])
    grade = list(classroom_df["grade"])
    aio = list(classroom_df["aio"])
    class2room, class2aio, class2grade = {}, {}, {}
    for i in range(0, len(clrm)):
        k, v1, v2, v3 = class_n[i], clrm[i], aio[i], grade[i]
        class2room[k] = v1
        class2aio[k] = v2
        class2grade[k] = v3
    return class2room, class2aio, class2grade


def split_class_teacher(df):
    """
    split class and teacher infomation

    :param df: schedule column, looks like "语文\r(吴昌梅)" or "思想品德教育"
    :return: a class_type dateframe and teacher dataframe
    """
    class_arr, teacher_arr = [], []
    for elm in df:
        elm = re.sub("(\r|\n)", "", str(elm))
        # print("before splitting is %s\n" % elm)
        if "(" not in elm and "（" not in elm:
            class_arr.append(elm)
            teacher_arr.append("")
        else:
            try:
                class_type, teacher = re.match(r"(.*)\((.*)\)", elm).groups()
            except AttributeError:
                print(elm)
            # print("after splitting is %s, %s\n" % (class_type, teacher))
            class_arr.append(class_type)
            teacher_arr.append(teacher)
    return pd.DataFrame(class_arr, columns=["subject"]), pd.DataFrame(teacher_arr, columns=["teacher"])

def get_time_df(df):
    """
    split time span into starting time nad end time data frame
    """
    start_arr, end_arr = [], []
    for time in df:
        start, end = str(time).split("~")
        start_arr.append(start)
        end_arr.append(end)
    return pd.DataFrame(start_arr, columns=["begintime"]), pd.DataFrame(end_arr, columns=["endtime"])


def create_column(content, n, column):
    return pd.DataFrame(np.repeat(content,n), columns=[column])

def load_class_schedule(class_n):
    """
    give a class number, read its schedule and generate a combined & comprehensive output
    :param class_no: class number, correspond to a class schduel csv file
    :return: a combined dataframe contains [weekday, begintime, endtime, schl, class, teacher, subject, clrm, aio, grade]
    """
    try:
        sched_df = pd.read_csv(data_path+str(class_n)+".csv")
    except FileNotFoundError:
        return None
    begintime_df, endtime_df = get_time_df(sched_df["时间"])
    n = len(begintime_df)

    class_df = create_column(class_n, n, "class")
    aio_df = create_column(class2aio[class_n], n, "aio")
    clrm_df = create_column(class2room[class_n], n, "clrm")
    grade_df = create_column(class2grade[class_n], n, "grade")
    schl_df = create_column(schl, n, "schl")


    schedule_df = pd.DataFrame()
    for day in day_of_week:
        weekday_df = create_column(day, n, "weekday")
        subject_df, teacher_df = split_class_teacher(sched_df[day])
        result = pd.concat([weekday_df, begintime_df, endtime_df, schl_df, class_df, teacher_df, subject_df, clrm_df, aio_df, grade_df], axis=1)
        schedule_df = schedule_df.append(result, ignore_index=True)
    return schedule_df


# 1. specify configuration
schl = "hyzx"
data_path = "../preprocess/type1/%s/" % schl
output_path = "../output/%s.csv" % schl
day_of_week = ["星期一", "星期二", "星期三", "星期四", "星期五"]

# 2. read schedule for each class, and merge them together
class2room, class2aio, class2grade = load_classroom()
result_df = pd.DataFrame()
for class_n in class2room.keys():
    print("loading class %s..." % class_n)
    schedule_df = load_class_schedule(class_n)
    result_df = result_df.append(schedule_df, ignore_index=True)

# 3. write to file
result_df.to_csv(output_path, encoding='utf-8')
