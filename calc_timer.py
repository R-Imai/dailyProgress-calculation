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
            help = "The path of the time-recorded file (*.json)"
    )

    parser.add_argument(
            "-d", "--day",
            type = str,
            dest = "day",
            default =None,
            help = "Select date to calculate"
    )

    parser.add_argument(
            "-p", "--plot",
            type = bool,
            dest = "plot",
            default = False,
            const = True,
            nargs="?",
            help = "Display all data as a pie chart"
    )

    parser.add_argument(
            "-n", "--newplot",
            type = bool,
            dest = "new_plot",
            default = False,
            const = True,
            nargs="?",
            help = "Display new format json file all data as a pie chart"
    )

    return parser


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

def new_format_calc_time(str_time):
    del_t = datetime.timedelta();
    for s_time in str_time:
        t_elem = s_time.split("-")
        del_t += dt.strptime(t_elem[1], "%H:%M") - dt.strptime(t_elem[0], "%H:%M")
    return del_t

def summarize(use_data):
    data = OrderedDict()
    for key in use_data:
        t_del = calc_time(use_data[key])
        minute = t_del.seconds//(60)
        t = datetime.time(hour=minute//60, minute=minute%(60))
        work_name = key.split("/", 1)
        if work_name[0] in data:
            data[work_name[0]].append([work_name[1], t])
        else:
            if len(work_name) == 1:
                data[work_name[0]] = t
            else:
                data[work_name[0]] = [[work_name[1], t]]
    return data

def output(data):
    for key in data:
        if type(data[key]) == list:
            print("* {0}".format(key))
            for elem in data[key]:
                msg = "    ** {0}: {1}h{2}m"
                if elem[1].hour == 0:
                        msg = "    ** {0}: {2}m"
                elif elem[1].minute == 0:
                    msg = "    ** {0}: {1}h"
                print(msg.format(elem[0], elem[1].hour, elem[1].minute))
        else:
            msg = "* {0}: {1}h{2}m"
            if data[key].hour == 0:
                msg = "* {0}: {2}m"
            elif data[key].minute == 0:
                msg = "* {0}: {1}h"
            print(msg.format(key, data[key].hour, data[key].minute))

def aggregate(all_data):
    ret_data = {}
    for day in all_data:
        data_elem = all_data[day]
        for subj_key in data_elem:
            subj = subj_key.split("/")[0]
            t = calc_time(data_elem[subj_key])
            ret_data[subj] = ret_data[subj] + t if subj in ret_data else t
    return ret_data


def hex2color(hex_c):
    return [int(hex_c[1:3],16)/256.0,int(hex_c[3:5],16)/256.0,int(hex_c[5:7],16)/256.0,1]


def plot(all_data):
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.cm as cm

    my_color = read_json("./color_config.json")

    label = []
    data = []
    col = cm.gist_rainbow(np.arange(len(all_data))/float(len(all_data)))

    for i, elem in enumerate(sorted(all_data.items(), key=lambda x: -x[1])):
        key = elem[0]
        val = elem[1]
        h = int(all_data[key].total_seconds()//(60*60))
        m = int(all_data[key].total_seconds()/60 - h*60)
        str_t = "{0}h{1}m".format(h, m)
        label.append("{0} [{1}]".format(key, str_t))
        data.append(val.total_seconds()/60)
        if key in my_color:
            col[i] = hex2color(my_color[key])

    plt.rcParams['font.family'] = 'Yu Mincho'
    plt.figure(figsize=(9,5))
    plt.pie(data,counterclock=False,startangle=90,autopct=lambda p:'{:.1f}%'.format(p), colors=col)
    plt.subplots_adjust(left=0,right=0.7)
    plt.legend(label, fancybox=True, loc='upper left', bbox_to_anchor=(0.83, 1))
    plt.axis('equal')
    plt.show()

def new_plot(all_data):
    ret_data = {}
    for day in all_data:
        data_elem = all_data[day]
        for subj in data_elem:
            for subj_key in data_elem[subj]:
                t = new_format_calc_time(data_elem[subj][subj_key])
                ret_data[subj] = ret_data[subj] + t if subj in ret_data else t
    return ret_data

def main():
    parser = parse_arguments()
    args = parser.parse_args()
    data = read_json(args.path)

    if args.plot:
        data = aggregate(data)
        plot(data)

    elif args.new_plot:
        data = new_plot(data)
        plot(data)

    elif args.day is not None:
        use_data = data[args.day]
        data = summarize(use_data)
        output(data)

    else:
        parser.print_help()





if __name__ == "__main__":
    main()
