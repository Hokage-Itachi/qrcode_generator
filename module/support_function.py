import socket


def data_formatter(data):
    ipaddress = get_host_ip()

    protocol = "http://"
    port = ":5000"

    action = "/get_information/"
    host = protocol + ipaddress + port

    action += data.get("fullname") + "&" + data.get("phone_number") + "&" + data.get("email")
    # print(action)
    url = host + action
    print(url)
    return url


def get_host_ip():
    hostname = socket.gethostname()
    ipaddress = socket.gethostbyname(hostname)
    return ipaddress
