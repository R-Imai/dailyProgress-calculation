# calc_timer
[TimeRecorder](https://github.com/R-Imai/TimeRecorder) のAPI部分

## 使い方

- run.batを起動する。もしくは
```
uvicorn fastapi_endpoint:app --reload --host {起動させるIPアドレス} --port ポート番号
```

### FastAPI

```
pip install fastapi
pip install uvicorn
pip install aiofiles
```

## 使えるAPI

- `{IPアドレス}:{ポート}/docs` でswaggerを表示
