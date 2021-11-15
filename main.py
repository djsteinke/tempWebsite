import os
import re
import socket
from flask_cors import CORS
from PIL import Image, ImageDraw, ImageFont
from PIL.ImageFont import load_default

from flask import Flask, render_template, send_from_directory, url_for

app = Flask(__name__)
CORS(app)


@app.route('/img')
def get_image():
    w = 758
    h = 758
    img = Image.new('RGB', (w, h), color="#FFFFFF")
    canvas = ImageDraw.Draw(img)

    font = ImageFont.truetype('Roboto-Regular.ttf', 50)
    text_width, text_height = canvas.textsize('Outside', font=font)
    x_pos = int((w - text_width) / 2)
    y_pos = int(text_height/2)
    canvas.text((x_pos, y_pos), "Outside", font=font, fill='#000000')

    font = ImageFont.truetype('Roboto-Regular.ttf', 30)
    text_width, text_height = canvas.textsize('Temperature', font=font)
    x_pos = int(w/4 - text_width/2)
    y_pos = int(y_pos + 50 + (text_height*1.1))
    canvas.text((x_pos, y_pos), "Temperature", font=font, fill='#000000')

    font = ImageFont.truetype('Roboto-Regular.ttf', 30)
    text_width, text_height = canvas.textsize('Humidity', font=font)
    x_pos = int(3*w/4 - text_width/2)
    canvas.text((x_pos, y_pos), "Humidity", font=font, fill='#000000')

    font = ImageFont.truetype('Roboto-Regular.ttf', 100)
    text_width, text_height = canvas.textsize('T Val', font=font)
    x_pos = int(w/4 - text_width/2)
    y_pos = int(y_pos + 50 )
    canvas.text((x_pos, y_pos), "T Val", font=font, fill='#000000')

    font = ImageFont.truetype('Roboto-Regular.ttf', 100)
    text_width, text_height = canvas.textsize('H Val', font=font)
    x_pos = int(3*w/4 - text_width/2)
    canvas.text((x_pos, y_pos), "H Val", font=font, fill='#000000')

    img.rotate(90).show()

    img.save('static/image.jpg')
    v = '<img src=' + url_for('static', filename='image.jpg') + '>'
    print(v)
    return 'value'


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
    host_name = socket.gethostbyname(socket.gethostname())
    try:
        stream = os.popen('hostname -I')
        stream = stream.read().strip()
        val = re.search("(?:(?!\s).)*", stream)
        host_name = val[0]
    except all:
        host_name = 'localhost'
    app.run(host=host_name)
