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

SAMPLES="./output/samples.csv"

def last24(includeColumns=False): 
    earliest = datetime.datetime.now() - timedelta(hours=24)
    rows = []
    with open(SAMPLES, "r") as f:
        r = csv.reader(f)
        for i, row in enumerate(r):
            if i == 0: 
                if includeColumns:
                    rows.append(row)
                continue
            dateVal = row[0]

            # only return values from within the last 24 hours
            if dateutil.parser.isoparse(dateVal) > earliest:
                rows.append(row)
    return rows

@app.route('/data')
def send_data():
    return send_from_directory('.', SAMPLES)

@app.route('/all.csv')
def send_csv():
    return Response(last24(True).join("\n"), mimetype='text/csv')

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
