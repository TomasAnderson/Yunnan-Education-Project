import pandas as pd
from dateutil import parser
week_day_dict={
    0: "星期一",1: "星期二",2: "星期三",3: "星期四",
    4: "星期五",5: "星期六",6: "星期日",
}

data_path = "../output/mzzx/result.csv"
data = pd.read_csv(data_path)

# sample query:
# we wang to know all information at 14:01 on 2017-11-8 at 1401 room in mzzx?

dt = parser.parse("2017-11-15 14:30")

time = "{:d}:{:02d}".format(dt.hour, dt.minute)
day_week = week_day_dict[dt.weekday()]
query_result = data.loc[(data["星期"] == day_week)
                  & (data["教室"] == 1401)
                  & (data["开始时间"] < time)
                  & (data["结束时间"] > time)]

print(query_result)
# output is the following:
    # Unnamed: 0   班号    教室   星期   开始时间   结束时间  科目   老师
# 23          23  129  1401  星期三  14:00  14:45  历史  李兆廷
