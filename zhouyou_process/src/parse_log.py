import json

# s = """
# {"in": [], "out": [[3440, "userinit.exe"]], "time": "2017-11-12 20:06:43 Sun"}
#
# """
# print(json.loads(s))
# exit()


fname = "hyzx-1203-172.16.3.49-20171112.log".split("-")
schl = fname[0]
clrm = fname[1]
host = fname[2]
date = fname[3][:-4]

print(schl,clrm,host,date)
exit()




def get_pid2exe(a1, a2):
    pid2exe = {}
    for c in a1:
        pid2exe[c[0]] = c[1]
    for c in a2:
        pid2exe[c[0]] = c[1]
    return pid2exe

test_file = open("../../log/hyzx-1203-172.16.3.49-20171112.log")
for line in test_file:
    if line != "\n":
        try:
            d = json.loads(line)
            date = d['time']
            pid2exe = get_pid2exe(d['out'], d['in'])
            print(len(pid2exe))
        except json.JSONDecodeError:
            print("Exception occurs at line: %s"%line)



