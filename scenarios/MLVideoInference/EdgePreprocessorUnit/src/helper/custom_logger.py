import logging

rootLogger = logging.getLogger()
rootLogger.setLevel(logging.DEBUG)


class CustomLogger():
    def get_logger(self): 
        logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")

        consoleHandler = logging.StreamHandler()
        consoleHandler.setFormatter(logFormatter)
        consoleHandler.setLevel(logging.DEBUG)
        rootLogger.addHandler(consoleHandler)

        return rootLogger