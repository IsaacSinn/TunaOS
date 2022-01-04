import time
from threading import Thread
from threading import Event

class Interval:
    def __init__(self, interval, action, single) :
        self.__interval = interval
        self.__action = action
        self.__single = single
        self.__stopEvent = False
        self.thread = Thread(target = self.__setInterval)
        self.thread.start()

    def __setInterval(self):
        self.__single()
        while 1:
            self.__action()
            time.sleep(self.__interval)

            if self.__stopEvent:
                break

    def stopThread(self):
        self.__stopEvent = True
        self.thread.join()

class Module:
    def run(self):
        pass

    def run_once_in_thread(self):
        pass

    def start(self, freq = 1):
        self.__interval = 1 / freq
        self.__thread = Interval(self.__interval, self.run, self.run_once_in_thread)

    def stop(self):
        self.__thread.stopThread()

class ModuleManager():

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ModuleManager, cls).__new__(cls)
            cls.modules = []
            cls.modules_name = []
            cls.modules_freq = []
            cls.ID = 0
        return cls.instance

    @classmethod
    def register(cls, *args):
        for module_info in args:
            cls.modules_freq.append(module_info[1])
            cls.modules_name.append(type(module_info[0]).__name__)
            cls.modules.append(module_info[0])

    @classmethod
    def get_registered_modules(cls):
        return cls.modules_name

    @classmethod
    def start_all(cls):
        for index, module in enumerate(cls.modules):
            module_freq = cls.modules_freq[index]
            module_name = cls.modules_name[index]

            module.start(module_freq)
            print(f"{module_name} started")


    @classmethod
    def stop_all(cls):
        for index, module in enumerate(cls.modules):
            module_name = cls.modules_name[index]

            module.stop()
            print(f"{module_name} stopped")

    @classmethod
    def start(cls, *args):
        for module_to_start in args:

            for index, module_name in enumerate(cls.modules_name):
                if module_name.casefold() == module_to_start.casefold():
                    module = cls.modules[index]
                    module_freq = cls.modules_freq[index]

                    module.start(module_freq)
                    print(f"{module_name} started")

                    break


    @classmethod
    def stop(cls, *args):
        for module_to_stop in args:

            for index, module_name in enumerate(cls.modules_name):
                if module_name.casefold() == module_to_stop.casefold():
                    module = cls.modules[index]

                    module.stop()
                    print(f"{module_name} stopped")

                    break
