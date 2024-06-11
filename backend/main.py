import sys
import datetime
import time
import random
from mqtt import MQTTHelper
from process import WaterProcess, Capacity
import scheduler
from device import Devices

mqttClient = MQTTHelper()

process_list = [
    WaterProcess(
        id=1,
        mixer=[0, 100, 100], n_mixers=3, area=3,
        start_time=datetime.datetime(2024, 6, 9, 12, 40),
        end_time=datetime.datetime(2024, 6, 9, 12, 55),
        priority=1
    ),
    WaterProcess(
        id=2,
        mixer=[200, 150, 100], n_mixers=3, area=3,
        start_time=datetime.datetime(2024, 6, 9, 12, 30),
        end_time=datetime.datetime(2024, 6, 9, 12, 40),
        priority=0,
    ),
    WaterProcess(
        id=3,
        mixer=[100, 200, 300], n_mixers=3, area=1,
        start_time=datetime.datetime(2024, 6, 9, 9, 30),
        end_time=datetime.datetime(2024, 6, 9, 9, 40),
    ),
    WaterProcess(
        id=4,
        mixer=[200, 0, 200], n_mixers=3, area=2,
        start_time=datetime.datetime(2024, 6, 9, 14, 30),
        end_time=datetime.datetime(2024, 6, 9, 15, 40),
        priority=1,
    ),
    WaterProcess(
        id=5,
        mixer=[0, 200, 100], n_mixers=3, area=1,
        start_time=datetime.datetime(2024, 6, 9, 14, 41),
        end_time=datetime.datetime(2024, 6, 9, 14, 55),
        priority=0,
    ),
]

complete_process = []

TIMESTEP = datetime.time(second=1)
CAPACITY = Capacity(mixer=[20, 20, 20], n_mixers=3, time_step=TIMESTEP)
counter = 0
all_complete = False

# Start loop
# Sort process list with arrival time
# Select the highest priority process which has arrived
# End loop if complete all the process
# Update the selected process response time, remaining time
# Update current Time
# Update completion time if remaining time = 0

devices = Devices()

while True:
    time.sleep(1)
    counter -= 1
    # Complete all process
    if not process_list and not all_complete:
        print("All process completed.")
        all_complete = True
    else:
        all_complete = False
    if counter <= 0:
        # Reset counter
        counter = int(TIMESTEP.second)
        process_list = scheduler.sort_by_time(process_list)
        select_index, select_process = scheduler.select_process(process_list, TIMESTEP, CAPACITY)
        if not select_process:
            print("No process selected.")
            continue

        # Terminate process through com port
        MIXER = select_process.mixer    # List of mixer volume. Ex: [20, 10, 15]
        AREA = select_process.area

        # ======= YOUR CODE START HERE =======


        # ======= YOUR CODE END HERE =======

        # Process terminated successfully
        if scheduler.update_process(process_list[select_index], MIXER):
            complete_process.append(process_list.pop(select_index))
        print("___________________\nComplete process: ", len(complete_process))
        # Update to server
        # print("Publish sensor to server ...")
        # temp = random.randint(10,100)



# readSerial(client)
