# -*- coding: utf-8 -*-
import argparse
import json
import datetime
from datetime import datetime as dt
from collections import OrderedDict


def parse_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument(
            "-f", "--file",
            type = str,
            dest = "path",
            required = True,
            help = "The path of the time-recorded file"
    )

    parser.add_argument(
            "-d", "--day",
            type = str,
            dest = "day",
            required = True,
            help = "date"
    )

    # parser.add_argument(
    #         "-o", "--output",
    #         type = str,
    #         dest = "output",
    #         default = None,
    #         help = "output file path (default: console)"
    # )

    return parser.parse_args()

def mk_dict(pairs):
    ret_dict = OrderedDict()
    for elem in pairs:
        ret_dict[elem[0]] = ret_dict[elem[0]] + "," + elem[1] if elem[0] in ret_dict else elem[1]
    return ret_dict


def read_json(path):
    fp = open(path, "r", encoding="utf-8")
    json_dict = json.load(fp, object_pairs_hook=mk_dict)
    return json_dict

def calc_time(str_time):
    del_t = datetime.timedelta();
    str_time = str_time.split(",")
    for s_time in str_time:
        t_elem = s_time.split("-")
        del_t += dt.strptime(t_elem[1], "%H:%M") - dt.strptime(t_elem[0], "%H:%M")
    return del_t

def main():
    args = parse_arguments()
    data = read_json(args.path)
    use_data = data[args.day]
    for key in use_data:
        t = dt.strptime(str(calc_time(use_data[key])), "%H:%M:%S")
        msg = "- {0}: {1}h{2}m"
        if t.hour == 0:
            msg = "- {0}: {2}m"
        elif t.minute == 0:
            msg = "- {0}: {1}h"
        print(msg.format(key.replace("/", "=>"), t.hour, t.minute))








if __name__ == "__main__":
    main()
