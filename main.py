import os
import re
import socket

from flask import Flask, render_template, send_from_directory

app = Flask(__name__)


@app.route('/')
def home():
    return render_template("home.html")


@app.route('/style.css')
def favicon():
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
