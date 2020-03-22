cd /d %~dp0
uvicorn fastapi_endpoint:app --reload --host 127.0.0.1 --port 5050
