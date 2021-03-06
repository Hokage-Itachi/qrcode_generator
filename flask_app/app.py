from flask import Flask, render_template, request, send_file, url_for, redirect, session
from module import qr_generator as qrg
from module import support_function as spf
from module import db_connector as dbc
import json

app = Flask(__name__)
check_in_ip = "192.168.50.193"
app.secret_key = "abcdef"
admin_account = {
    "username": "admin",
    "password": "123"
}


@app.route('/')
def home():
    if not session.get("user"):
        return render_template("home.html", role="user")
    else:
        return redirect(url_for("render_admin"))


@app.route("/generate", methods=["POST"])
def generate():
    req_data = request.get_data().decode("utf-8")
    req_data = json.loads(req_data)

    if dbc.select_by_phone(req_data.get("phone_number")):
        response = {
            "code": "01",
            "message": "Số điện thoại đã được đăng ký",
            "data": ""
        }

        return response

    if dbc.select_by_email(req_data.get("email")):
        response = {
            "code": "02",
            "message": "Email đã được đăng ký",
            "data": ""
        }

        return response

    data = list(req_data.values())
    dbc.insert(data=data)

    url, filename = spf.data_format(data)
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
    if dbc.check_exist(fullname, phone_number, email, address):
        code = "00"
        if request.remote_addr == check_in_ip:
            status = 1
            dbc.update(fullname, phone_number, email, address, status)
            code = "01"
        return render_template("information.html", fullname=fullname, phone_number=phone_number, email=email,
                               address=address, code=code)
    else:
        code = "02"
        return render_template("information.html", code=code)


@app.route("/statistic")
def statistic():
    query_result = dbc.select_all()

    data = []
    i = 1
    if query_result:
        for row in query_result:

            status = "Chưa check in"
            if row[5] == 1:
                status = "Đã check in"

            user_info = {
                "id": i,
                "fullname": row[1],
                "phone_number": row[2],
                "email": row[3],
                "address": row[4],
                "status": status
            }
            i += 1

            data.append(user_info)

    return render_template("statistic.html", data=data)


@app.route("/export", methods=["POST"])
def export():
    req_data = request.form.get("data")

    filename = spf.to_excel(req_data)
    return send_file(filename, as_attachment=True)


@app.route("/visualize", methods=["POST"])
def visualize():
    address_data = dbc.group_by_address()

    status_data = dbc.group_by_status()

    resp_data = {
        "address_data": {},
        "status_data": {}
    }
    for d in address_data:
        resp_data["address_data"][d[0]] = d[1]

    for d in status_data:
        if d[0] == 1:
            key = "Đã check in"
        else:
            key = "Chưa check in"
        resp_data["status_data"][key] = d[1]

    response = {
        "code": "00",
        "message": "Data group by address",
        "data": []
    }

    if not address_data:
        response["code"] = "01"
        response["message"] = "No data found"

    response["data"] = resp_data

    return response


@app.route("/admin/login", methods=["POST", "GET"])
def render_login():
    # session["user"] = request.remote_addr
    if request.method == "GET":
        if not session.get("user"):
            return render_template("login.html", message=None)
    else:
        username = request.form["username"]
        passwd = request.form["password"]

        # if username == admin_account.get("username") and passwd == admin_account.get("password"):
        if True:
            session["user"] = username
        else:
            return render_template("login.html", message="Tên đăng nhập hoặc mật khẩu không đúng")
    return redirect(url_for("render_admin"))


@app.route("/admin")
def render_admin():
    if not session.get("user"):
        return redirect(url_for("render_login"))
    return render_template("home.html", role="admin")

