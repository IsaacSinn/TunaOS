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
        return cls.instance

    @classmethod
    def register(cls, *args): # mm.register(("Module1", "Module1", freq), ("Module2", "Module2", freq))
        for module_info in args:

            module_file = module_info[0]
            module_name = module_info[1]
            module_freq = module_info[2]

            exec(f"from {module_file} import {module_name}")
            module = eval(f"{module_name}()")
            cls.modules.append( {"name" : module_name, "object": module, "freq": module_freq} )

    @classmethod
    def get_registered_modules(cls):
        return cls.modules

    @classmethod
    def start_all(cls):
        for module in cls.modules:
            module_name = module["name"]
            module_object = module["object"]
            module_freq = module["freq"]

            module_object.start(module_freq)
            print(f"{module_name} started")

    @classmethod
    def stop_all(cls):
        for module in cls.modules:
            module_name = module["name"]
            module_object = module["object"]
            module_freq = module["freq"]

            module_object.stop()
            print(f"{module_name} stopped")

    @classmethod
    def start(cls, *args):
        for module_info in args:
            module_name = module_info[0]
            module_freq = module_info[1]

            for index in range(len(cls.modules)):
                if cls.modules[index]["name"] == module_name:
                    cls.modules[index]["object"].start(module_freq)
                    print(f"{module_name} started")

    @classmethod
    def stop(cls, *args):
        for module_info in args:
            module_name = module_info[0]
            module_freq = module_info[1]

            for index in range(len(cls.modules)):
                if cls.modules[index]["name"] == module_name:
                    cls.modules[index]["object"].stop(module_freq)
                    print(f"{module_name} stopped")
