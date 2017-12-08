from os import listdir
import pandas as pd
def remove_redundant_columns():
    for f in range(54, 67):
        with open("%d.csv"%f, "r") as input:
            with open("../%d.csv"%f, 'w') as output:
                for line in input:
                    if "休" in line:
                        continue
                    else:
                        output.write(line)

def get_hyzx_schedule():
    schedule = ["7:00~7:25","8:00~8:45","9:00~9:45","10:05~10:50","11:05~11:50",
                "14:00~14:45","15:05~15:50","16:00~16:50","17:00~17:45","19:00~19:45","19:55~20:50"]
    return schedule


def get_xjzx_schedule():
    schedule = ["7:00~7:25","8:00~8:45","9:00~9:45","10:05~10:50","11:05~11:50", #am
                "14:00~14:45","15:05~15:50","16:00~16:50", #pm
                "19:00~19:45", "20:00~20:45"] #evening
    return schedule

def get_mcyz_schedule():
    schedule = ["7:00~7:30","8:00~8:45","8:55~9:40","10:00~10:45","10:55~11:40", #am
                "14:00~14:45","15:00~15:45","15:55~16:40", #pm
                "19:00~20:00"] #evening
    return schedule


def get_files(path):
    names = listdir(path)
    if ".DS_Store" in names:
        names.remove(".DS_Store")
    return names

def add_schedule(input_path, output_path, schedule_df):
    files = get_files(input_path)
    for name in files:
        print("loading %s..."%name)
        df = pd.read_csv(input_path+name)
        df = format_teacher_subject(df)
        schedule_df = schedule_df + [""]*(len(df)-len(schedule_df))
        df["时间"] = schedule_df
        df.to_csv(output_path+name, encoding="utf-8", columns=day_of_week+["时间"])

def get_teachers_subjects(df):
    content = list(df)
    final_len = len(df)
    result = []
    result.append("自习(%s)" % content[0])
    subjects = content[1:14:2]
    teachers = content[2:15:2]
    for i in range(0, len(subjects)):
        result.append("%s(%s)" % (subjects[i], teachers[i]))
    result.append("晚自习1(%s)" % (content[-2]))
    result.append("晚自习2(%s)" % (content[-1]))
    result = result + [""] * (final_len - len(result))
    return result

def format_teacher_subject(df):
    for day in day_of_week:
        df[day] = get_teachers_subjects(df[day])
    df = df.drop(df.index[10:17])
    return df


def clean(input_path):
    files = get_files(input_path)
    for name in files:
        with open(input_path+name, "r", encoding="utf-8") as input:
            with open(raw_outpath+name, 'w', encoding="utf-8") as output:
                print("reading %s..."%(name))
                input.readline()
                input.readline()
                input.readline()
                for line in input:
                    # if "午休" in line or "\"下" in line:
                    if ",,,,,,," in line or "二零一七" in line: # handle xjzx
                        print("skip %s"%line)
                        continue
                    else:
                        output.write(line)


schl = "xjzx"
path = "../preprocess/type1/%s/"%schl
input_path = path + "raw_classes/"
raw_outpath = path + "raw_out/"
outpath = path+"clean_classes/"
day_of_week = ["星期一", "星期二", "星期三", "星期四", "星期五"]


# clean(input_path)
add_schedule(raw_outpath, outpath, get_xjzx_schedule())


