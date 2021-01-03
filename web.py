from flask import Flask
from flask import Response
from flask import send_from_directory, stream_with_context
from flask import jsonify
import csv
from io import StringIO
import datetime
from datetime import timedelta
import dateutil.parser

app = Flask(__name__, static_url_path="/static")

def last24(): 
    earliest = datetime.datetime.now() - timedelta(hours=24)
    rows = []
    with open("./all.csv", "r") as f:
        r = csv.reader(f)
    # only return values from within the last 24 hours
        for i, row in enumerate(r):
            if i == 0:
                continue
            dateVal = row[0]
            if dateutil.parser.isoparse(dateVal) > earliest:
                rows.append(row)
    return rows

@app.route('/data')
def send_data():
    return send_from_directory('.', "all.csv")

@app.route('/all.csv')
def send_csv():
    def generate():
        with open("./all.csv", "r") as f:
            data = StringIO() 

            # only return values from within the last 24 hours
            earliest = datetime.datetime.now() - timedelta(hours=24)

            r = csv.reader(f, delimiter="\t")
            for i, row in enumerate(r):
                if i == 0:
                    data.write("".join(row) + "\n")
                    yield data.getvalue()
                    data.seek(0)
                    data.truncate(0)
                else:
                    dateVal = row[0].split(",")[0]
                    if dateutil.parser.isoparse(dateVal) > earliest:
                        data.write("".join(row) + "\n")
                        yield data.getvalue()
                        data.seek(0)
                        data.truncate(0)
    return Response(generate(), mimetype='text/csv')

@app.route('/')
@app.route('/chart')
def send_chart():
    return send_from_directory('.', "chart.html")

@app.route('/summary')
def summary():
    d = last24()
    s = sum([float(x[3]) for x in d])
    if len(d) > 0:
        return jsonify(
                {
                    'AQI_2.5_24': round(s / len(d)),
                    'AQI_2.5_Now': d[-1][3],
                    'Updated': d[-1][0]},
                )
    return jsonify(
            {
                'AQI_2.5_24': -1,
                'AQI_2.5_Now': -1
                })
