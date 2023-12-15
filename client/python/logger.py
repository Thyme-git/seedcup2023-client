import logging

# logger config
logging.basicConfig(
    # uncomment this will redirect log to file *client.log*
    # filename="client.log",
    # filemode="a+",
    format="[%(asctime)s][%(levelname)s] %(message)s",
)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)