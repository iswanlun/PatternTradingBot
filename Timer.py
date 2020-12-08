import threading, time

class RepeatTimer:

    def __init__(self, period) -> None:
        self.period = period
        self.thread = None

    def worker(self, target):
        while self.running:
            time.sleep(self.period)
            target.event()

    def start(self, target):
        self.running = True
        self.thread = threading.Thread(target=self.worker, args=(target,))
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.join()
    