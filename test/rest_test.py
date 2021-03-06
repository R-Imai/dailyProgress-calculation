import requests
import json

val = requests.get('http://127.0.0.1:5000/calc/daily?path=sample_data.json&day=1')
print(val.text)

val = requests.put('http://127.0.0.1:5000/record/test')
print(val)

val = requests.post(
    'http://127.0.0.1:5000/record/start',
    json.dumps({"val":"テスト作業1: 19:00-"}),
    headers={'Content-Type': 'application/json'}
)
print(val)

val = requests.get('http://127.0.0.1:5000/record/start')
print(val.text)

val = requests.post(
    'http://127.0.0.1:5000/record/end',
    json.dumps({"path": "sample_data.json", "day": "7", "subj":  "Java学習/Java入門3", "val":"19:00-19:30"}),
    headers={'Content-Type': 'application/json'}
)
print(val.text)

val = requests.post(
    'http://127.0.0.1:5000/record/end',
    json.dumps({"path": "sample_data.json", "day": "6", "subj":  "Java学習/Java入門3", "val":"19:00-19:30"}),
    headers={'Content-Type': 'application/json'})
print(val.text)

val = requests.post(
    'http://127.0.0.1:5000/record/end',
    json.dumps({"path": "sample_data.json", "day": "1", "subj":  "Java学習/Java入門4", "val":"19:00-19:30"}),
    headers={'Content-Type': 'application/json'})
print(val.text)

val = requests.get('http://127.0.0.1:5000/setting/path')
print(val.text)

val = requests.get('http://127.0.0.1:5000/graph/save?json=sample_data.json&path=sample_data.png')
print(val.text)
