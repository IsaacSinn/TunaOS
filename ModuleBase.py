import time
from threading import Thread
from threading import Event

class Interval:
    def __init__(self, interval, action) :
        self.__interval = interval
        self.__action = action
        self.__stopEvent = False
        self.thread = Thread(target = self.__setInterval)
        self.thread.start()

    def __setInterval(self):
        while 1:
            self.__action()
            time.sleep(self.__interval)

            if self.__stopEvent:
                break

    def stopThread(self):
        self.__stopEvent = True
        self.thread.join()
        print("Thread Killed")



class Module:
    def run(self):
        pass

    def start(self, freq = 1):
        self.__interval = 1 / freq
        self.__thread = Interval(self.__interval, self.run)

    def stop(self):
        self.__thread.stopThread()
