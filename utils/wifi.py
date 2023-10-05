import network
import json
import random
import socket
import time
from utils.common import file_exists, get_unique_id
from utils.oled import OLED

ACCESS_POINT_HTML = '''
<html>
<head>
<title>Raspberry Pi Pico W WiFi Setup</title>
</head>
<body>
    <h2>Device {id} WiFi Setup</h2>
    
    <p>Connected to WiFi: <b>{connected}</b></p>
    <p style="color: red;">{error}</p>
    
    <p>Enter your wireless information below</p>

    <form action="/" method="post">
    <table>
        <tr>
            <th>SSID:</th>
            <td><input type="text" name="ssid" value="{wlan_ssid}"></td>
        </tr>
        <tr>
            <th>Password:</th>
            <td><input type="password" name="password" value={wlan_password}></td>
        </tr>
        <tr>
        <td colspan="2">
            <input type="submit" value="Connect">
        </td>
        </tr>
    </table>
    </form>
</body>
</html>
'''

class WiFi:
    WIFI_FILE = 'wifi.json'

    def __init__(self):
        self.wlan = network.WLAN(network.STA_IF)
        self.access_point = network.WLAN(network.AP_IF)
        self.ip = None
        self.oled = OLED()

    def connect(self, ssid=None, password=None, timeout=10):
        if not ssid and file_exists(self.WIFI_FILE):
            with open(self.WIFI_FILE, 'r') as f:
                credentials = json.load(f)
        elif ssid and password:
            credentials = {}
            credentials['ssid'] = ssid
            credentials['password'] = password
        else:
            return False

        self.wlan.active(True)
        self.wlan.connect(credentials['ssid'], credentials['password'])

        while timeout > 0:
            print(f'Connecting to wifi... {timeout}')
            if self.wlan.isconnected():
                break
            time.sleep(1)
            timeout -= 1
        else:
            self.wlan.active(False)
            return False
        
        self.ip = self.wlan.ifconfig()[0]

        with open(self.WIFI_FILE, 'w') as f:
            json.dump(credentials, f)

        print('Connection successful!')

        return True

    def start_access_point(self, timeout=10):
        ap_ssid = 'Pico W' #get_unique_id()
        ap_password = '12345678' #''.join(random.choice('0123456789') for _ in range(8))

        print(f'Starting access point with SSID {ap_ssid} and password {ap_password}')

        self.access_point.config(essid=ap_ssid, password=ap_password)
        self.access_point.active(True)

        while timeout > 0:
            if self.access_point.isconnected():
                break
            time.sleep(1)
            timeout -= 1
        else:
            self.access_point.active(False)
            return False

        self.ip = self.access_point.ifconfig()[0]

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('', 80))
        sock.listen(1)

        self.oled.clear()
        self.oled.write('SSID:', 0, 0)
        self.oled.write(ap_ssid, 0, 8)
        self.oled.write('Password:', 0, 24)
        self.oled.write(ap_password, 0, 32)
        self.oled.write('IP:', 0, 48)
        self.oled.write(self.ip, 0, 56)
        self.oled.show()

        wlan_ssid = ''
        wlan_password = ''
        error = ''
        while True:
            try:
                conn, addr = sock.accept()
                print(f'Client connected {addr}')

                req = conn.recv(1024).decode('utf-8')

                if 'POST' in req:
                    params = req.split('\n')[-1]
                    for param in params.split('&'):
                        key, value = param.split('=')
                        if key == 'ssid':
                            wlan_ssid = value
                        elif key == 'password':
                            wlan_password = value
        
                    if self.connect(wlan_ssid, wlan_password):
                        error = ''
                        self.access_point.active(False)
                        break
                    else:
                        error = 'Failed to connect. Please try again.'

                conn.send(ACCESS_POINT_HTML.format(
                    id=get_unique_id(),
                    connected='yes' if self.wlan.isconnected() else 'no',
                    error=error,
                    wlan_ssid=wlan_ssid,
                    wlan_password=wlan_password))

                conn.close()
            except KeyboardInterrupt:
                break

        sock.close()
        self.access_point.active(False)
