from machine import I2C, Pin
from ssd1306 import SSD1306_I2C
from micropython_qr import QRCode

from config import config

class OLED:
    def __init__(self):
        id = int(config["oled_id"])
        scl = Pin(int(config["oled_scl"]))
        sda = Pin(int(config["oled_sda"]))
        i2c = I2C(id, scl=scl, sda=sda)
        self.display = SSD1306_I2C(128, 64, i2c)
        self.qr = QRCode(border=1)
    
    def write(self, text, x=0, y=0):
        self.display.text(text, x, y)

    def generate_wifi_qr(self, ssid, password, scale=1):
        # make display white for the black QR code
        self.display.fill(1)

        # QR code format for connecting to an access point
        self.qr.add_data(f"WIFI:S:{ssid};T:WPA;P:{password};;", 0)

        matrix = self.qr.get_matrix()
        for y in range(len(matrix) * scale):
            for x in range(len(matrix[0]) * scale):
                y_s = int(y/scale)
                x_s = int(x/scale)
                value = not matrix[y_s][x_s]
                self.display.pixel(x, y, value)

        self.display.show()