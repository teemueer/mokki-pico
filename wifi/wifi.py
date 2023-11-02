import network
import time

class Wifi:
    def __init__(self):
        self.wlan = network.WLAN(network.STA_IF)

    def connect(self, ssid, password, timeout=30):
        self.wlan.active(True)
        self.wlan.connect(ssid, password)

        start = time.ticks_ms()
        while (time.ticks_ms() - start) < (timeout * 1000):
            if self.wlan.isconnected() and self.wlan.status() == network.STAT_GOT_IP:
                return True

        self.wlan.active(False)
        return False