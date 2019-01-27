import json
from collections import OrderedDict

RECORD_DIR = "record/"
START_FILE = RECORD_DIR + "system/start_time.txt"
PATH_RECORD_FILE = RECORD_DIR + "system/path_record.txt"
FIGURE_DIR = RECORD_DIR + "fig/"

def _mk_dict(pairs):
    ret_dict = OrderedDict()
    for elem in pairs:
        ret_dict[elem[0]] = ret_dict[elem[0]] + "," + elem[1] if elem[0] in ret_dict else elem[1]
    return ret_dict

def read_start():
    val = ""
    with open(START_FILE, 'r', encoding="utf-8") as fp:
        val = fp.read()
    return val

def write_start(val):
    with open(START_FILE, 'w', encoding="utf-8") as fp:
        fp.write(val)

def read_json(path):
    with open(path, "r", encoding="utf-8") as fp:
        json_dict = json.load(fp, object_pairs_hook=_mk_dict)
    return json_dict

def write_json(path, data):
    with open(path, 'w', encoding="utf-8") as fp:
        json.dump(data, fp, ensure_ascii=False, indent=4)

def read_path_record():
    val = ""
    with open(PATH_RECORD_FILE, 'r', encoding="utf-8") as fp:
        val = fp.read()
    return val

def write_path_record(val):
    with open(PATH_RECORD_FILE, 'w', encoding="utf-8") as fp:
        fp.write(val)
