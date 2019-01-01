import json
from src import util
from collections import OrderedDict

def start(val):
    util.write_start(val)

def get():
    return util.read_start()

def end(path, day, subj, val):
    data = util.read_json(util.RECORD_DIR + path)
    subj = subj.split("/", 1)

    if day in data:
        date_val = data[day]
        if subj[0] in date_val:
            if subj[1] in date_val[subj[0]]:
                date_val[subj[0]][subj[1]].append(val)
            else:
                date_val[subj[0]][subj[1]] = [val]
        else:
            date_val[subj[0]] = {subj[1]: [val]}
    else:
        date_val = {subj[0]: {subj[1]: [val]}}
    data[day] = date_val

    util.write_json(util.RECORD_DIR + path, data)
    util.write_start("")
    return json.dumps({day: date_val}, ensure_ascii=False, indent=4)



def test(path):
    path = util.RECORD_DIR + path
    data = util.read_json(path)
    data["31"] = {"test": "10:00-12:00"}
    util.write_json(path, data)
