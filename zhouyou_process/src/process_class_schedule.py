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
def add_schedule(path):
    schedule_df = get_hyzx_schedule()
    files = listdir(path)
    for name in files:
        df = pd.read_csv(path+name)
        df["时间"]=schedule_df
        df.to_csv("../preprocess/type1/hyzx/out/%s"%name, encoding="utf-8")



add_schedule("../preprocess/type1/hyzx/classes/")

