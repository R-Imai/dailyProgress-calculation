import sys
import json

def main():
    path = sys.argv[1]
    with open(path, "r", encoding="utf-8") as fp:
        color_dict = json.load(fp)
    new_dict_arr = []
    for i, key in enumerate(color_dict):
        new_elem = {
            "name": key,
            "color": color_dict[key],
            "sort_val": i,
            "is_active": True
        }
        new_dict_arr.append(new_elem)
    with open(sys.argv[2], 'w', encoding="utf-8") as fp:
        json.dump(new_dict_arr, fp, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    main()
