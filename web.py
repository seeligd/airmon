from flask import Flask
from flask import send_from_directory

app = Flask(__name__)

@app.route('/graph')
def send_graph():
    return send_from_directory('.', "output.png")

@app.route('/data')
def send_data():
    return send_from_directory('.', "all.csv")

@app.route('/all.csv')
def send_csv():
    return send_from_directory('.', "all.csv")

@app.route('/')
@app.route('/chart')
def send_chart():
    return send_from_directory('.', "chart.html")
