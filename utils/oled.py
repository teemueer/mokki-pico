from machine import I2C, Pin
from ssd1306 import SSD1306_I2C
from micropython_qr import QRCode

class OLED:
    def __init__(self):
        i2c = I2C(id=1, scl=Pin(15), sda=Pin(14))
        self.display = SSD1306_I2C(128, 64, i2c)
        self.qr = QRCode(border=1)

    def write(self, text):
        self.fill(0)

        y = 0
        for t in text.split("\n"):
            self.text(t, 0, y)
            y += 8

        self.show()
    
    def text(self, text, x=0, y=0):
        self.display.text(text, x, y)

    def fill(self, value):
        self.display.fill(value)

    def show(self):
        self.display.show()

    def generate_qr(self, message, scale=1):
        self.fill(1)

        self.qr.clear()
        self.qr.add_data(message, 0)
        matrix = self.qr.get_matrix()
        if not matrix:
            return

        for y in range(len(matrix) * scale):
            for x in range(len(matrix[0]) * scale):
                y_s = int(y/scale)
                x_s = int(x/scale)
                value = not matrix[y_s][x_s]
                self.display.pixel(x, y, value)

        self.show()
