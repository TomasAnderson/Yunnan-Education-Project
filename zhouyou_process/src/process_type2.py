import pandas as pd
import os
import re
# 1. specify configuration
schl = "dzzx"
data_path = "../preprocess/type2/%s/" % schl
output_path = "../output/%s.csv" % schl
day_of_week = ["星期一", "星期二", "星期三", "星期四", "星期五"]

# 2. change header
def get_dzzx_header():
    header = "clrm,星期一-1,星期一-2,星期一-3,星期一-4,星期一-5,星期一-6,星期一-7,星期一-8,星期一-9,星期一-10,星期二-1,星期二-2,星期二-3,星期二-4,星期二-5,星期二-6,星期二-7,星期二-8,星期二-9,星期二-10,星期三-1,星期三-2,星期三-3,星期三-4,星期三-5,星期三-6,星期三-7,星期三-8,星期三-9,星期三-10,星期四-1,星期四-2,星期四-3,星期四-4,星期四-5,星期四-6,星期四-7,星期四-8,星期四-9,星期四-10,星期五-1,星期五-2,星期五-3,星期五-4,星期五-5,星期五-6,星期五-7\n"
    return header

def change_hander():
    with open(data_path + "17-18_schedule_dzzx.csv", 'r', encoding="utf-8") as input:
        with open(data_path + "temp.csv", 'w', encoding="utf-8") as output:
            lines = input.readlines()[2:]
            output.write(get_dzzx_header())
            for line in lines:
                output.write(line)

# 3. handle each column
def split_subject_teacher(df):
    col = list(df)
    subjects = col[0:len(col):2]
    teachers = col[1:len(col)+1:2]
    st_col = []
    for i in range(0, len(subjects)):
        st_col.append("%s~%s"%(subjects[i], teachers[i]))
    return st_col

def generate_clean_schedule():
    df = pd.read_csv(data_path + "temp.csv", encoding="utf-8")
    headers = get_dzzx_header().strip().split(",")
    clean_df = pd.DataFrame()
    for header in headers:
        if header == "clrm":
            clrm_col = list(df["clrm"])
            clean_df[header] = clrm_col[0:len(clrm_col):2]

        else:
            subject_teacher_col = split_subject_teacher(df[header])
            clean_df[header] = subject_teacher_col
    clean_df.to_csv(data_path + "cleaned_schedule.csv", encoding="utf-8")
    os.remove(data_path + "temp.csv")

# change_hander()
# generate_clean_schedule()


# 4. output
weekday2index = {
    "星期一":[1,10],
    "星期二":[11,20],
    "星期三":[21,30],
    "星期四":[31,40],
    "星期五":[41,47],
}
schedule = ["7:00~7:30", "8:00~8:45", "8:55~9:40", "10:00~10:45", "10:55~11:40",  # am
            "14:00~14:45", "15:00~15:45", "15:55~16:40",  # pm
            "19:00~20:00", "20:10~20:50"]  # evening

def load_classroom():
    classroom_df = pd.read_csv(data_path+"classroom_%s_clean.csv"%schl)
    clrm = list(classroom_df["clrm"])
    class_n = list(classroom_df["class"])
    aio = list(classroom_df["aio"])
    class2room, class2aio, class2grade = {}, {}, {}
    for i in range(0, len(clrm)):
        k, v1, v2 = class_n[i], clrm[i], aio[i]
        class2room[k] = v1
        class2aio[k] = v2
    return class2room, class2aio

class2clrm, class2aio = load_classroom()
headers = ",weekday,begintime,endtime,schl,class,teacher,subject,clrm,aio,grade\n"

def output():
    # ,weekday,begintime,endtime,schl,class,teacher,subject,clrm,aio,grade
    with open(data_path + "cleaned_schedule.csv", 'r', encoding="utf-8") as input:
        with open(data_path + "output.csv", 'w', encoding="utf-8") as output:
            output.write(headers)
            input.readline()
            index = 0
            for line in input:
                contents = line.strip().split(",")[1:]
                g_c = contents[0]
                grade, class_n = re.match(r"(.*)\((.*)\)", g_c).groups()
                for weekday in day_of_week:
                    start_i, end_i = weekday2index[weekday]
                    schedule_i = -1
                    for st in contents[start_i:end_i+1]:
                        schedule_i = schedule_i + 1
                        if "0" in st:
                            continue
                        subject, teacher = st.split("~")
                        # TODO: clrm, aio here
                        class_time = schedule[schedule_i].split("~")
                        index = index + 1
                        curr_line = "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (index, weekday, class_time[0], class_time[1], schl, class_n, teacher, subject, class2clrm[class_n], class2aio[class_n], grade)
                        output.write(curr_line)


output()



