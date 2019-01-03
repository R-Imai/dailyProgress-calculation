import json
import os
from collections import OrderedDict

from src import util

def start(val):
    util.write_start(val)

def get_start():
    return util.read_start()

def end(path, day, subj, val):
    if os.path.exists(util.RECORD_DIR + path):
        data = util.read_json(util.RECORD_DIR + path)
    else:
        data = {}
    subj = subj.split("/", 1)
    if len(subj) == 1:
        subj.append("")

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
    return json.dumps({day: date_val}, ensure_ascii=False, indent=4)[6:-2].replace("\n    ", "\n")

def get_record(path, day):
    if os.path.exists(util.RECORD_DIR + path):
        data = util.read_json(util.RECORD_DIR + path)
    else:
        data = {}
    try:
        data = data[day]
        data = json.dumps({day: data}, ensure_ascii=False, indent=4)[6:-2].replace("\n    ", "\n")
    except KeyError:
        data = "\"{0}\":{{\n}}".format(day)
    return data

def edit(path, val, day):
    val = json.loads(val)
    val = val[day]
    json_data = util.read_json(util.RECORD_DIR + path)
    json_data[day] = val
    util.write_json(util.RECORD_DIR + path, json_data)

def test(path):
    path = util.RECORD_DIR + path
    data = util.read_json(path)
    data["31"] = {"test": "10:00-12:00"}
    util.write_json(path, data)
