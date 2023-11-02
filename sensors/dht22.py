import dht
from machine import Pin

class DHT22:
    def __init__(self):
        self.sensor = dht.DHT22(26)
        
    def measure(self):
        self.sensor.measure()

        temperature = self.sensor.temperature()
        humidity = self.sensor.humidity()

        return {
            'temperature': temperature,
            'humidity': humidity,
        }