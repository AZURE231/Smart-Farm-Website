import sys
import paho.mqtt.client as mqtt

json_pump = "{'station_id':'pump_station_0001','station_name':'Irrigation Station','sensors':[{'id':'pump_0001','value':'0'},{'id':'pump_0002','value':'0'},{'id':'pump_0003','value':'0'},{'id':'pump_0004','value':'0'},{'id':'pump_0005','value':'0'}]}"
json_valve = "{'station_id':'valve_station_0001','station_name':'Mix Nutrition','sensors':[{'id':'valve_0001','value':'0'},{'id':'valve_0002','value':'0'},{'id':'valve_0003','value':'0'}]}"


class MQTTHelper:

    MQTT_SERVER = "mqttserver.tk"
    MQTT_PORT = 1883
    MQTT_USERNAME = "innovation"
    MQTT_PASSWORD = "Innovation_RgPQAZoA5N"

    MQTT_TOPIC_SUB_PUMP = "/innovation/pumpcontroller/WSNs"
    MQTT_TOPIC_SUB_VALVE = "/innovation/valvecontroller/WSNs"

    MQTT_TOPIC_PUB_PUMP = "/innovation/pumpcontroller"
    MQTT_TOPIC_PUB_VALVE = "/innovation/valvecontroller"

    def __init__(self):
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        # self.client = mqtt.Client()
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

    def on_connect(self, client, userdata, flags, reason_code):
        print(f"Connect with reason code: {str(reason_code)}")
        client.subscribe(self.MQTT_TOPIC_SUB_PUMP)
        client.subscribe(self.MQTT_TOPIC_SUB_VALVE)

    def on_subscribed(self, client, userdata, mid, rc_list):
        print(f"Broker granted the following QoS: 0")

    def on_message(self, client, userdata, message):
        print("Received message " + str(message.payload.decode("utf-8")) + " on topic " + message.topic)
