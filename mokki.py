import time
import gc
import json
from utils.wifi import WiFi
from utils.dht22 import DHT22
from utils.mqtt import MQTT

def main():
    wifi = WiFi()

    if not wifi.connect():
        wifi.start_access_point()

    dht22 = DHT22()
    mqtt = MQTT('192.168.50.17', 'mokki')

    while True:
        try:
            mqtt.check_messages()

            temperature, humidity = dht22.measure()
            data = {}
            data['id'] = mqtt.id
            data['temperature'] = temperature
            data['humidity'] = humidity
            mqtt.publish(json.dumps(data))
        except KeyboardInterrupt:
            break
        time.sleep(10)

if __name__ == '__main__':
    gc.collect()
    main()
