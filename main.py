import sys
from Adafruit_IO import MQTTClient
import time, random
from datetime import datetime, time
from process import WaterProcess, Capacity
import scheduler

AIO_USERNAME = "Dat_iot"
AIO_KEY = "aio_VZDo46c1MmWIEhVzEajdlsOjTKZA"
BUTTONS = ["button1", "button2"]
SENSORS = [f"sensor{x}" for x in range(1,3)]


def connected(client):
    print("Connect successfully ...")
    for feed in BUTTONS:
        client.subscribe(feed)

def subscribe(client , userdata , mid , granted_qos):
    print("Subscribe successfully ...")

def disconnected(client):
    print("Disconnected ...")
    sys.exit (1)

def message(client , feed_id , payload):
    print(format(f"Received: feed id: {feed_id} {payload}"))
    # if feed_id == BUTTONS[0]:
    #     if payload == "0":
    #         writeSerial(0)
    #     else:
    #         writeSerial(1)
    # elif feed_id == BUTTONS[1]:
    #     if payload == "0":
    #         writeSerial(0)
    #     else:
    #         writeSerial(1)


client = MQTTClient(AIO_USERNAME , AIO_KEY)
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message
client.on_subscribe = subscribe
client.connect()
client.loop_background()


process_list = [
    WaterProcess(
        mixer=[0, 100, 100], n_mixers=3, area=3,
        start_time=datetime(2024, 7, 9, 12, 40),
        end_time=datetime(2024, 7, 9, 12, 55),
        emergency=0, time_out=datetime(2025, 7, 8, 13),
        priority=1
    ),
    WaterProcess(
        mixer=[200, 150, 100], n_mixers=3, area=3,
        start_time=datetime(2024, 6, 9, 12, 30),
        end_time=datetime(2024, 6, 9, 12, 40),
        emergency=0, time_out=datetime(2024, 6, 7, 13),
        priority=0,
    ),
    WaterProcess(
        mixer=[100, 200, 300], n_mixers=3, area=1,
        start_time=datetime(2024, 6, 9, 9, 30),
        end_time=datetime(2024, 6, 9, 9, 40),
        emergency=0, time_out=datetime(2024, 6, 7, 10),
    ),
    WaterProcess(
        mixer=[200, 0, 200], n_mixers=3, area=2,
        start_time=datetime(2024, 6, 9, 14, 30),
        end_time=datetime(2024, 6, 9, 15, 40),
        emergency=0, time_out=datetime(2024, 6, 7, 16),
        priority=1,
    ),
    WaterProcess(
        mixer=[0, 200, 100], n_mixers=3, area=1,
        start_time=datetime(2024, 6, 9, 14, 41),
        end_time=datetime(2024, 6, 9, 14, 55),
        emergency=0, time_out=datetime(2024, 6, 7, 14, 59),
        priority=0,
    ),
]

complete_process = []

NUM_PROCESS = len(process_list)
TIMESTEP = time(second=20)
CAPACITY = Capacity(mixer=[20, 20, 20], n_mixers=3, time_step=TIMESTEP)
counter = 0

# Start loop
# Sort process list with arrival time
# Select the  highest priority process which has arrived
# End loop if complete all the process
# Update the selected process response time, remaining time
# Update current Time
# Update completion time if remaining time = 0

while True:
    counter -= 1
    # Complete all process
    if not process_list:
        print("All process completed.")
        break
    if counter <= 0:
        # Reset counter
        counter = int(TIMESTEP.second)
        process_list = scheduler.sort_by_time(process_list)
        select_index, select_process = scheduler.select_process(process_list, TIMESTEP, CAPACITY)

        # Terminate process through com port
        MIXER = select_process.mixer    # List of mixer volume. Ex: [20, 10, 15]
        AREA = select_process.area

        # ======= YOUR CODE START HERE =======



        # ======= YOUR CODE END HERE =======

        # Process terminated successfully
        if scheduler.update_process(process_list[select_index], MIXER):
            complete_process.append(process_list.pop(select_index))
        # Update to server
        print("Publish sensor to server ...")
        temp = random.randint(10,100)

    # readSerial(client)
    time.sleep(1)