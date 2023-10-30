import json
from umqtt.simple import MQTTClient

from config import config
from utils.common import get_unique_id

class MQTT:
    def __init__(self):
        self.uid = config.get("uid")

        self.client = MQTTClient(
            self.uid,
            config.get("mqtt_server"),
            ssl=True,
            ssl_params={
                "cert": "/certs/ca.crt"
            },
        )

        self.client.set_callback(self.sub_callback)
        self.client.connect()
        #self.client.subscribe(config.get("mqtt_topic_subcribe"))
        self.client.subscribe(f"sensors/{self.uid}/commands")

    def publish(self, data):
        data = json.dumps(data)
        #self.client.publish(config.get("mqtt_topic_publish"), data)
        self.client.publish(f"sensors/{self.uid}", data)

    def check_messages(self):
        self.client.check_msg()

    def sub_callback(self, topic, message):
        message = message.decode()
        print("topic:", topic, "message:", message)