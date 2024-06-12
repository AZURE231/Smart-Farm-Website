import signal, sys
from threading import Thread, Lock, Event
from process import WaterProcess, Capacity
import scheduler
import datetime, time
from mqttPi import MQTTHelper
from device import Devices
import json


mqttClient = MQTTHelper()
devices = Devices()
stop_event = Event()


TIMESTEP = datetime.time(second=1)
PUBLISH_TIME = datetime.time(second=10)
TIME_FORMAT = "%d/%m/%Y %H:%M:%S"
NUM_MIXERS = 3
CAPACITY = Capacity(mixer=[20, 20, 20], n_mixers=NUM_MIXERS, time_step=TIMESTEP)

# process_list = []
process_list = [
    WaterProcess(
        id=1,
        mixer=[0, 100, 100],
        n_mixers=3,
        area=3,
        start_time=datetime.datetime.combine(datetime.date.today(), datetime.time(12, 30)),
        end_time=datetime.datetime.combine(datetime.date.today(), datetime.time(12, 40)),
        priority=1,
        cycle=2,
    ),
    WaterProcess(
        id=2,
        mixer=[210, 150, 110],
        n_mixers=3,
        area=3,
        start_time=datetime.datetime.combine(datetime.date.today(), datetime.time(12, 40)),
        end_time=datetime.datetime.combine(datetime.date.today(), datetime.time(12, 50)),
        priority=0,
        cycle=1,
    ),
    WaterProcess(
        id=3,
        mixer=[100, 200, 300],
        n_mixers=3,
        area=1,
        start_time=datetime.datetime.combine(datetime.date.today(), datetime.time(9, 30)),
        end_time=datetime.datetime.combine(datetime.date.today(), datetime.time(9, 40)),
        cycle=1,
    ),
    WaterProcess(
        id=4,
        mixer=[200, 0, 200],
        n_mixers=3,
        area=2,
        start_time=datetime.datetime.combine(datetime.date.today(), datetime.time(15, 30)),
        end_time=datetime.datetime.combine(datetime.date.today(), datetime.time(15, 40)),
        priority=1,
        cycle=1,
    ),
    WaterProcess(
        id=5,
        mixer=[0, 200, 100],
        n_mixers=3,
        area=1,
        start_time=datetime.datetime.combine(datetime.date.today(), datetime.time(14, 41)),
        end_time=datetime.datetime.combine(datetime.date.today(), datetime.time(14, 51)),
        priority=0,
        cycle=2,
    ),
]
complete_process = []

to_update_process = None
# to_update_process = WaterProcess(
#     id=1,
#     start_time=datetime.datetime.now(),
#     end_time=datetime.datetime.now(),
#     mixer=[100, 200, 300],
#     area=1,
#     priority=1,
#     isActive=False,
#     cycle=0,
# )


def background_task():
    """
    Background task to schedule, terminate and update process.
    :return:
    """
    global process_list, complete_process, to_update_process
    select_index, select_process = None, None
    counter = 0
    all_complete, stop_publish = False, False
    global MIXER
    MIXER = [0, 0, 0]
    while not stop_event.is_set():
        time.sleep(1)
        counter -= 1
        # Reset counter
        if counter <= 0:
            counter = 60
        # Send update request to Web View
        if counter % int(PUBLISH_TIME.second) == 0 and not stop_publish:
            publish_result = send_all_process()
            if publish_result.rc == mqttClient.MQTT_ERR_SUCCESS:
                print("Process published.")
            else:
                print("Failed to publish the process.")
            if all_complete:
                stop_publish = True

        # Schedule process
        if counter % int(TIMESTEP.second) == 0:
            if not process_list:
                if not all_complete:
                    print("All process completed.")
                    all_complete = True
                continue
            # Update process in previous step
            if select_process and to_update_process:
                # Process terminated successfully
                if scheduler.update_process(to_update_process, select_process.mixer):
                    complete_process.append(to_update_process)
                    process_list.remove(to_update_process)
                    print("___________________\nComplete process: ", len(complete_process))
            # Select process for the next step
            all_complete, stop_publish = False, False
            process_list = scheduler.sort_by_time(process_list)
            select_index, select_process = scheduler.select_process(process_list, TIMESTEP, CAPACITY)
            if not select_process:
                # scheduler.print_process_list(process_list)
                print("No process selected.")
                MIXER = [0, 0, 0]
                continue

            # Terminate process through com port
            to_update_process = process_list[select_index]
            MIXER = select_process.mixer  # List of mixer volume. Ex: [20, 10, 15]
            AREA = select_process.area


def logic():
    while not stop_event.is_set():
        message = mqttClient.get_payload()
        if message != "":
            data = json.loads(message)
            add_process(data)
            send_all_process()


def control():
    while not stop_event.is_set():
        devices.controlDevices(MIXER)


