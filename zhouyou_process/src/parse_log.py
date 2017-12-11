import json
from os import listdir
from dateutil import parser
import pandas as pd

def parse_log_fname(s):
    fname = s.split("-")
    schl = fname[0]
    clrm = fname[1]
    host = fname[2]
    date = fname[3][:-4]
    return schl, clrm, host, date

def get_pid2exe(a1, a2):
    pid2exe = {}
    for c in a1:
        pid2exe[c[0]] = c[1]
    for c in a2:
        pid2exe[c[0]] = c[1]
    return pid2exe

day_of_week = ["星期一", "星期二", "星期三", "星期四", "星期五"]

def parse_dtime(dtime):
    # dtime = "2017-11-08 15:36:30 Wed"
    dt = parser.parse(dtime)
    weekday = day_of_week[dt.weekday()]
    time = "{:d}:{:02d}".format(dt.hour, dt.minute)
    return weekday, time

def parse_log_content(fname):
    test_file = open(fname)
    error_lines = []
    for line in test_file:
        if line != "\n":
            try:
                d = json.loads(line)
                weekday, time = parse_dtime(d['time'])
                pid2exe = get_pid2exe(d['out'], d['in'])
            except json.JSONDecodeError:
                error_lines.append([fname, line])
    return weekday, time, pid2exe, error_lines

def print_error_lines(error_lines):
    for item in error_lines:
        print("In file %s, the error line is \n%s\n" % (item[0], item[1]))

def load_school_df(schl):
    return pd.read_csv("../output/%s.csv"%schl, encoding="utf-8")

def get_schl_dfs():
    schl = ["dzzx", "hyzx", "mcyz", "mzzx", "xjzx"]
    schl2df = {}
    for s in schl:
        schl2df[s] = load_school_df(s)
    return schl2df

def query(schl, clrm, time, weekday):
    if schl not in schl2df:
        print("Invalid schl name %s\n"%(schl))
        return None

    df = schl2df[schl]
    query_result = df.loc[(df["weekday"] == weekday)
                            & (df["clrm"] == int(clrm))
                            & (df["begintime"] < time)
                            & (df["endtime"] > time)]

    begintime = list(query_result["begintime"])[0]
    endtime = list(query_result["endtime"])[0]
    class_n= list(query_result["class"])[0]
    teacher= list(query_result["teacher"])[0]
    subject= list(query_result["subject"])[0]
    aio= list(query_result["aio"])[0]
    grade= list(query_result["grade"])[0]
    return begintime,endtime,class_n,teacher,subject,aio,grade





data_path = "../../log/"
schl2df = get_schl_dfs()
# result = query("hyzx", "1106", "12:00", "星期三")
# print(result)
# exit()

def parse_log(data_path):
    """
    pid, exe, date, weekday, begintime, endtime, schl, class teacher, subject clrm, aio, grade
    :param data_path:
    :return:
    """
    fnames = listdir(data_path)
    with open("../output/output.csv", 'w', encoding="utf-8") as output:
        output.write("pid, exe, date, weekday, begintime, endtime, schl, class, teacher, subject, clrm, aio, grade\n")
        for name in fnames:
            if ".log" in name:
                try:
                    schl, clrm, host, date = parse_log_fname(name)
                    weekday, time, pid2exe, error_lines = parse_log_content(data_path + name)
                    begintime, endtime, class_n, teacher, subject, aio, grade = query(schl, clrm, time, weekday)
                    for pid in pid2exe:
                        output.write("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n"%(pid, pid2exe[pid], date, weekday, begintime, endtime, schl, class_n, subject, clrm, aio, grade))
                    if error_lines != []:
                        print_error_lines(error_lines)
                except IndexError:
                    print("IndexError: %s" % name)
                except UnboundLocalError:
                    print("UnboundLocalError: %s" % name)
                except json.JSONDecodeError as e:
                    print("JSONDecodeError in file %s, error is %s" % (name, e))
                except TypeError as e:
                    print("TypeError %s"%e)


parse_log(data_path)

