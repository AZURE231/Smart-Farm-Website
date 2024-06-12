from datetime import datetime, time
from process import WaterProcess, Capacity
import heapq
import sys


def sort_by_time(process_list: list[WaterProcess]):
    # Sort the list with start time
    n_process = len(process_list)
    heapq.heapify(process_list)
    return [heapq.heappop(process_list) for i in range(n_process)]

def select_process(process_list: list[WaterProcess], time_step: time, capacity: Capacity):
    """
    Select the  highest priority process which has arrived, return the step process from the selected process.
    :param process_list:    list of WaterProcess, sorted by start time.
    :param time_step:       time duration for each step.
    :param capacity:        Capacity of the system for mixers in each step.
    :return:                Tuple(index of the selected process, StepProcess)
    """
    num_process = len(process_list)
    highest_priority = sys.maxsize
    highest_priority_index = None
    current_time = datetime.now()
    for index in range(num_process):
        # Arrival process
        if process_list[index].start_time < current_time:
            if process_list[index].priority < highest_priority:
                highest_priority = process_list[index].priority
                highest_priority_index = index

    if highest_priority_index is None:
        return None, None
    print("===========================\nSelected process:")
    process_list[highest_priority_index].isActive = True
    # print(str(process_list[highest_priority_index]))
    return highest_priority_index, process_list[highest_priority_index].time_step_divide(time_step, capacity)

def update_process(process: WaterProcess, mixer: list[float]):
    """
    Update process after terminate.
    :param process: WaterProcess
    :param mixer:   list of float, the mixer volume after the process.
    :return:        bool, True if the process is completed.
    """
    assert len(process.mixer) == len(mixer), f"Mixer should have {process.n_mixers} items."
    process.update(mixer)
    process.isActive = False
    print("===========================\nUpdated process:")
    print(str(process))
    for item in process.mixer:
        if item > 0:
            return False
        else:
            item = 0
    process.isCompleted = True
    return True


def print_process_list(process_list: list[WaterProcess]):
    print("===========================\nProcess list:")
    for process in process_list:
        print(str(process))

##### Further develop: Deploy DBMS.
