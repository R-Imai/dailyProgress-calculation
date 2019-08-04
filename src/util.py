import json
from collections import OrderedDict

RECORD_DIR = "record/"
START_FILE = RECORD_DIR + "system/start_time.json"
PATH_RECORD_FILE = RECORD_DIR + "system/path_record.txt"
PATH_COLOR_FILE = RECORD_DIR + "system/color_config.json"
PATH_SUBJECT_FILE = RECORD_DIR + "system/subject_config.json"
FIGURE_DIR = RECORD_DIR + "fig/"

def _mk_dict(pairs):
    ret_dict = OrderedDict()
    for elem in pairs:
        ret_dict[elem[0]] = ret_dict[elem[0]] + "," + elem[1] if elem[0] in ret_dict else elem[1]
    return ret_dict

def read_start():
    val = {}
    with open(START_FILE, "r", encoding="utf-8") as fp:
        val = json.load(fp, object_pairs_hook=_mk_dict)
    return val

def write_start(val):
    with open(START_FILE, 'w', encoding="utf-8") as fp:
        json.dump(val, fp, ensure_ascii=False, indent=4)

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

def read_color_file():
    with open(PATH_SUBJECT_FILE, "r", encoding="utf-8") as fp:
        json_dict = json.load(fp)
    res = {}
    for key in json_dict:
        res[key] = json_dict[key]["color"]
    print(res)
    return res

def read_subject_file():
    with open(PATH_SUBJECT_FILE, "r", encoding="utf-8") as fp:
        json_dict = json.load(fp)
    return json_dict

def write_subject_file(val):
    with open(PATH_SUBJECT_FILE, "w", encoding="utf-8") as fp:
        json.dump(val, fp, ensure_ascii=False, indent=4)
