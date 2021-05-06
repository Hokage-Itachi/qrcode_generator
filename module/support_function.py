import json
import socket

import re

import pandas


def get_host():
    ipaddress = get_host_ip()

    protocol = "http://"

    port = ":5000"

    host = protocol + ipaddress + port
    return host


def data_format(data):
    action = "/get_information/"
    host = get_host()

    filename = ""

    filename += data[0] + "_" + data[1]
    for i in data:
        action += i + "&"

    action = action[0: len(action) - 1]

    filename = re.sub(" ", "_", filename)

    url = host + action
    print(filename)
    return url, filename


def get_host_ip():
    hostname = socket.gethostname()
    ipaddress = socket.gethostbyname(hostname)

    return ipaddress


def to_excel(data):
    filename = "D:/Excel/QRCode_app/user_data.xlsx"

    data_dict = json.loads(data)
    columns = ["Họ và tên", "Số điện thoại", "Email", "Địa chỉ"]

    df = pandas.DataFrame()

    for user_data in data_dict.get("data"):
        data_list = list(user_data.values())
        user_df = pandas.DataFrame([data_list], columns=columns)
        # print(user_data)
        df = pandas.concat([df, user_df], ignore_index=True)

    writer = pandas.ExcelWriter(filename, engine="xlsxwriter")
    df.to_excel(writer)
    writer.close()
    return filename
