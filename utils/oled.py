import ssd1306
from machine import I2C, Pin

class OLED:
    def __init__(self):
        self.i2c = I2C(1, scl=Pin(15), sda=Pin(14))
        self.display = ssd1306.SSD1306_I2C(128, 64, self.i2c)

    def write(self, text, x=0, y=0):
        self.display.text(text, x, y)
    
    def show(self):
        self.display.show()

    def clear(self):
        self.display.fill(0)