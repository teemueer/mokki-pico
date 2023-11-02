import json
from umqtt.simple import MQTTClient

class MQTT:
    def __init__(self, uid, server):
        self.uid = uid
        self.server = server

        self.client = MQTTClient(
            self.uid,
            self.server,
            ssl=True,
            ssl_params={
                "cert": "/certs/ca.crt"
            },
        )

        self.client.set_callback(self.sub_callback)
        self.client.connect()
        self.client.subscribe(f"sensors/{self.uid}/commands")

    def publish(self, data):
        data = json.dumps(data)
        self.client.publish(f"sensors/{self.uid}", data)

    def sub_callback(self, topic, message):
        message = message.decode()
        print("topic:", topic, "message:", message)