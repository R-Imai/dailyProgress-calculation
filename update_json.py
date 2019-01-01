from src import util
from collections import OrderedDict




def main():
    data = util.read_json("record/test_data.json")
    new_dict = OrderedDict()
    for key in data:
        days_dict = OrderedDict()
        for subj in data[key]:

            new_subj = subj.split("/", 1)
            if len(new_subj) == 1:
                new_subj.append("")
            if new_subj[0] in days_dict:
                days_dict[new_subj[0]][new_subj[1]] = data[key][subj].split(",")
            else:
                elem_dict = OrderedDict()
                elem_dict[new_subj[1]] = data[key][subj].split(",")
                days_dict[new_subj[0]] = elem_dict
        new_dict[key] = days_dict
    print(new_dict)
    util.write_json("record/sample_data.json", new_dict)

if __name__ == '__main__':
    main()
