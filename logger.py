import logging

logger = logging.getLogger('Logger')
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

FileOutputHandler = logging.FileHandler('logs.log')
logger.addHandler(FileOutputHandler)
