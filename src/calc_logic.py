import datetime
from datetime import datetime as dt
from collections import OrderedDict

from src import util

def _calc_time(str_time):
    del_t = datetime.timedelta();
    for s_time in str_time:
        t_elem = s_time.split("-")
        del_t += dt.strptime(t_elem[1], "%H:%M") - dt.strptime(t_elem[0], "%H:%M")
    return del_t


def _summarize(use_data):
    data = OrderedDict()
    for key in use_data:
        for subj in use_data[key]:
            t_del = _calc_time(use_data[key][subj])
            minute = t_del.seconds//(60)
            t = datetime.time(hour=minute//60, minute=minute%(60))
            work_name = [key, subj]
            if work_name[0] in data:
                data[work_name[0]].append([work_name[1], t])
            else:
                if len(work_name) == 1:
                    data[work_name[0]] = t
                else:
                    data[work_name[0]] = [[work_name[1], t]]
    return data

def _mk_str(data):
    ret_val = ""
    for key in data:
        ret_val_elem = "* {0}{1}\n".format(key, "{0}")
        for elem in data[key]:
            if elem[0] != "":
                msg = "\t** {0}: {1}h{2}m\n"
                if elem[1].hour == 0:
                        msg = "\t** {0}: {2}m\n"
                elif elem[1].minute == 0:
                    msg = "\t** {0}: {1}h\n"
                ret_val_elem += msg.format(elem[0], elem[1].hour, elem[1].minute)
            else:
                msg = ": {0}h{1}m"
                if elem[1].hour == 0:
                    msg = ": {1}m"
                elif elem[1].minute == 0:
                    msg = ": {0}h"
                ret_val_elem = ret_val_elem.format(msg.format(elem[1].hour, elem[1].minute))
        ret_val += ret_val_elem.format("")
    return ret_val

def _hex2color(hex_c):
    return [int(hex_c[1:3],16)/256.0,int(hex_c[3:5],16)/256.0,int(hex_c[5:7],16)/256.0,1]

def _plot_data(all_data, save_path=None):
    import numpy as np
    import matplotlib.pyplot as plt
    import matplotlib.cm as cm

    my_color = util.read_color_file()

    label = []
    data = []
    col = [None for i in range(len(all_data))]

    for i, elem in enumerate(sorted(all_data.items(), key=lambda x: -x[1])):
        key = elem[0]
        val = elem[1]
        h = int(all_data[key].total_seconds()//(60*60))
        m = int(all_data[key].total_seconds()/60 - h*60)
        str_t = "{0}h{1}m".format(h, m)
        label.append("{0} [{1}]".format(key, str_t))
        data.append(val.total_seconds()/60)
        if key in my_color:
            col[i] = _hex2color(my_color[key])

    no_color_lange = col.count(None)
    cmap = cm.gist_rainbow(np.arange(no_color_lange)/float(no_color_lange))

    cnt = 0
    for i, elem in enumerate(col):
        if elem is None:
            col[i] = cmap[cnt]
            cnt += 1

    plt.rcParams['font.family'] = 'Yu Mincho'
    plt.figure(figsize=(18, 10))
    plt.pie(data,counterclock=False,startangle=90,autopct=lambda p:'{:.1f}%'.format(p), colors=col)
    plt.subplots_adjust(left=0,right=0.7)
    plt.legend(label, fancybox=True, loc='upper left', bbox_to_anchor=(0.83, 1))
    plt.axis('equal')
    if save_path is None:
        plt.show()
    else:
        plt.savefig(save_path)
    plt.clf()

def _aggregate(all_data):
    ret_data = {}
    for day in all_data:
        data_elem = all_data[day]
        for subj in data_elem:
            for subj_key in data_elem[subj]:
                t = _calc_time(data_elem[subj][subj_key])
                ret_data[subj] = ret_data[subj] + t if subj in ret_data else t
    return ret_data

def calc_daily(path, day):
    data = util.read_json(util.RECORD_DIR + path)
    use_data = data[day]
    data = _summarize(use_data)
    return _mk_str(data)

def plot(json_path, save_path=None):
    data = util.read_json(util.RECORD_DIR + json_path)
    data = _aggregate(data)
    save_path = None if save_path is None else util.FIGURE_DIR + save_path
    _plot_data(data, save_path)
    return save_path
