import json
import os
from datetime import datetime
from collections import OrderedDict

from src import util

def start(subject, value):
    start_time = datetime.now().strftime("%H:%M")
    val = {"subject": subject, "value": value, "start_time":start_time}
    util.write_start(val)

def clear_start_record():
    util.write_start({})

def get_start():
    return util.read_start()

def end():
    path = util.read_path_record()
    job_data = util.read_start()
    day = str(datetime.now().day)
    subj = [job_data["subject"], job_data["value"]]
    val = f"{job_data['start_time']}-{datetime.now().strftime('%H:%M')}"

    if os.path.exists(util.RECORD_DIR + path):
        data = util.read_json(util.RECORD_DIR + path)
    else:
        data = {}

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
    clear_start_record()
    return date_val

def get_record(path, day):
    if path is None:
        path = util.read_path_record()
    if os.path.exists(util.RECORD_DIR + path):
        data = util.read_json(util.RECORD_DIR + path)
    else:
        data = {}
    try:
        data = data[day]
    except KeyError:
        data = {}
    return data

def edit(path, val, day):
    print(val)
    if path is None:
        path = util.read_path_record()
    if day is None:
        day = str(datetime.now().day)

    json_data = util.read_json(util.RECORD_DIR + path)
    json_data[day] = val
    util.write_json(util.RECORD_DIR + path, json_data)

def test(path):
    path = util.RECORD_DIR + path
    data = util.read_json(path)
    data["31"] = {"test": "10:00-12:00"}
    util.write_json(path, data)
