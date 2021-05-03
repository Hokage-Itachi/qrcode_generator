import qrcode


def create(data, filename):
    path = "flask_app/static/"
    img = qrcode.make(data)
    img.save(path + filename)
    return filename
