import json
import logging

import pika

logger = logging.getLogger(__name__)


class RabbitMQBroker:
    """
    Implementation of a broker that sends messages to a queue. This particular implementation is of a RabbitMQ broker.

    Attributes
    ----------

    queue_address: str
        The host of the RabbitMQ server.
    queue_name: str
        The name of the queue we are sending messages to.

    """

    def __init__(self, queue_address, queue_name):
        self.channel = None
        self.queue_address = queue_address
        self.queue_name = queue_name

    def start_connection(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.queue_address))
        self.channel = connection.channel()
        self.channel.queue_declare(queue=self.queue_name)

    def send_message(self, message):
        """
        Method used to send a message to the queue.
        :param message: Message we are sending to the queue.
            The message must be appropriately serialized by whoever invokes this method.
        :return:
        """
        logger.info("Attempting to send message...")
        if self.channel is None:
            logger.info('Starting connection !')
            self.start_connection()
        self.channel.basic_publish(exchange='', routing_key=self.queue_name, body=json.dumps(message))
        logger.info("Message sent.")
