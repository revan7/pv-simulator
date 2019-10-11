import logging.config
import time
from messaging.senders.RabbitMQBroker import RabbitMQBroker
from meter.GaussianMeter import GaussianMeter

logging.config.fileConfig(fname='logger.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

broker = RabbitMQBroker('rabbit_pv', 'values')
rate = 2000
meter = GaussianMeter('gaussian', 0., 1., 9, 5, rate, 2000)

while True:
    logger.debug("Polling meter")
    reading = meter.get_reading()
    if reading:
        broker.send_message(reading)
    time.sleep(1)
