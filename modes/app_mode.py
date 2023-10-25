from utime import sleep

from utils.mqtt import MQTT
from sensors.dht22 import DHT22
from sensors.ky018 import KY018

def start():
    print("*** Starting application mode")

    mqtt = MQTT()

    dht22 = DHT22()
    ky018 = KY018()

    while True:
        try:
            data = dht22.measure() | ky018.measure()
            mqtt.publish(data)
            mqtt.check_messages()
        except KeyboardInterrupt:
            break
        sleep(5)