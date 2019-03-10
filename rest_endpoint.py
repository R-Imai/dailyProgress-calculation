from flask import Flask, request, jsonify
from src import calc_logic
from src import post_record
from src import setting_data
from src import util
from flask_cors import CORS

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)


@app.route("/")
def root():
    result = {
        "version": "2.1.0",
        "description": "This is calc time project. "
    }
    return jsonify(result)

@app.route("/calc/daily")
def calc_daily():
    path = request.args.get("path")
    date = request.args.get("day")
    ret_val = calc_logic.calc_daily(path, date)
    return ret_val

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
        return jsonify(ret_val)
    else:
        return "application/jsonでPOSTしてください"

@app.route("/record/get", methods=['GET'])
def record_get():
    path = request.args.get("path")
    day = request.args.get("day")
    ret_val = post_record.get_record(path, day)
    return jsonify(ret_val)

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

@app.route("/graph/show", methods=['GET'])
def graph_show():
    path = request.args.get("json")
    calc_logic.plot(path)
    return "OK"

@app.route("/graph/save", methods=['GET'])
def graph_save():
    json_path = request.args.get("json")
    save_path = request.args.get("path")
    ret_value = calc_logic.plot(json_path, save_path=save_path)
    return ret_value + "へ画像を保存しました。"

@app.route("/graph/color", methods=['GET', 'PUT'])
def color_config():
    if request.method == "GET":
        color_data = util.read_color_file()
        return jsonify(color_data)
    elif request.method == "PUT":
        if request.headers['Content-Type'] == 'application/json':
            data = request.json["color_data"]
            util.write_color_file(data)
            return "OK"

if __name__ == "__main__":
    app.run(debug=True)
