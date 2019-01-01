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

def calc_daily(path, day):
    data = util.read_json(util.RECORD_DIR + path)
    use_data = data[day]
    data = _summarize(use_data)
    return _mk_str(data)
