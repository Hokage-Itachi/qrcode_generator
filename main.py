from flask_app.app import app
from module import support_function as spf

# host = "192.168.50.33"
host = spf.get_host_ip()
app.run(host=host, debug=True)
