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

    url = spf.data_formatter(req_data)

    filename = "images/qr_code.png"

    qrg.create(data=url, filename=filename)

    return filename


@app.route("/get_information/<fullname>&<phone_number>&<email>")
def get_information(fullname, phone_number, email):
    # s = fullname + "/n" + phone_number + "/n" + email
    print("Here")
    return render_template("information.html", fullname=fullname, phone_number=phone_number, email=email)
