cd /d %~dp0
REM set FLASK_APP=rest_endpoint.py
REM flask run
uvicorn fastapi_endpoint:app --reload
