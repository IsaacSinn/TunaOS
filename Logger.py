import logging
from ModuleBase import Module
from pubsub import pub
import datetime

class Logger(Module):

    def __init__(self, log_file, log_print, *args):

        logFormatter = logging.Formatter("%(asctime)s [%(levelname)-5.5s] %(message)s")
        self.rootLogger = logging.getLogger()
        self.rootLogger.setLevel(logging.DEBUG)

        if log_file:
            log_date = datetime.datetime.now()
            log_date = log_date.strftime("%x").replace("/", "-")
            fileHandler = logging.FileHandler(f"./logs/{log_date}.log", mode = "a")
            fileHandler.setFormatter(logFormatter)
            self.rootLogger.addHandler(fileHandler)

        if log_print:
            consoleHandler = logging.StreamHandler()
            consoleHandler.setFormatter(logFormatter)
            self.rootLogger.addHandler(consoleHandler)

        for topic in args:
            pub.subscribe(self.Listener, topic)

    def Listener(self, message):
        self.rootLogger.debug(f"{message}")

    def run(self):
        pass

if __name__ == "__main__":
    pass
