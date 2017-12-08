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


def get_mcyz_schedule():
    schedule = ["7:00~7:25","8:00~8:45","9:00~9:45","10:05~10:50","11:05~11:50", #am
                "14:00~14:45","15:05~15:50","16:00~16:50", #pm
                "19:00~20:00"] #evening
    return schedule



def add_schedule(input_path, output_path, schedule_df):
    files = listdir(input_path)
    files.remove(".DS_Store")
    for name in files:
        print("loading %s..."%name)
        df = pd.read_csv(input_path+name)
        df = df.drop(df.index[9])
        schedule_df = schedule_df + [""]*(len(df)-len(schedule_df))
        df["时间"] = schedule_df
        df.to_csv(output_path+name, encoding="utf-8")


def clean(input_path):
    files = listdir(input_path)
    files.remove(".DS_Store")

    for name in files:
        with open(input_path+name, "r", encoding="utf-8") as input:
            with open(raw_outpath+name, 'w', encoding="utf-8") as output:
                print("reading %s..."%(name))
                input.readline()
                input.readline()
                input.readline()
                for line in input:
                    if "午休" in line or "\"下" in line:
                        print("skip %s"%line)
                        continue
                    else:
                        output.write(line)



path = "../preprocess/type1/mcyz/"
input_path = path + "raw_classes/"
raw_outpath = path + "raw_out/"
outpath = path+"clean_classes/"

# clean(input_path)
add_schedule(raw_outpath, outpath, get_mcyz_schedule())

