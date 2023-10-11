import time
import gc
import json
from utils.wifi import WiFi
from utils.dht22 import DHT22
from utils.ky018 import KY018
from utils.mqtt import MQTT


def main():
    wifi = WiFi()

    if not wifi.connect():
        wifi.start_access_point()

    dht22 = DHT22()
    ky018 = KY018()

    mqtt = MQTT('192.168.50.17', 'mokki')

    while True:
        try:
            mqtt.check_messages()
            data = {
                'id': mqtt.id,
                'dht22': dht22.measure(),
                'ky018': ky018.measure(),
            }
            mqtt.publish(json.dumps(data))
        except KeyboardInterrupt:
            break
        time.sleep(10)


if __name__ == '__main__':
    gc.collect()
    main()
