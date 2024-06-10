from abc import ABC
import datetime


class Capacity():
     def __init__(self, mixer: list[float] = [20,20,20], n_mixers: int = 3, time_step = datetime.time(second=20), perMinute: bool = False):
         self.mixer = mixer
         self.time_step = time_step
         if perMinute:
             self.mixer = list(map(lambda x: x / 60 * time_step.second, mixer))
         self.n_mixers = n_mixers
         assert len(mixer) == n_mixers, f"Mixer should have {self.n_mixers} items."


class Process(ABC): pass

class StepProcess(Process):
    def __init__(self, area: int, mixer: list[float], n_mixers: int = 3):
        """

        :param area:        int
                            Area where the process is watering.
        :param mixer:       List of Volume of liquid in a single time step from Mixer 1..3 in ml.
        """
        self.area = area
        self.mixer = mixer
        self.n_mixers = n_mixers
        assert len(mixer) == n_mixers, f"Mixer should have {self.n_mixers} items."

    def __str__(self):
        s = "________________________\n" +\
            f"Area: {self.area}\n"
        for i in range(self.n_mixers):
            s += f"Mixer {i+1}: {self.mixer[i]}\n"
        return s

class WaterProcess(Process):
    def __init__(self, id: int, start_time, end_time, area: int,
                 mixer: list[float], n_mixers: int = 3, priority: int = 1,
                 isActive: bool = False, cycle: int = 0):
        """
        :param id:          int
                            Unique identifier of the process.
        :param start_time:  datetime.datetime
                            Expected time the process should start.
        :param end_time:    datetime.datetime
                            Expected time the process should stop.
        :param time_step:   datetime.time
                            The amount of time which the process is divided into
                            steps.
        :param area:        int
                            Area where the process is watering.
        :param mixer:       List of Volume of liquid from Mixer 1..3 in ml.
        :param date:        Date on which the process defined.
        :param priority:    Priority to complete the process.
        :param isActive:    State of the process. If True, the process is running.
        :param cycle:       int
                            The n-th time of watering a specified area in the day.
        """
        self.id = id
        self.priority = priority
        self.mixer = mixer
        self.n_mixers = n_mixers
        assert len(mixer) == n_mixers, f"Mixer should have {self.n_mixers} items."
        self.area = area
        self.start_time = start_time
        self.end_time = end_time
        self.isActive = isActive
        self.cycle = cycle


    def time_step_divide(self, time_step = datetime.time(second=20), capacity: Capacity = None):
        """
        Divide the process into time steps.
        :return:    StepProcess with scaled mixers' volume with capacity.
        """
        if capacity:
            max_ratio = 0
            max_index = -1
            mixer_ratio = [self.mixer[i]/capacity.mixer[i] for i in range(self.n_mixers)]
            for i in range(self.n_mixers):
                if mixer_ratio[i] > max_ratio:
                    max_ratio = mixer_ratio[i]
                    max_index = i
            mixer = []
            for i in range(self.n_mixers):
                if i == max_index:
                    mixer.append(capacity.mixer[i])
                else:
                    mixer.append(capacity.mixer[max_index] * self.mixer[i] / self.mixer[max_index])
            return StepProcess(area=self.area, mixer=mixer, n_mixers=self.n_mixers)

        time_ratio = (self.end_time - self.start_time).total_seconds() / time_step.second
        mixer = list(map(lambda x: x/time_ratio, self.mixer))
        return StepProcess(area=self.area, mixer=mixer, n_mixers=self.n_mixers)


    def remain_time(self):
        return self.end_time - datetime.datetime.now()

    def update(self, mixer: list[float]):
        assert len(mixer) == self.n_mixers, f"Mixer should have {self.n_mixers} items."
        self.mixer = list(map(lambda curr, step: curr - step, self.mixer, mixer))



    def __str__(self):
        s = "________________________\nWatering Process:\n" + \
            f"ID: {self.id}\n" \
            f"Priority: {self.priority}\n" \
            f"Start time: {str(self.start_time)}\n" \
            f"End time: {str(self.end_time)}\n" \
            f"isActive: {self.isActive}\n" \
            f"Area: {self.area}\n"
        for i in range(self.n_mixers):
            s += f"Mixer {i+1}: {self.mixer[i]}\n"
        s += f"Cycle: {self.cycle}\n"
        return s

    def __lt__(self, other):
        return self.start_time < other.start_time

    def __dict__(self, time_format="%d/%m/%Y %H:%M:%S"):
        return {
            "id": self.id,
            "start_time": self.start_time.strftime(time_format),
            "end_time": self.end_time.strftime(time_format),
            "isActive": self.isActive,
            "area": self.area,
            "mixer": self.mixer,
            "cycle": self.cycle
        }