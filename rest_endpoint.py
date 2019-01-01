from flask import Flask, request
from src import calc_logic
from src import post_record
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
        val = request.args.get("val")
        post_record.start(val)
        return "OK"
    elif request.method == "GET":
        return post_record.get()

@app.route("/record/end", methods=['POST'])
def job_end():
    path = request.args.get("path")
    day = request.args.get("day")
    subj = request.args.get("subj")
    val = request.args.get("val")
    ret_val = post_record.end(path, day, subj, val)
    return ret_val

if __name__ == "__main__":
    app.run(debug=True)
