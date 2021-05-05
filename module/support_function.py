import binascii
import socket
import base64
import re

secure_code = "4Z36rffJz4xFukmw7l0nRYVYgPkXW1kZHJeXvwmvAVtj7epD8AFsY4mhKNvCz9RXtzNzclvdK6LKId0cd1FNSS8qR2jJeAHVS1Gs"


def data_encode(data):
    action = "/get_information/"
    host = get_host()
    info_string = ""
    for key in data:
        info_string += data.get(key) + "&"
    info_string = info_string[0:len(info_string) - 1]
    secure_string = secure_code[0:len(info_string)]
    info_id = combine_b64(base64_encode(info_string), base64_encode(secure_string))

    action += info_id

    url = host + action

    return url, info_id


def data_decode(data):
    info_b64, secure_b64 = separate_b64(data)
    try:
        secure_string = base64_decode(secure_b64).rstrip()
        info_string = base64_decode(info_b64).rstrip()
    except binascii.Error as e:
        print(e)
        return "404"

    if (not secure_string in secure_code):
        return "404"

    info = info_string.split("&")

    return info


def get_host():
    ipaddress = get_host_ip()

    protocol = "http://"

    port = ":5000"

    host = protocol + ipaddress + port
    return host


def base64_encode(string):
    string_bytes = bytes(string, "utf-8")

    base64_bytes = base64.b64encode(string_bytes)

    base64_string = base64_bytes.decode('ascii', "utf-8")

    return base64_string


def base64_decode(base64_string):
    base64_bytes = bytes(base64_string, "utf-8")

    string_bytes = base64.b64decode(base64_bytes)

    string = str(string_bytes, "utf-8")

    return string


def combine_b64(*b64_strings):
    result = ""
    s1 = b64_strings[0]
    s2 = b64_strings[1]
    n = len(s1)
    m = len(s2)
    if m > n:
        k = (m - n) // 4
        additional_space = ""
        for i in range(k):
            additional_space += "   "
        s1 += base64_encode(additional_space)
    else:
        k = (n - m) // 4
        additional_space = ""
        for i in range(k):
            additional_space += "   "

        s2 += base64_encode(additional_space)

    for i in range(n):
        result += s1[i] + s2[i]

    return result


def separate_b64(combined_b64_string):
    n = len(combined_b64_string)
    b64_s1 = combined_b64_string[0:n:2]
    b64_s2 = combined_b64_string[1:n:2]

    return b64_s1, b64_s2


def data_format(data):
    action = "/get_information/"
    host = get_host()

    filename = ""

    for i in data:
        filename += data[i] + "_"
        action += data[i] + "&"

    filename = filename[0:len(filename) - 1]
    action = action[0: len(action) - 1]

    filename = re.sub(" ", "_", filename)

    url = host + action

    return url, filename


def get_host_ip():
    hostname = socket.gethostname()
    ipaddress = socket.gethostbyname(hostname)

    return ipaddress