def add_process(data):
    """
    REST API to add a new process from client via POST to the process list.
    :return:    str, the new process.
    """
    global process_list, complete_process
    # Remove process with the same id in queue.
    process = WaterProcess(
        id=get_new_id(process_list + complete_process),
        start_time=datetime.datetime.strptime(data["start_time"], TIME_FORMAT),
        end_time=datetime.datetime.strptime(data["end_time"], TIME_FORMAT),
        mixer=[int(item) for item in data["mixer"]],
        n_mixers=NUM_MIXERS,
        area=int(data["area"]),
        priority=0 if data["emergency"] else 1,
        cycle=get_cycle(process_list, data["area"]),
    )
    process_list.append(process)
    scheduler.print_process_list(process_list)


def update_process(data):
    """
    REST API to update process from client via POST.
    :return:    str, the updated process.
    """
    global process_list, complete_process
    # If single update, convert to list
    if not isinstance(data, list):
        data = [data]
    updated_process_list = []
    for item in data:
        process_id = int(item["id"])
        complete_index, process = find_process(complete_process, process_id)
        if complete_index is None:
            _, process = find_process(process_list, process_id)
        assert process, "Process not found."
        prev_area = process.area
        for key, value in item.items():
            if key == "start_time" or key == "end_time":
                setattr(process, key, datetime.datetime.strptime(value, TIME_FORMAT))
            elif key == "emergency":
                setattr(process, "priority", 0 if value else 1)
            elif key == "mixer":
                setattr(process, key, [int(item) for item in value])
            else:
                # Area
                setattr(process, key, int(value))

        if complete_index is not None:
            # Update process
            if not scheduler.update_process(process, [0 for _ in range(NUM_MIXERS)]):
                complete_process.pop(complete_index)
                process_list.append(process)
            elif datetime.datetime.now() < process.end_time or process.area != prev_area:
                process.mixer = process.defined_mixer
                complete_process.pop(complete_index)
                process_list.append(process)
        updated_process_list.append(process)
    scheduler.print_process_list(updated_process_list)


def delete_process(data):
    """
    REST API to delete process from client via POST.
    :return:    str, notify the process is deleted.
    """
    global process_list, complete_process
    process_id = int(data["id"])
    index, _ = find_process(complete_process, process_id)
    if index is not None:
        del complete_process[index]
        print("Completed process deleted.")
        return
    else:
        index, _ = find_process(process_list, process_id)
        if index is None:
            print("No process to delete.")
        del process_list[index]
        print("Process deleted.")


def send_process_data():
    """
    REST API to send the updated process data via GET.
    """
    global to_update_process
    if to_update_process:
        return mqttClient.publish(mqttClient.MQTT_TOPIC_WEB_UPDATE, json.dumps(to_update_process.__dict__(TIME_FORMAT)))
    return mqttClient.publish(mqttClient.MQTT_TOPIC_WEB_UPDATE, json.dumps({}))


def send_process_list():
    """
    REST API to send the process queue via GET.
    """
    global complete_process
    process_dict = [get_area_dict(process_list, area) for area in range(1, NUM_MIXERS + 1)]
    return mqttClient.publish(mqttClient.MQTT_TOPIC_WEB_UPDATE, json.dumps(process_dict))


def send_completed_list():
    """
    REST API to send the completed process list via GET.
    """
    global complete_process
    process_dict = [get_area_dict(complete_process, area) for area in range(1, NUM_MIXERS + 1)]
    return mqttClient.publish(mqttClient.MQTT_TOPIC_WEB_UPDATE, json.dumps(process_dict))


def send_all_process():
    """
    REST API to send all process data via GET.
    """
    global process_list, complete_process
    process_dict = [get_area_dict(process_list + complete_process, area) for area in range(1, NUM_MIXERS + 1)]
    return mqttClient.publish(mqttClient.MQTT_TOPIC_WEB_UPDATE, json.dumps(process_dict))


def get_cycle(ctx: list[WaterProcess], area):
    cycle = 0
    for process in ctx:
        if process.area == int(area):
            cycle += 1
    return cycle + 1


def get_area_dict(ctx: list[WaterProcess], area):
    area_dict = {}
    area_dict["area"] = int(area)
    area_dict["process"] = [process.__dict__(TIME_FORMAT) for process in ctx if process.area == int(area)]
    return area_dict


def find_process(ctx: list[WaterProcess], id):
    for i in range(len(ctx)):
        if ctx[i].id == int(id):
            return i, ctx[i]
    return None, None


def get_new_id(ctx: [WaterProcess]):
    if not ctx:
        return 1
    return max([process.id for process in ctx]) + 1


def signal_handler(sig, frame):
    print("Received SIGINT (Ctrl+C). Stopping the threads...")
    stop_event.set()


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)

    thread1 = Thread(target=background_task)
    thread2 = Thread(target=logic)
    thread3 = Thread(target=control)
    thread1.start()
    thread2.start()
    thread3.start()

    try:
        # Keep the main thread running, waiting for Ctrl+C
        while not stop_event.is_set():
            time.sleep(0.1)
    except KeyboardInterrupt:
        pass

    # Wait for the threads to finish
    thread1.join()
    thread2.join()
    thread3.join()

    print("Threads have stopped.")
    print("Main program is exiting.")
    sys.exit(0)
    # Debug/Development
    # app.run(debug=True, host="0.0.0.0", port="5000")
    # Production
    # http_server = WSGIServer(("127.0.0.1", 8000), app)
    # http_server.serve_forever()
