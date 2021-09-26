from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from typing import List
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse
from starlette.staticfiles import StaticFiles

import api_param as param
from src import calc_logic
from src import post_record
from src import setting_data
from src import util

app = FastAPI()
origins = [
    "http://127.0.0.1",
    "http://192.168.1.20"
    "http://192.168.1.18"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/storage", StaticFiles(directory="record"), name="storage")

@app.get("/", response_model=param.AppInfo)
def root():
    info = param.AppInfo(version="3.0.2")
    info_jsonvalue = jsonable_encoder(info)
    return JSONResponse(content=info_jsonvalue)

@app.get("/calc/daily")
def calc_daily(path: str, date: str):
    ret_val = calc_logic.calc_daily(path, date)
    return ret_val

@app.post("/record/start", response_model=param.ReturnResult)
def job_start(post_param: param.JobInfo):
    post_record.start(post_param.subject, post_param.value)
    return param.ReturnResult(msg=f"Job ${post_param.subject}/${post_param.value} is start.")

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

@app.post("/record/edit", response_model=param.ReturnResult)
def record_edit(post_param: param.EditParam):
    post_record.edit(post_param.path, post_param.val, post_param.day)
    return param.ReturnResult(msg="Edit record.")

@app.get("/setting/path", response_model=param.RecordPath)
def path_record():
    path = setting_data.get()
    response = param.RecordPath(path=path)
    return response

@app.post("/setting/path", response_model=param.ReturnResult)
def path_record(post_param: param.RecordPath):
    path = post_param.path
    setting_data.write(path)
    return param.ReturnResult(msg="Set save path.")


@app.get("/graph/save", response_model=param.GraphPath)
def graph_save(json_path: str = None, save_path: str = None):
    saved_path = calc_logic.plot(json_path, save_path=save_path)
    data = open(saved_path, 'rb')
    response = param.GraphPath(path=saved_path.replace("record/", "storage/", 1))
    jsonvalue = jsonable_encoder(response)
    return jsonvalue

@app.get("/setting/subject", response_model=List[param.SubjectData])
def subject_config():
    subject_data = util.read_subject_file()
    return subject_data

@app.put("/setting/subject", response_model=param.ReturnResult)
def subject_config(data: List[param.SubjectData]):
    sendData = [{"name": d.name, "color": d.color, "sort_val": d.sort_val, "is_active": d.is_active} for d in data]
    util.write_subject_file(sendData)
    return param.ReturnResult(msg="Set subject value.")
