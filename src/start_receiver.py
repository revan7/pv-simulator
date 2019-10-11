import json
import logging.config
from datetime import datetime

import Utils
from messaging.receivers.RabbitMQReceiver import RabbitMQReceiver
from pv.PVSimulator import PVSimulator

logging.config.fileConfig(fname='logger.conf', disable_existing_loggers=False)
logger = logging.getLogger(__name__)

pv_generator = PVSimulator(0.6)


def on_message_received(ch, method, properties, body):
    """
    We pass this function to the broker, because this is the call back for when we receive messages.
    This has the signature that RabbitMQ callbacks require. 
    :param ch:
    :param method:
    :param properties:
    :param body:
    :return:
    """
    message = json.loads(body)
    measured_value = message['measured_value']
    time = datetime.strptime(message['time'], "%Y-%m-%dT%H:%M:%S.%f")
    output_value = pv_generator.output(measured_value)
    Utils.write_output(time, measured_value, output_value, measured_value + output_value)
    logger.info("Received : {}".format(message))


receiver = RabbitMQReceiver('rabbit_pv', 'values')
receiver.start_listening(on_message_received)
