from abc import ABC
import datetime


class Process(ABC): pass

class WateringProcess(Process):
    def __init__(self, priority, mixer1, mixer2, mixer3, area: int, start_time, end_time, emergency, time_out, isActive: bool = False, cycle: int = 0):
        """

        :param priority:    Priority to complete the process.
        :param mixer1:      Volume of liquid from Mixer 1 in ml.
        :param mixer2:      Volume of liquid from Mixer 2 in ml.
        :param mixer3:      Volume of liquid from Mixer 3 in ml.
        :param area:        int
                            Area where the process is watering.
        :param start_time:  datetime.datetime
                            Expected time the process should start.
        :param end_time:    datetime.datetime
                            Expected time the process should stop.
        # :param date:        Date on which the process defined.
        :param emergency:   Exception from system/ environment/ users.
        :param time_out:
        :param isActive:    State of the process. If True, the process is running.
        :param cycle:       int
                            The n-th time of watering a specified area in the day.
        """
        # self.priority = priority
        self.mixer1 = mixer1
        self.mixer2 = mixer2
        self.mixer3 = mixer3
        self.area = area
        self.start_time = start_time
        self.end_time = end_time
        # self.date = date
        self.emergency = emergency
        self.time_out = time_out
        self.isActive = isActive
        self.cycle = cycle

    def remain_time(self):
        return self.end_time - datetime.datetime.now()

    def __str__(self):
        s = f"Start time: {str(self.start_time)}" \
            f"End time: {str(self.end_time)}" \
            f"isActive: {self.isActive}" \
            f"Area: {self.area}" \
            f"Cycle: {self.cycle}" \
            f"Mixer 1: {self.mixer1}" \
            f"Mixer 2: {self.mixer2}" \
            f"Mixer 3: {self.mixer3}" \
            f"Timeout: {str(self.time_out)}" \
            f"Emergency: {str(self.emergency)}"
        return s
