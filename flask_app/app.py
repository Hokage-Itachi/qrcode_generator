from flask import Flask, render_template, request, url_for, redirect
from module import qr_generator as qrg
from module import support_function as spf
from module import db_connector as dbc
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

    if dbc.select_by_phone(req_data.get("phone_number")):
        response = {
            "code": "01",
            "message": "Phone number has been registered",
            "data": ""
        }

        return response

    if dbc.select_by_email(req_data.get("email")):
        response = {
            "code": "02",
            "message": "Email has been registered",
            "data": ""
        }

        return response

    data = list(req_data.values())
    dbc.insert(data=data)

    url, filename = spf.data_encode(req_data)
    print(url)

    filename = "images/" + filename + ".png"

    qrg.create(data=url, filename=filename)

    response = {
        "code": "00",
        "message": "Create successfully",
        "data": {
            "filename": filename
        }
    }
    return response


@app.route("/get_information/<fullname>&<phone_number>&<email>&<address>")
def get_information(fullname, phone_number, email, address):
    if (dbc.select_by_phone(phone_number)):
        return render_template("information.html", fullname=fullname, phone_number=phone_number, email=email,
                               address=address, status="200")
    else:
        return render_template("information.html", status="404")
