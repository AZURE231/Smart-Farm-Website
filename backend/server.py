from flask import Flask, request, jsonify
from gevent.pywsgi import WSGIServer
from threading import Thread, Lock
from process import WaterProcess, Capacity
import scheduler
import datetime, time

app = Flask(__name__)

TIMESTEP = datetime.time(second=1)
TIME_FORMAT = "%d/%m/%Y %H:%M:%S"
NUM_MIXERS = 3
CAPACITY = Capacity(mixer=[20, 20, 20], n_mixers=NUM_MIXERS, time_step=TIMESTEP)

# process_list = []
process_list = [
    WaterProcess(
        id=1,
        mixer=[0, 100, 100], n_mixers=3, area=3,
        start_time=datetime.datetime(2024, 6, 9, 12, 40),
        end_time=datetime.datetime(2024, 6, 9, 12, 55),
        priority=1, cycle=2
    ),
    WaterProcess(
        id=2,
        mixer=[200, 150, 100], n_mixers=3, area=3,
        start_time=datetime.datetime(2024, 6, 9, 12, 30),
        end_time=datetime.datetime(2024, 6, 9, 12, 40),
        priority=0, cycle=1
    ),
    WaterProcess(
        id=3,
        mixer=[100, 200, 300], n_mixers=3, area=1,
        start_time=datetime.datetime(2024, 6, 9, 9, 30),
        end_time=datetime.datetime(2024, 6, 9, 9, 40),
        cycle=1
    ),
    WaterProcess(
        id=4,
        mixer=[200, 0, 200], n_mixers=3, area=2,
        start_time=datetime.datetime(2024, 6, 9, 14, 30),
        end_time=datetime.datetime(2024, 6, 9, 15, 40),
        priority=1, cycle=1
    ),
    WaterProcess(
        id=5,
        mixer=[0, 200, 100], n_mixers=3, area=1,
        start_time=datetime.datetime(2024, 6, 9, 14, 41),
        end_time=datetime.datetime(2024, 6, 9, 14, 55),
        priority=0, cycle=2
    ),
]
complete_process = []

# updated_process = None
updated_process = WaterProcess(
    id=1,
    start_time=datetime.datetime.now(),
    end_time=datetime.datetime.now(),
    mixer=[100, 200, 300],
    area=1,
    priority=1,
    isActive=False,
    cycle=0
)


def background_task():
    """
    Background task to schedule, terminate and update process.
    :return:
    """
    global process_list, complete_process, updated_process
    select_index, select_process = None, None
    counter = 0
    all_complete = False
    while True:
        time.sleep(1)
        counter -= 1
        # All process completed
        # scheduler.print_process_list(process_list)
        if counter <= 0:
            # Reset counter
            counter = int(TIMESTEP.second)
            if not process_list:
                if not all_complete:
                    print("All process completed.")
                    all_complete = True
                continue
            # Update process in previous step
            if select_process:
                updated_process = process_list[select_index]
                # Process terminated successfully
                if scheduler.update_process(process_list[select_index], select_process.mixer):
                    complete_process.append(process_list.pop(select_index))
                print("___________________\nComplete process: ", len(complete_process))
            # Update to client
            all_complete = False
            process_list = scheduler.sort_by_time(process_list)
            select_index, select_process = scheduler.select_process(process_list, TIMESTEP, CAPACITY)
            if not select_process:
                print("No process selected.")
                continue

            # Terminate process through com port
            MIXER = select_process.mixer  # List of mixer volume. Ex: [20, 10, 15]
            AREA = select_process.area

            # ======= YOUR CODE START HERE =======

            # ======= YOUR CODE END HERE =======



