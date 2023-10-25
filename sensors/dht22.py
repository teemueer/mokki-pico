import dht
from machine import Pin

from config import config


class DHT22:
    def __init__(self):
        pin = Pin(int(config["dht22_pin"]))
        self.sensor = dht.DHT22(pin)
        
    def measure(self):

        self.sensor.measure()
        temperature = self.sensor.temperature()
        humidity = self.sensor.humidity()
        return {
            'temperature': temperature,
            'humidity': humidity,
        }
