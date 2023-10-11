from machine import ADC, Pin


class KY018:
    def __init__(self):
        self.adc = ADC(Pin(27))

    def measure(self):
        value = self.adc.read_u16()
        voltage = (value / 65535) * 3.3
        return {
            'value': value,
            'voltage': voltage,
        }
