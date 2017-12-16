import pandas as pd
import os
import re
# 1. specify configuration
schl = "yjzx"
data_path = "../preprocess/type3/%s/" % schl
output_path = "../output/%s.csv" % schl
day_of_week = ["星期一", "星期二", "星期三", "星期四", "星期五"]

# 2. get schedule clean file
def get_njzx_header():
    # header = "clrm,星期一-1,星期一-2,星期一-3,星期一-4,星期一-5,星期一-6,星期一-7,星期一-8,星期一-9,星期一-10,星期一-11,星期一-12,星期一-13,星期一-14,星期一-15,星期二-1,星期二-2,星期二-3,星期二-4,星期二-5,星期二-6,星期二-7,星期二-8,星期二-9,星期二-10,星期二-11,星期二-12,星期二-13,星期二-14,星期二-15,星期三-1,星期三-2,星期三-3,星期三-4,星期三-5,星期三-6,星期三-7,星期三-8,星期三-9,星期三-10,星期三-11,星期三-12,星期三-13,星期三-14,星期三-15,星期四-1,星期四-2,星期四-3,星期四-4,星期四-5,星期四-6,星期四-7,星期四-8,星期四-9,星期四-10,星期四-11,星期四-12,星期四-13,星期四-14,星期四-15,星期五-1,星期五-2,星期五-3,星期五-4,星期五-5,星期五-6,星期五-7,星期五-8,星期日-1,星期日-2\n"
    header = "redundant,class,schedule,星期一,星期二,星期三,星期四,星期五\n"
    return header

def change_schedule_header():
    # change header and remove redundant lines
    with open(data_path + "17-18_teacher_%s.csv"%(schl), 'r', encoding="utf-8") as input:
        with open(data_path + "temp.csv", 'w', encoding="utf-8") as output:
            lines = input.readlines()
            output.write(get_njzx_header())
            prev = ""
            for line in lines[1:]:
                if "晚自习" in prev:
                    prev = line
                    continue
                if ",,,,,,,\n" not in line and "寅街中学" not in line and "课表执行时间" not in line and "星期" not in line and "课程" not in line and "13:00" not in line and "晚自习" not in line:
                    output.write(line)
                if "晚自习" in line:
                    prev = line
    # remove redundant characters
    df = pd.read_csv(data_path+"temp.csv", encoding="utf-8")
    df["class"] = [int(v/20)+33 for v in list(df.index)]
    df.drop(['redundant'], axis=1, inplace=True)

    n = len(df["schedule"])

    schl_col = list(df["schedule"])
    schl_col = schl_col[0:len(schl_col):2]
    df["schedule"] = schl_col + [""]*(n - len(schl_col))

    class_col = list(df["class"])
    class_col = class_col[0:len(class_col):2]
    df["class"] = class_col + [""]*(n - len(class_col))

    for weekday in day_of_week:
        weekday_col = list(df[weekday])
        subject_col = weekday_col[0:len(weekday_col)-1:2]
        teacher_col = weekday_col[1:len(weekday_col):2]
        weekday_col = ["%s~%s" %(subject_col[i], teacher_col[i]) for i in range(0, len(subject_col))]
        df[weekday] = weekday_col + [""]*(n-len(weekday_col))


    df.to_csv(data_path+"schedule_clean.csv", encoding="utf-8", index=False)
    os.remove(data_path+"temp.csv")


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



# change_schedule_header()
# exit()
# 4. output
# weekday2index = {
#     "星期一":[1,15],
#     "星期二":[16,30],
#     "星期三":[31,45],
#     "星期四":[46,60],
#     "星期五":[60,67],
#     "星期日":[68,69]
# }
# schedule = ["0~0","0~0", #am reading
#             "7:00~7:30", "8:00~8:45", "8:55~9:40", "10:00~10:45", "10:55~11:40",  # am
#             "14:00~14:45", "15:00~15:45", "15:55~16:40",  # pm
#             "0~0","0~0",#eve reading
#             "19:00~20:00", "20:10~20:50", "21:00~21:40"]  # evening

# schedule = ["07:00~07:30", "08:00~08:45", "08:55~09:40", "010:00~10:45", "10:55~11:40",  # am
#             "14:00~14:45", "15:00~15:45", "15:55~16:40"]
# weekday_cn = ['一','二','三','四','五']


def load_classroom():
    classroom_df = pd.read_csv(data_path+"classroom_%s_clean.csv"%schl)
    clrm = [s[-3:] for s in list(classroom_df["clrm"])]
    class_n = [s[:2] for s in list(classroom_df["class"])]
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

# teacher_df = pd.read_csv(data_path+"teacher_clean.csv")
# def get_teacher(subject, class_n):
#     query_result = teacher_df.loc[(teacher_df["班级"] == class_n)]
#     if subject in query_result:
#         teacher = list(query_result[subject])[0]
#         return teacher
#     else:
#         return "Not Found"


def output():
    # ,weekday,begintime,endtime,schl,class,teacher,subject,clrm,aio,grade
    with open(data_path + "schedule_clean.csv", 'r', encoding="utf-8") as input:
        with open(data_path + "%s.csv"%schl, 'w', encoding="utf-8") as output:
            output.write(headers)
            input.readline()
            index = 0
            for line in input:
                if "nan~nan,nan~nan,nan~nan" in line:
                    continue
                if ",,,,,," in line:
                    continue
                contents = line.strip().split(",")
                class_n = contents[0]
                grade = class2grade[str(class_n)] if class_n in class2grade else "No info"
                clrm = class2clrm[str(class_n)] if class_n in class2clrm else "No Info"
                aio = class2aio[str(class_n)] if class_n in class2aio else "No info"
                begintime, endtime = contents[1].split("-")
                for i in range(2, 7):
                    if "nan" in contents[i]:
                        index = index + 1
                        continue
                    subject, teacher = contents[i].split("~")
                    index = index + 1
                    output.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" % (
                    index,day_of_week[i-2], begintime, endtime, schl, class_n, teacher, subject,
                    clrm, aio, grade))

output()



