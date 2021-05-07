import os
import re
import socket
from flask_cors import CORS

from flask import Flask, render_template, send_from_directory

app = Flask(__name__)
CORS(app)


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/Moment.js')
def moment_js():
    return send_from_directory(os.path.join(app.root_path, 'templates'), 'Moment.js')


@app.route('/date.js')
def date_js():
    return send_from_directory(os.path.join(app.root_path, 'templates'), 'date.js')


@app.route('/style.css')
def style_css():
    return send_from_directory(os.path.join(app.root_path, 'templates'), 'style.css')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    host_name = socket.gethostbyname(socket.gethostname())
    try:
        stream = os.popen('hostname -I')
        stream = stream.read().strip()
        val = re.search("(?:(?!\s).)*", stream)
        host_name = val[0]
    except all:
        host_name = 'localhost'
    app.run(host=host_name)
