import dht
from machine import Pin
from utils.oled import OLED

class DHT22:
    def __init__(self):
        self.sensor = dht.DHT22(Pin(26))
        self.oled = OLED()

    def measure(self):
        self.sensor.measure()
        temperature = self.sensor.temperature()
        humidity = self.sensor.humidity()

        self.oled.clear()
        self.oled.write(f'Temperature:')
        self.oled.write(f'{temperature}C', 32, 16)
        self.oled.write(f'Humidity:', 0, 32)
        self.oled.write(f'{humidity}%', 32, 48)
        self.oled.show()

        return temperature, humidity