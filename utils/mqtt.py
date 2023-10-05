from umqtt.simple import MQTTClient
from utils.common import get_unique_id

class MQTT:
    def __init__(self, server, topic):
        self.id = get_unique_id()
        
        self.server = server
        self.publish_topic = f'{topic}/room1'
        self.subscribe_topic = f'{topic}/commands'

        ssl_params = {}
        ssl_params['cert'] = '/certs/mosquitto.crt'

        self.client = MQTTClient(
            self.id,
            self.server,
            ssl=True,
            ssl_params=ssl_params)

        self.client.set_callback(self.sub_callback)
        self.client.connect()
        self.client.subscribe(self.subscribe_topic)

    def publish(self, data):
        print(self.publish_topic, data)
        self.client.publish(self.publish_topic, data)

    def check_messages(self):
        self.client.check_msg()

    def sub_callback(self, topic, message):
        message = message.decode('utf-8')
        print(f'New message: {message}')
