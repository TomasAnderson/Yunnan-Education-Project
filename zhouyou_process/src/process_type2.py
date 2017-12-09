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
    header = "clrm,星期一-1,星期一-2,星期一-3,星期一-4,星期一-5,星期一-6,星期一-7,星期一-8,星期一-9,星期一-10,星期二-1,星期二-2,星期二-3,星期二-4,星期二-5,星期二-6,星期二-7,星期二-8,星期二-9,星期二-10,星期三-1,星期三-1,星期三-4,星期三-4,星期三-5,星期三-6,星期三-7,星期三-8,星期三-9,星期三-10,星期四-1,星期四-2,星期四-3,星期四-4,星期四-5,星期四-6,星期四-7,星期四-8,星期四-9,星期四-10,星期五-1,星期五-2,星期五-3,星期五-4,星期五-5,星期五-6,星期五-7\n"
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

# 4. output
weekday2index = {
    "星期一":[1,11],
    "星期二":[12,21],
    "星期三":[22,31],
    "星期四":[32,41],
    "星期五":[42,48],
}
def output():
    # ,weekday,begintime,endtime,schl,class,teacher,subject,clrm,aio,grade
    with open(data_path + "cleaned_schedule.csv", 'r', encoding="utf-8") as input:
        with open(data_path + "output.csv", 'w', encoding="utf-8") as output:
            input.readline()
            for line in input:
                contents = line.strip().split(",")[1:]
                g_c = contents[0]
                grade, class_n = re.match(r"(.*)\((.*)\)", g_c).groups()
                for weekday in day_of_week:
                    start_i, end_i = weekday2index[weekday]
                    for st in contents[start_i:end_i]:
                        if "0" in st:
                            continue
                        subject, teacher = st.split("~")
                        # TODO: add begintime, endtime, aio here
                        curr_line = ",%s,%s,%s,%s,%s,%s\n" % (weekday, schl, class_n, teacher, subject, grade)
                        output.write(curr_line)







