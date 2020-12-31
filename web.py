from flask import Flask
from flask import Response
from flask import send_from_directory, stream_with_context
import csv
from io import StringIO

app = Flask(__name__)

def is_valid_data(row):
    return True

@app.route('/graph')
def send_graph():
    return send_from_directory('.', "output.png")

@app.route('/data')
def send_data():
    return send_from_directory('.', "all.csv")

@app.route('/all.csv')
def send_csv():
    def generate():
        with open("./all.csv", "r") as f:
            data = StringIO() 

            r = csv.reader(f, delimiter="\t")
            for i, row in enumerate(r):
                if i == 0:
                    data.write("".join(row) + "\n")
                    yield data.getvalue()
                    data.seek(0)
                    data.truncate(0)
                else:
                    if is_valid_data(row[0]):
                        data.write("".join(row) + "\n")
                        yield data.getvalue()
                        data.seek(0)
                        data.truncate(0)
    return Response(generate(), mimetype='text/csv')

@app.route('/')
@app.route('/chart')
def send_chart():
    return send_from_directory('.', "chart.html")
