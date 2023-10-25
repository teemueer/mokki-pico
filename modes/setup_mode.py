import json
from phew import server, access_point, dns
from phew.template import render_template

from config import config, save_config
from utils.common import restart
from utils.oled import OLED

AP_NAME = "Pico W"
AP_PASSWORD = "12345678"
AP_DOMAIN = "pipico.net"

@server.route("/")
def index(req):
    if req.headers.get("host") != AP_DOMAIN:
        return render_template("templates/redirect.html", domain=AP_DOMAIN)

    return render_template("templates/index.html", **config)

@server.route("/configure", methods=["POST"])
def configure(req):
    save_config(req.form)
    #restart()
    return render_template("templates/configured.html")

@server.catchall()
def catch_all(req):
    if req.headers.get("host") != AP_DOMAIN:
        return render_template("templates/redirect.html", domain=AP_DOMAIN)
    return "Not found", 404

def start():
    print("*** Starting Setup mode...")

    oled = OLED()

    ap = access_point(AP_NAME, AP_PASSWORD)
    ip = ap.ifconfig()[0]
    dns.run_catchall(ip)

    oled.generate_wifi_qr(AP_NAME, AP_PASSWORD, 1.5)

    server.run()