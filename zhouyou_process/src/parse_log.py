import json
from os import listdir


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


def parse_log_content(fname):
    test_file = open(fname)
    error_lines = []
    for line in test_file:
        if line != "\n":
            try:
                d = json.loads(line)
                date = d['time']
                pid2exe = get_pid2exe(d['out'], d['in'])
            except json.JSONDecodeError:
                error_lines.append([fname, line])
    return date, pid2exe, error_lines

def print_error_lines(error_lines):
    for item in error_lines:
        print("In file %s, the error line is \n%s\n" % (item[0], item[1]))

data_path = "../../log/"
def parse_log(data_path):
    fnames = listdir(data_path)
    for name in fnames:
        if ".log" in name:
            try:
                schl, clrm, host, date = parse_log_fname(name)
                date, pid2exe, error_lines = parse_log_content(data_path + name)
                if error_lines != []:
                    print_error_lines(error_lines)
            except IndexError:
                print("Error: %s" % name)
            except UnboundLocalError:
                print("Error: %s" % name)
            except json.JSONDecodeError as e:
                print("Error in file %s, error is %s" % (name, e))


parse_log(data_path)

