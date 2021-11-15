import os
import re
import socket
import requests
import threading
from flask_cors import CORS
from PIL import Image, ImageDraw, ImageFont

from flask import Flask, render_template, send_from_directory, url_for

app = Flask(__name__)
CORS(app)

timer = None


@app.route('/img')
def get_image():
    response = requests.get('http://192.168.0.140:31000/getTemp')
    r_json = response.json()
    t = int(round(r_json['temp_f'], 0))
    h = int(round(r_json['humidity'], 0))
    # t = 75
    # h = 30
    t_str = f'{t}\N{DEGREE SIGN}F'
    h_str = f'{h}%'

    font_family = 'Ubuntu-R.ttf'
    #font_family = '/static/Roboto-Regular.ttf'
    w = 860
    h = 350
    img = Image.new('RGB', (w, h), color="#FFFFFF")
    canvas = ImageDraw.Draw(img)

    font = ImageFont.truetype(font_family, 60)
    text_width, text_height = canvas.textsize('Outside', font=font)
    x_pos = int((w - text_width) / 2)
    y_pos = int(text_height/2)
    canvas.text((x_pos, y_pos), "Outside", font=font, fill='#000000')

    font = ImageFont.truetype(font_family, 35)
    text_width, text_height = canvas.textsize('Temperature', font=font)
    x_pos = int(w/3.5 - text_width/2)
    y_pos = int(y_pos + 50 + (text_height*1.1))
    canvas.text((x_pos, y_pos), "Temperature", font=font, fill='#000000')

    font = ImageFont.truetype(font_family, 35)
    text_width, text_height = canvas.textsize('Humidity', font=font)
    x_pos = int(2.5*w/3.5 - text_width/2)
    canvas.text((x_pos, y_pos), "Humidity", font=font, fill='#000000')

    font = ImageFont.truetype(font_family, 120)
    text_width, text_height = canvas.textsize(t_str, font=font)
    x_pos = int(w/3.5 - text_width/2)
    y_pos = int(y_pos + 50)
    canvas.text((x_pos, y_pos), t_str, font=font, fill='#000000')

    font = ImageFont.truetype(font_family, 120)
    text_width, text_height = canvas.textsize(h_str, font=font)
    x_pos = int(2.5*w/3.5 - text_width/2)
    canvas.text((x_pos, y_pos), h_str, font=font, fill='#000000')

    img = img.rotate(90, expand=True)

    img.save('static/image.jpg')

    threading.Timer(60, get_image).start()


@app.route('/')
def home():
    return render_template("home_rotate.html")


@app.route('/Moment.js')
def moment_js():
    return send_from_directory(os.path.join(app.root_path, 'templates'), 'Moment.js')


@app.route('/style.css')
def style_css():
    return send_from_directory(os.path.join(app.root_path, 'templates'), 'style.css')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    get_image()
    host_name = socket.gethostbyname(socket.gethostname())
    try:
        stream = os.popen('hostname -I')
        stream = stream.read().strip()
        val = re.search("(?:(?!\s).)*", stream)
        host_name = val[0]
    except all:
        host_name = 'localhost'
    app.run(host=host_name)
