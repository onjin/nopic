from StringIO import StringIO

from PIL import Image, ImageFont, ImageDraw
import flask
from flask import Flask, request, render_template

app = Flask(__name__, static_url_path='/media')


def get_image_response(width, height, background='cccccc',
                       foreground='666666', background_alpha=0,
                       foreground_alpha=0, text=None, font=None, size=16):
    buf = StringIO()
    img = Image.new("RGB", (width, height), '#' + background)

    # font
    draw = ImageDraw.Draw(img)
    fontname = font + '.otf'
    try:
        font = ImageFont.truetype("fonts/" + fontname, size)
    except IOError:
        fontname = 'lobster.otf'
        font = ImageFont.truetype("fonts/" + fontname, size)

    w, h = font.getsize(text)
    draw.text(
        ((width - w) / 2, (height - h) / 2),
        text, '#' + foreground, font=font
    )

    img.save(buf, "PNG")

    resp = flask.make_response(buf.getvalue())
    resp.content_type = "image/jpeg"
    return resp


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/<int:width>/',)
@app.route('/<int:width>/<string:background>/',)
@app.route('/<int:width>/<string:background>/<string:foreground>/',)
@app.route('/<int:width>x<int:height>/')
@app.route('/<int:width>x<int:height>/<string:background>/')
@app.route('/<int:width>x<int:height>/<string:background>/<string:foreground>/')
def fakeimg(width, height=None, background='cccccc', foreground='666666',
            background_alpha=0, foreground_alpha=0):
    if not height:
        height = width
    text = request.args.get('text', "%s x %s" % (width, height)).encode('utf8')
    size = int(request.args.get('size', 16))
    font = request.args.get('font', 'lobster')

    return get_image_response(
        width, height, background, foreground, background_alpha,
        foreground_alpha, text, font, size
    )

if __name__ == '__main__':
    app.run(debug=True)
