from fastapi import FastAPI
import api_param as param
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
from starlette.staticfiles import StaticFiles

from src import calc_logic
from src import post_record
from src import setting_data
from src import util

app = FastAPI()
app.mount("/record", StaticFiles(directory="record"), name="record")

@app.get("/", response_model=param.AppInfo)
def root():
    info = param.AppInfo(version="2.1.0")
    info_jsonvalue = jsonable_encoder(info)
    return JSONResponse(content=info_jsonvalue)

@app.get("/calc/daily")
def calc_daily(path: str, date: str):
    ret_val = calc_logic.calc_daily(path, date)
    return ret_val

@app.post("/record/start")
def job_start(param: param.JobInfo):
    post_record.start(param.subject, param.value)
    return "ok"

@app.delete("/record/start")
def del_start():
    post_record.clear_start_record()


@app.get("/record/start", response_model=param.CurrentJobInfo)
def job_start():
    record = post_record.get_start()
    is_doing = not len(record) == 0
    jobInfo = None if not is_doing else param.JobStartInfo(subject=record["subject"], value=record["value"], startTime=record["start_time"])
    response = param.CurrentJobInfo(isDoing=is_doing, jobInfo=jobInfo)
    jsonvalue = jsonable_encoder(response)
    return JSONResponse(content=jsonvalue)


@app.post("/record/end", response_model=dict)
def job_end():
    ret_val = post_record.end()
    return ret_val

@app.get("/record/get", response_model=dict)
def record_get(day: str, path: str = None):
    ret_val = post_record.get_record(path, day)
    return ret_val

@app.post("/record/edit")
def record_edit(param: param.EditParam):
    post_record.edit(param.path, param.val, param.day)
    return "OK"

@app.get("/setting/path", response_model=param.RecordPath)
def path_record():
    path = setting_data.get()
    response = param.RecordPath(path=path)
    return response

@app.post("/setting/path")
def path_record(param: param.RecordPath):
    path = param.path
    setting_data.write(path)
    return "OK"


@app.get("/graph/save", response_model=param.GraphPath)
def graph_save(json_path: str = None, save_path: str = None):
    saved_path = calc_logic.plot(json_path, save_path=save_path)
    data = open(saved_path, 'rb')
    response = param.GraphPath(path=saved_path)
    jsonvalue = jsonable_encoder(response)
    return jsonvalue

@app.get("/setting/subject", response_model=dict)
def subject_config():
    subject_data = util.read_subject_file()
    return subject_data

@app.put("/setting/subject", response_model=dict)
def subject_config(data: dict):
    util.write_subject_file(data)
    return "OK"
