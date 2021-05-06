import os

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
    app.run()
