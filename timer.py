import time


class Timer:
    timeout_interval = 0
    running = False
    start_time = 0

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
