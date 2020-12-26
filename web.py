from flask import Flask
from flask import send_from_directory

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/graph')
def send_graph():
    return send_from_directory('.', "output.png")

@app.route('/data')
def send_data():
    return send_from_directory('.', "all.csv")
