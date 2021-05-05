import socket

import re


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

    filename = filename[0:len(filename) - 1]
    action = action[0: len(action) - 1]

    filename = re.sub(" ", "_", filename)

    url = host + action

    return url, filename


def get_host_ip():
    hostname = socket.gethostname()
    ipaddress = socket.gethostbyname(hostname)

    return ipaddress
