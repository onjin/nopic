from StringIO import StringIO

from PIL import Image, ImageFont, ImageDraw
import flask
from flask import Flask, request

app = Flask(__name__)


def get_image_response(width, height, background='cccccc',
                       foreground='666666', background_alpha=0,
                       foreground_alpha=0, text=None, font=None, size=16):
    buf = StringIO()
    img = Image.new("RGB", (width, height), '#' + background)

    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("fonts/Lobster_1.3.otf", size)
    w, h = font.getsize(text)
    draw.text(
        ((width - w) / 2, (height - h) / 2),
        text, '#' + foreground, font=font
    )

    img.save(buf, "PNG")

    resp = flask.make_response(buf.getvalue())
    resp.content_type = "image/jpeg"
    return resp


@app.route('/<int:width>/',)
@app.route('/<int:width>/<string:background>/',)
@app.route('/<int:width>/<string:background>/<string:foreground>/',)
@app.route('/<int:width>x<int:height>/')
@app.route('/<int:width>x<int:height>/<string:background>/')
@app.route('/<int:width>x<int:height>/<string:background>/<string:foreground>/')
def fakeimg(width, height=None, background='cccccc', foreground='666666',
            background_alpha=0, foreground_alpha=0, font=None):
    if not height:
        height = width
    text = request.args.get('text', "%s x %s" % (width, height)).encode('utf8')
    size = int(request.args.get('size', 16))

    return get_image_response(
        width, height, background, foreground, background_alpha,
        foreground_alpha, text, font, size
    )

app.run(debug=True)
