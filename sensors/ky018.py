from machine import ADC, Pin

class KY018:
    def __init__(self):
        self.sensor = ADC(Pin(27))

    def measure(self):
        try:
            value = self.sensor.read_u16()
            light_level = 100 - ((value / 65535) * 100)
            return {
                "light_level": round(light_level, 1),
            }
        except:
            return {}