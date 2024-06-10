from flask import Flask, request, jsonify
from gevent.pywsgi import WSGIServer
from threading import Thread, Lock
from process import WaterProcess, Capacity
import scheduler
import datetime, time

app = Flask(__name__)

TIMESTEP = datetime.time(second=10)
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
    global process_list, complete_process, updated_process
    updated_process = None
    counter = 0
    while True:
        time.sleep(1)
        counter -= 1
        # All process completed
        # scheduler.print_process_list(process_list)
        if not process_list:
            print("All process completed.")
            break
        if counter <= 0:
            # Reset counter
            counter = int(TIMESTEP.second)
            # process_list = scheduler.sort_by_time(process_list)
            select_index, select_process = scheduler.select_process(process_list, TIMESTEP, CAPACITY)
            if not select_process:
                print("No process selected.")
                continue

            # Terminate process through com port
            MIXER = select_process.mixer  # List of mixer volume. Ex: [20, 10, 15]
            AREA = select_process.area

            # ======= YOUR CODE START HERE =======

            # ======= YOUR CODE END HERE =======

            # Process terminated successfully
            updated_process = process_list[select_index]
            if scheduler.update_process(process_list[select_index], MIXER):
                complete_process.append(process_list.pop(select_index))
            print("___________________\nComplete process: ", len(complete_process))
            # Update to client


@app.route('/add_process', methods=['POST'])
def add_process():
    data = request.get_json()
    # return jsonify(data)

    global process_list

    # Remove process with the same id in queue.
    _, prev_process = find_process(process_list, data["id"])
    if prev_process:
        process_list.remove(prev_process)
    process = WaterProcess(
        id=data["id"],
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
    return str(process)

@app.route('/update_process', methods=['POST'])
def update_process():
    data = request.get_json()
    global process_list
    _, process = find_process(process_list, data["id"])
    assert process, "Process not found."
    for key, value in data.items():
        if key == "start_time" or key == "end_time":
            setattr(process, key, datetime.datetime.strptime(value, TIME_FORMAT))
        elif key == "emergency":
            setattr(process, "priority", 0 if value else 1)
        else:
            setattr(process, key, value)
    scheduler.print_process_list(process_list)
    return str(process)

@app.route('/delete_process', methods=['POST'])
def delete_process():
    data = request.get_json()
    global process_list
    print(data["id"])
    index, _ = find_process(process_list, data["id"])
    assert index is not None, "Process not found."
    process_list.pop(index)
    scheduler.print_process_list(process_list)
    return "Process deleted."

@app.route('/process_data', methods=["GET"])
def send_process_data():
    global updated_process
    if updated_process:
        return jsonify(updated_process.__dict__(TIME_FORMAT))
    return jsonify({})

@app.route('/process_list', methods=["GET"])
def send_process_list():
    global process_list
    return jsonify([process.__dict__(TIME_FORMAT) for process in process_list])

@app.route('/complete_process_list', methods=["GET"])
def send_complete_list():
    global complete_process
    return jsonify([process.__dict__(TIME_FORMAT) for process in complete_process])

def get_cycle(ctx: list[WaterProcess], area):
    cycle = 0
    for process in ctx:
        if process.area == area:
            cycle += 1
    return cycle + 1

def find_process(ctx: list[WaterProcess], id):
    for i in range(len(ctx)):
        if ctx[i].id == id:
            return i, ctx[i]
    return None, None


if __name__ == '__main__':
    thread = Thread(target=background_task)
    thread.start()
    # Debug/Development
    # app.run(debug=True, host="0.0.0.0", port="5000")
    # Production
    http_server = WSGIServer(("127.0.0.1", 8000), app)
    http_server.serve_forever()

