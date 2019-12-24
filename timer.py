import time


class Timer:
    """Assigns the timer to a package

    Attributes:
        timeout_interval : float
            sets the time to check if the packet is lost
        running : bool
        start_time : float
    """
    timeout_interval: float
    start_time: float
    running = False

    def __init__(self, timeout_interval):
        self.timeout_interval = timeout_interval

    def start(self):
        self.running = True
        self.start_time = time.time()

    def stop(self):
        self.running = False

    def is_running(self):
        return self.running

    def time_out(self):
        return time.time() - self.start_time > self.timeout_interval
