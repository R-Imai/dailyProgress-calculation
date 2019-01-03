from flask import Flask, request
from src import calc_logic
from src import post_record
from src import setting_data
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route("/")
def root():
    return "This is calc time project"

@app.route("/calc/daily")
def calc_daily():
    path = request.args.get("path")
    date = request.args.get("day")
    ret_val = calc_logic.calc_daily(path, date)
    return ret_val

@app.route("/record/test", methods=['PUT'])
def test():
    post_record.test("test_data.json")
    return "OK"

@app.route("/record/start", methods=['POST', 'GET'])
def job_start():
    if request.method == "POST":
        if request.headers['Content-Type'] == 'application/json':
            val = request.json["val"]
            post_record.start(val)
            return "OK"
        else:
            return "application/jsonでPOSTしてください"
    elif request.method == "GET":
        return post_record.get_start()

@app.route("/record/end", methods=['POST'])
def job_end():
    if request.headers['Content-Type'] == 'application/json':
        path = request.json["path"]
        day = request.json["day"]
        subj = request.json["subj"]
        val = request.json["val"]
        ret_val = post_record.end(path, day, subj, val)
        return ret_val
    else:
        return "application/jsonでPOSTしてください"

@app.route("/record/get", methods=['GET'])
def record_get():
    path = request.args.get("path")
    day = request.args.get("day")
    ret_val = post_record.get_record(path, day)
    return ret_val

@app.route("/record/edit", methods=['POST'])
def record_edit():
    if request.headers['Content-Type'] == 'application/json':
        path = request.json["path"]
        val = request.json["val"]
        day = request.json["day"]
        post_record.edit(path, val, day)
        return "OK"
    else:
        return "application/jsonでPOSTしてください"

@app.route("/setting/path", methods=['POST', 'GET'])
def path_record():
    if request.method == "POST":
        if request.headers['Content-Type'] == 'application/json':
            path = request.json["path"]
            setting_data.write(path)
            return "OK"
        else:
            return "application/jsonでPOSTしてください"
    elif request.method == "GET":
        return setting_data.get()

if __name__ == "__main__":
    app.run(debug=True)
