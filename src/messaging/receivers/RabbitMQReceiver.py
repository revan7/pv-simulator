import pika


class RabbitMQReceiver:
    """
    Implementation of a receiver. Particularly a RabbitMQ Receiver.

    Attributes
    ----------

    queue_address: str
        The host of the RabbitMQ server.
    queue_name: str
        The name of the queue we are expecting messages from.
    """

    def __init__(self, queue_address, queue_name):
        self.queue_address = queue_address
        self.queue_name = queue_name
        self.channel = None

    def start_connection(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.queue_address))
        self.channel = connection.channel()
        self.channel.queue_declare(queue=self.queue_name)

    def start_listening(self, callback):
        """
        Method used to engage the receiver to start listening to messages from the queue.
        :param callback: The callback function that will be invoked when a message is consumed.
        :return:
        """
        if self.channel is None:
            self.start_connection()
        self.channel.basic_consume(
            queue=self.queue_name, on_message_callback=callback, auto_ack=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()
