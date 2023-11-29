import json
from umqtt.simple import MQTTClient

class MQTT:
    def __init__(self, uid, server):
        self.uid = uid
        self.server = server
        self.new_config = {}

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
        self.client.subscribe(f"command/{self.uid}")

    def publish(self, data):
        data = json.dumps(data)
        self.client.publish(f"data/{self.uid}", data)

    def sub_callback(self, topic, message):
        message = message.decode()
        try:
            self.new_config = json.loads(message)
            print(self.new_config)
        except:
            return
        
    def check_msg(self):
        self.client.check_msg()