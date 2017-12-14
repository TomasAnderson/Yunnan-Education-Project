import pandas as pd
import os
import re
# 1. specify configuration
schl = "njzx"
data_path = "../preprocess/type3/%s/" % schl
output_path = "../output/%s.csv" % schl
day_of_week = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期日"]

# 2. get schedule clean file
def get_njzx_header():
    header = "clrm,星期一-1,星期一-2,星期一-3,星期一-4,星期一-5,星期一-6,星期一-7,星期一-8,星期一-9,星期一-10,星期一-11,星期一-12,星期一-13,星期一-14,星期一-15,星期二-1,星期二-2,星期二-3,星期二-4,星期二-5,星期二-6,星期二-7,星期二-8,星期二-9,星期二-10,星期二-11,星期二-12,星期二-13,星期二-14,星期二-15,星期三-1,星期三-2,星期三-3,星期三-4,星期三-5,星期三-6,星期三-7,星期三-8,星期三-9,星期三-10,星期三-11,星期三-12,星期三-13,星期三-14,星期三-15,星期四-1,星期四-2,星期四-3,星期四-4,星期四-5,星期四-6,星期四-7,星期四-8,星期四-9,星期四-10,星期四-11,星期四-12,星期四-13,星期四-14,星期四-15,星期五-1,星期五-2,星期五-3,星期五-4,星期五-5,星期五-6,星期五-7,星期五-8,星期日-1,星期日-2\n"
    return header

def change_schedule_header():
    with open(data_path + "17-18_schedule_%s.csv"%(schl), 'r', encoding="utf-8") as input:
        with open(data_path + "schedule_clean.csv", 'w', encoding="utf-8") as output:
            lines = input.readlines()[4:]
            output.write(get_njzx_header())
            for line in lines:
                if ",,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,," not in line:
                    output.write(line)

# 3. get teacher clean file
def change_teacher_header():
    with open(data_path+"17-18_teacher_njzx.csv", 'r', encoding="utf-8") as input:
        with open(data_path + "temp_teacher.csv", 'w', encoding="utf-8") as output:
            lines = input.readlines()[1:]
            for line in lines:
                if ",,,,,,,,,,,,,,,,,," not in line:
                    output.write(line)
    df = pd.read_csv(data_path+"temp_teacher.csv", encoding="utf-8")
    df["grade"] = ["九年级"]*5+["八年级"]*5+["七年级"]*5
    df["clrm"] = df["班级"]
    df.to_csv(data_path+"teacher_clean.csv", encoding="utf-8")
    os.remove(data_path+"temp_teacher.csv")


# change_teacher_header()

# 4. output
weekday2index = {
    "星期一":[1,15],
    "星期二":[16,30],
    "星期三":[31,45],
    "星期四":[46,60],
    "星期五":[60,67],
    "星期日":[68,69]
}
schedule = ["0~0","0~0", #am reading
            "7:00~7:30", "8:00~8:45", "8:55~9:40", "10:00~10:45", "10:55~11:40",  # am
            "14:00~14:45", "15:00~15:45", "15:55~16:40",  # pm
            "0~0","0~0",#eve reading
            "19:00~20:00", "20:10~20:50", "21:00~21:40"]  # evening

def load_classroom():
    classroom_df = pd.read_csv(data_path+"classroom_%s_clean.csv"%schl)
    clrm = list(classroom_df["clrm"])
    class_n = list(classroom_df["class"])
    aio = list(classroom_df["aio"])
    grade = list(classroom_df["grade"])
    class2room, class2aio, class2grade = {}, {}, {}
    for i in range(0, len(clrm)):
        k, v1, v2, v3 = class_n[i], clrm[i], aio[i], grade[i]
        class2room[k] = v1
        class2aio[k] = v2
        class2grade[k] = v3
    return class2room, class2aio, class2grade

class2clrm, class2aio, class2grade = load_classroom()
headers = ",weekday,begintime,endtime,schl,class,teacher,subject,clrm,aio,grade\n"

teacher_df = pd.read_csv(data_path+"teacher_clean.csv")
def get_teacher(subject, class_n):
    query_result = teacher_df.loc[(teacher_df["clrm"] == class_n)]
    if subject in query_result:
        teacher = list(query_result[subject])[0]
        return teacher
    else:
        return "Not Found"


def output():
    # ,weekday,begintime,endtime,schl,class,teacher,subject,clrm,aio,grade
    with open(data_path + "schedule_clean.csv", 'r', encoding="utf-8") as input:
        with open(data_path + "%s.csv"%schl, 'w', encoding="utf-8") as output:
            output.write(headers)
            input.readline()
            index = 0
            for line in input:
                contents = line.strip().split(",")
                class_n = int(contents[0])
                grade = class2grade[int(class_n)]
                # grade, class_n = re.match(r"(.*)\((.*)\)", g_c).groups()
                for weekday in day_of_week:
                    start_i, end_i = weekday2index[weekday]
                    schedule_i = -1
                    for subject in contents[start_i:end_i+1]:
                        schedule_i = schedule_i + 1
                        if subject == "0":
                            continue
                        class_time = schedule[schedule_i].split("~")
                        if "0" == class_time[0]:
                            continue
                        teacher = get_teacher(subject, class_n)
                        if teacher == "Not Found" and class_time[0] >= "19:00" and class_time[0] < "7:00":
                            teacher = subject
                            subject = "晚自习"
                        index = index + 1
                        curr_line = "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (index, weekday, class_time[0], class_time[1], schl, class_n, teacher, subject, class2clrm[class_n], class2aio[class_n], grade)
                        output.write(curr_line)


output()



