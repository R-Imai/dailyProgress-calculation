
from pydantic import BaseModel
from collections import OrderedDict

class ReturnResult(BaseModel):
    res: str = "OK"
    msg: str

class AppInfo(BaseModel):
    name: str = "dailyProgress-calculation"
    version: str
    description: str = "This is an api that measures and calculates daily work time."

class JobInfo(BaseModel):
    subject: str
    value: str

class JobStartInfo(BaseModel):
    subject: str
    value: str = ""
    startTime: str

class CurrentJobInfo(BaseModel):
    isDoing: bool
    jobInfo: JobStartInfo = None

class EditParam(BaseModel):
    val: OrderedDict
    day: str = None
    path: str = None

class RecordPath(BaseModel):
    path: str

class GraphPath(BaseModel):
    path: str
