import sys
import paho.mqtt.client as mqtt


class MQTTHelper:

    MQTT_SERVER = "mqttserver.tk"
    MQTT_PORT = 1883
    MQTT_USERNAME = "innovation"
    MQTT_PASSWORD = "Innovation_RgPQAZoA5N"

    MQTT_TOPIC_SUB_PUMP = "/innovation/pumpcontroller/WSNs"
    MQTT_TOPIC_SUB_VALVE = "/innovation/valvecontroller/WSNs"

    MQTT_TOPIC_PUB_PUMP = "/innovation/pumpcontroller"
    MQTT_TOPIC_PUB_VALVE = "/innovation/valvecontroller"

    payload = ""
    isTx = False

    def __init__(self):
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.username_pw_set(self.MQTT_USERNAME, self.MQTT_PASSWORD)
        self.client.connect(self.MQTT_SERVER, int(self.MQTT_PORT), 60)

        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_subscribe = self.on_subscribed
        self.client.loop_start()

    def subscribe(self, topic):
        self.client.subscribe(topic)

    def publish(self, topic, message):
        self.client.publish(topic, message)

    def on_connect(self, client, userdata, flags, reason_code, properties):
        if reason_code.is_failure:
            print(f"Failed to connect: {reason_code}. loop_forever() will retry connection")
        else:
            print("Connected successfully")
            self.subscribe(self.MQTT_TOPIC_SUB_PUMP)
            self.subscribe(self.MQTT_TOPIC_SUB_VALVE)

    def on_subscribed(self, client, userdata, mid, reason_code_list, properties):
        if reason_code_list[0].is_failure:
            print(f"Broker rejected your subscription: {reason_code_list[0]}")
        else:
            print(f"Broker granted the following QoS: {reason_code_list[0].value}")

    def on_message(self, client, userdata, message):
        # print("Received message " + str(message.payload.decode("utf-8")) + " on topic " + message.topic)
        self.payload = str(message.payload.decode("utf-8"))

    def get_payload(self):
        if self.payload == "":
            return ""
        res = self.payload
        self.payload = ""
        return res
