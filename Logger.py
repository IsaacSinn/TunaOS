import logging
from ModuleBase import Module
from pubsub import pub

class Logger(Module):

    def __init__(self, log_file, log_print, *args):

        if log_file:
            logging.basicConfig(filename='info.log', filemode='a', format='%(name)s - %(levelname)s - %(message)s')

        if log_print:
            logging.basicConfig(level=logging.DEBUG)

        for topic in args:
            pub.subscribe(self.Listener, topic)

    def Listener(self, message):
        logging.debug(str(message))
