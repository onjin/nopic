from StringIO import StringIO

from itsdangerous import URLSafeSerializer

from PIL import Image, ImageFont, ImageDraw
import flask
from flask import Flask, request, render_template, url_for, redirect

app = Flask(__name__, static_url_path='/media')

SECRET = 'changeme'


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

    lines = text.split('\\n')
    _, lines_height = font.getsize(lines[0])
    text_height = (height - (len(lines) * lines_height)) / 2
    for index, line in enumerate(lines):
        w, h = font.getsize(line)
        draw.text(
            ((width - w) / 2, text_height),
            line, '#' + foreground, font=font
        )
        text_height += lines_height

    img.save(buf, "PNG")

    resp = flask.make_response(buf.getvalue())
    resp.content_type = "image/jpeg"
    return resp


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/c/<path:url>')
def create_short(url):
    s = URLSafeSerializer(SECRET)
    short = s.dumps(url)
    return redirect('/s/' + short)


@app.route('/s/<path:path>/')
def open_short(path):
    s = URLSafeSerializer(SECRET)
    short = s.loads(path)
    return redirect('/' + short)


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
    text = request.args.get('text', u"%s x %s" % (width, height))

    size = int(request.args.get('size', 16))
    font = request.args.get('font', 'lobster')

    return get_image_response(
        width, height, background, foreground, background_alpha,
        foreground_alpha, text, font, size
    )

if __name__ == '__main__':
    app.run(debug=True)
