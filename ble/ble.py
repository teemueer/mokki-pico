import bluetooth

from .ble_simple_peripheral import BLESimplePeripheral

class BLE:
    def __init__(self, name, oled):
        self.name = name
        self.oled = oled
        self.ble = bluetooth.BLE()
        self.sp = BLESimplePeripheral(self.ble, name)
    
    def on_write(self, callback):
        self.sp.on_write(callback)

    def send(self, data):
        self.sp.send(data)

    def start(self):
        self.sp._advertise()
        
        # in the future generate QR with just the name for the mobile app to read
        self.oled.generate_qr(f"http://192.168.50.208:5000/devices/register?name={self.name}")

    def stop(self):
        self.ble.active(False)