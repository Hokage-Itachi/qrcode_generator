import binascii
import socket
import base64

secure_code = "4Z36rffJz4xFukmw7l0nRYVYgPkXW1kZHJeXvwmvAVtj7epD8AFsY4mhKNvCz9RXtzNzclvdK6LKId0cd1FNSS8qR2jJeAHVS1Gs"


def data_formatter(data):
    ipaddress = get_host_ip()

    protocol = "http://"
    port = ":5000"

    action = "/get_information/"
    host = protocol + ipaddress + port

    action += data.get("fullname") + "&" + data.get("phone_number") + "&" + data.get("email")
    print(len(action))
    url = host + action
    print(url)
    return url


def data_encode(data):
    ipaddress = get_host_ip()

    protocol = "http://"
    port = ":5000"

    action = "/get_information/"
    host = protocol + ipaddress + port
    info_string = ""
    for key in data:
        info_string += data.get(key) + "&"
    info_string = info_string[0:len(info_string) - 1]

    info_id = combine_b64(base64_encode(info_string), base64_encode(secure_code[0:len(info_string)]))

    action += info_id

    url = host + action

    return url, info_id


def data_decode(data):
    info_b64, secure_b64 = separate_b64(data)
    try:
        secure_string = base64_decode(secure_b64)
        info_string = base64_decode(info_b64)
    except binascii.Error as e:
        print(e)
        return "404"

    if (not secure_string in secure_code):
        return "404"

    info = info_string.split("&")

    return info


def get_host_ip():
    hostname = socket.gethostname()
    ipaddress = socket.gethostbyname(hostname)
    return ipaddress


def base64_encode(string):
    string_bytes = string.encode("ascii")

    base64_bytes = base64.b64encode(string_bytes)

    base64_string = base64_bytes.decode('ascii')

    return base64_string


def base64_decode(base64_string):
    base64_bytes = base64_string.encode("ascii")

    string_bytes = base64.b64decode(base64_bytes)

    string = string_bytes.decode("ascii")

    return string


def combine_b64(*b64_strings):
    result = ""

    n = len(b64_strings[0])

    for i in range(n):
        result += b64_strings[0][i] + b64_strings[1][i]

    return result


def separate_b64(combined_b64_string):
    n = len(combined_b64_string)
    b64_s1 = combined_b64_string[0:n:2]
    b64_s2 = combined_b64_string[1:n:2]

    return b64_s1, b64_s2
