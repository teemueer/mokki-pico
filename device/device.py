import json
from machine import Pin, Timer
from time import ticks_ms, ticks_diff, sleep

from config import Config
from wifi import Wifi
from ble import BLE
from mqtt import MQTT
from sensors import DHT22, KY018
from utils.oled import OLED
from utils.common import get_random_string, restart

class Device:
    INIT_MODE = 0
    APP_MODE = 1
    BLE_MODE = 2
    ERROR_MODE = 3

    def __init__(self):
        self.config = Config()
        self.oled = OLED()
        self.wifi = Wifi()

        self._ble_button = Pin(9, Pin.IN, Pin.PULL_UP)
        self._ble_button_timer = Timer(-1)
        self._ble_button.irq(handler=self._ble_button_handler, trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING)

        self.mqtt = None
        self.last_mqtt_send_time = 0
        self.mqtt_send_interval = 10 * 1000

        self.sensors = [DHT22(), KY018()]

        self.mode = self.INIT_MODE

    def _ble_button_handler(self, pin):
        if pin.value() == 0:
            self._ble_button_timer.init(period=1000, mode=Timer.ONE_SHOT, callback=lambda s: self.switch_mode(self.BLE_MODE))
        else:
            self._ble_button_timer.deinit()

    def switch_mode(self, mode):
        self.mode = mode

    def init_mode(self):
        self.oled.write("*** INIT ***")

        ssid = self.config.get("wlan_ssid")
        password = self.config.get("wlan_password")
        
        #print(ssid, password)

        if ssid and self.wifi.connect(ssid, password, 30):
            print("connected to wifi")
            self.switch_mode(self.APP_MODE)
        else:
            self.switch_mode(self.ERROR_MODE)

    def app_mode(self):
        self.oled.write("*** APP ***")

        now = ticks_ms()
        if ticks_diff(now, self.last_mqtt_send_time) < self.mqtt_send_interval:
            return
        
        if self.mqtt:
            self.mqtt.check_msg()
            if self.mqtt.new_config:
                for key, value in self.mqtt.new_config.items():
                    self.config.set(key, float(value))
                self.new_config = {}

        if not self.mqtt:
            uid = self.config.get("uuid")
            server = self.config.get("mqtt_broker_url")
            self.mqtt = MQTT(uid, server)


        all_data = {}
        for sensor in self.sensors:
            sensor_data = sensor.measure()
            
            if "temperature" in sensor_data:
                set_temperature = self.config.get("set_temperature", 0)
                if set_temperature > 0:
                    sensor_data["temperature"] = set_temperature
            
            all_data |= sensor_data

        print(f"Publishing:", all_data)
        self.mqtt.publish(all_data)
        
        self.last_mqtt_send_time = now

    def ble_mode(self, timeout=60):
        self.oled.write("*** BLE ***")

        name = get_random_string()
        ble = BLE(name, self.oled)
        ble.start()

        buffer = b""
        def receive_data(data):
            nonlocal buffer
            buffer += data

        ble.on_write(receive_data)
        
        with open("secrets/secret.enc2", "rb") as f:
            secret = f.read()

        start = ticks_ms()
        while (ticks_ms() - start) < (timeout * 1000):
            if ble.sp.is_connected():
                print("sending secret...")
                ble.send(secret)
                
                if buffer.endswith(b"\0"):  # type: ignore
                    try:
                        data = json.loads(buffer[:-1])
                        print("got data", data)
                        self.config.set("wlan_ssid", data.get("wlan_ssid"))
                        self.config.set("wlan_password", data.get("wlan_password"))
                        self.config.set("mqtt_broker_url", data.get("mqtt_broker_url"))
                        self.config.set("uuid", data.get("uuid"))
                        self.mqtt = None
                    except:
                        pass
                    break
            sleep(1)

        ble.stop()
        #restart()
        self.switch_mode(self.INIT_MODE)

    def error_mode(self):
        self.oled.write("*** ERROR ***")

    def run(self):
        while True:
            if self.mode == self.INIT_MODE:
                self.init_mode()
            elif self.mode == self.APP_MODE:
                self.app_mode()
            elif self.mode == self.BLE_MODE:
                self.ble_mode()
            elif self.mode == self.ERROR_MODE:
                self.error_mode()
            
            sleep(0.1)

if __name__ == "__main__":
    device = Device()
    device.run()
