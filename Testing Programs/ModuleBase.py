import time
from threading import Thread
from threading import Event

class Interval :
    def __init__(self, interval, action) :
        self.__interval = interval
        self.__action = action
        self.__stopEvent = Event()
        thread = Thread(target = self.__setInterval)
        thread.start()

    def __setInterval(self) :
        while True:
            self.__action()
            time.sleep(self.__interval)

        self.__action()

    def __cancel(self) :
        self.__stopEvent.set()

class Module:
    def __init__(self):
        self.__running = False
        pass

    def run(self):
        pass

    def start(self, freq=1):
        self.__running = True
        self.__interval = 1/freq
        self.__thread = Interval(self.__interval, self.run)

    def stop(self):
        if self.__running:
            self.__thread.__cancel()
        self.__running = False
