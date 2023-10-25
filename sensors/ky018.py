from machine import ADC, Pin

from config import config

class KY018:
    def __init__(self):
        pin = Pin(int(config["ky018_pin"]))
        self.sensor = ADC(pin)

    def measure(self):
        try:
            value = self.sensor.read_u16()
            light_level = 100 - ((value / 65535) * 100)
            return {
                "light_level": light_level,
            }
        except:
            return {}