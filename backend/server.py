from flask import Flask, request

from process import WaterProcess, Capacity
import scheduler
import datetime

app = Flask(__name__)

process_list = []
TIME_FORMAT = "%d/%m/%Y %H:%M:%S"


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
        n_mixers=len(data["mixer"]),
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
    app.run(debug=True)

