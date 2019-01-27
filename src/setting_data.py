from src import util

def write(val):
    util.write_path_record(val)

def get():
    return util.read_path_record()
