
import base64
import json

from kombu.log import get_logger
from kombu.mixins import ConsumerMixin

from services.queues import task_queues

logger = get_logger(__name__)


class NumbersWorker(ConsumerMixin):

    def __init__(self, connection):
        self.connection = connection

    def get_consumers(self, Consumer, channel):
        return [Consumer(queues=task_queues, callbacks=[self.process_task])]

    def process_task(self, body, message):
        logger.info(f"received message: {body}")
        try:
            body: dict = json.loads(base64.b64decode(body).decode())
            logger.info(f"Decrypted: {body}")
            to_sort: list = body["arrange"]
            to_sort = sorted(to_sort)
            logger.info(f"sorted: {to_sort}")
        except Exception as exc:
            logger.error('task raised exception: %r', exc)

        message.ack()


__all__ = ["NumbersWorker", ]
