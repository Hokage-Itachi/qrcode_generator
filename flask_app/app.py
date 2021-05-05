from flask import Flask, render_template, request, url_for, redirect
from module import qr_generator as qrg
from module import support_function as spf
import json

app = Flask(__name__)


@app.route('/')
@app.route("/<img_file>")
def home(img_file=None):
    if (img_file):
        return render_template("home.html", img_file=img_file)
    else:
        return render_template("home.html")


@app.route("/generate", methods=["POST"])
def generate():
    req_data = request.get_data().decode("utf-8")
    req_data = json.loads(req_data)

    url, info_id = spf.data_encode(req_data)
    print(url)
    filename = "images/" + info_id + ".png"

    qrg.create(data=url, filename=filename)

    return filename


@app.route("/get_information/<info_id>")
def get_information(info_id):
    info = spf.data_decode(info_id)
    if (info == "404"):
        return render_template("information.html", status="404")
    # print("Here")
    return render_template("information.html", fullname=info[0], phone_number=info[1], email=info[2], status="200")