@app.route('/add_process', methods=['POST'])
def add_process():
    """
    REST API to add a new process from client via POST to the process list.
    :return:    str, the new process.
    """
    data = request.get_json()
    # return jsonify(data)

    global process_list, complete_process

    # Remove process with the same id in queue.
    process = WaterProcess(
        id=get_new_id(process_list + complete_process),
        start_time=datetime.datetime.strptime(data["start_time"], TIME_FORMAT),
        end_time=datetime.datetime.strptime(data["end_time"], TIME_FORMAT),
        mixer=data["mixer"],
        n_mixers=NUM_MIXERS,
        area=data["area"],
        priority=0 if data["emergency"] else 1,
        cycle=get_cycle(process_list, data["area"]),
    )
    process_list.append(process)
    scheduler.print_process_list(process_list)
    return jsonify(process.__dict__(TIME_FORMAT))

@app.route('/update_process', methods=['POST'])
def update_process():
    """
    REST API to update process from client via POST.
    :return:    str, the updated process.
    """
    data = request.get_json()
    global process_list, complete_process
    # If single update, convert to list
    if not isinstance(data, list):
        data = [data]
    updated_process_list = []
    for item in data:
        complete_index, process = find_process(complete_process, item["id"])
        if complete_index is None:
            _, process = find_process(process_list, item["id"])
        assert process, "Process not found."
        prev_area = process.area
        for key, value in item.items():
            if key == "start_time" or key == "end_time":
                setattr(process, key, datetime.datetime.strptime(value, TIME_FORMAT))
            elif key == "emergency":
                setattr(process, "priority", 0 if value else 1)
            else:
                setattr(process, key, value)

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
    scheduler.print_process_list(process_list)
    return jsonify([process.__dict__() for process in updated_process_list])

@app.route('/delete_process', methods=['POST'])
def delete_process():
    """
    REST API to delete process from client via POST.
    :return:    str, notify the process is deleted.
    """
    data = request.get_json()
    global process_list, complete_process
    index, _ = find_process(complete_process, data["id"])
    if index is not None:
        del complete_process[index]
        return jsonify({"deleted": True})
    else:
        index, _ = find_process(process_list, data["id"])
        if index is None:
            return jsonify({"deleted": False})
        del process_list[index]
    scheduler.print_process_list(process_list)
    return jsonify({"deleted": True})

@app.route('/process_data', methods=["GET"])
def send_process_data():
    """
    REST API to send the updated process data via GET.
    :return:    JSON, the updated process data.
    """
    global updated_process
    if updated_process:
        return jsonify(updated_process.__dict__(TIME_FORMAT))
    return jsonify({})

@app.route('/process_list', methods=["GET"])
def send_process_list():
    """
    REST API to send the process queue via GET.
    :return:    JSON, the process queue.
    """
    global process_list
    return jsonify([get_area_dict(process_list, area) for area in range(1, 4)])

@app.route('/completed_process_list', methods=["GET"])
def send_completed_list():
    """
    REST API to send the completed process list via GET.
    :return:    JSON, the completed process list.
    """
    global complete_process
    return jsonify([get_area_dict(complete_process, area) for area in range(1, 4)])

@app.route('/all_process', methods=["GET"])
def send_all_process():
    """
    REST API to send all process data via GET.
    :return:    JSON, all process data.
    """
    global process_list, complete_process
    return jsonify([get_area_dict(process_list + complete_process, area) for area in range(1, 4)]
    )

def get_cycle(ctx: list[WaterProcess], area):
    cycle = 0
    for process in ctx:
        if process.area == area:
            cycle += 1
    return cycle + 1

def get_area_dict(ctx: list[WaterProcess], area):
    area_dict = {}
    area_dict["area"] = area
    area_dict["process"] = [process.__dict__(TIME_FORMAT) for process in ctx if process.area == area]
    return area_dict

def find_process(ctx: list[WaterProcess], id):
    for i in range(len(ctx)):
        if ctx[i].id == id:
            return i, ctx[i]
    return None, None

def get_new_id(ctx: [WaterProcess]):
    if not ctx:
        return 1
    return max([process.id for process in ctx]) + 1

if __name__ == '__main__':
    thread = Thread(target=background_task)
    thread.start()
    # Debug/Development
    # app.run(debug=True, host="0.0.0.0", port="5000")
    # Production
    http_server = WSGIServer(("127.0.0.1", 8000), app)
    http_server.serve_forever()

