
import base64
import json
import random
from datetime import datetime
from typing import Any, Optional

from kombu import Connection
from kombu.pools import producers
from mode import Service

from services.queues import task_exchange


class NumbersMaker(Service):
    def __init__(self, **kwargs: Any):
        self._connection: Optional[Connection] = None
        super().__init__(**kwargs)

    async def on_start(self) -> None:
        self._connection = Connection("memory://")

    async def on_stop(self) -> None:
        if self._connection is not None:
            self._connection.release()

    @Service.task
    async def make_numbers(self) -> None:
        try:
            while not self.should_stop:
                x = random.SystemRandom()
                number_list = [int(x.random()*500000) for _ in range(20)]
                print(f"Generated: {number_list}")
                message = {"arrange": number_list}
                message = json.dumps(message).encode()
                message = base64.b64encode(message)
                with producers[self._connection].acquire(block=True) as producer:
                    print(f"Sent Message: {message} @ {datetime.now()}")
                    producer.publish(message, exchange=task_exchange, declare=[task_exchange],
                                     routing_key='numbers')

                await self.sleep(5.0)
        except KeyboardInterrupt:
            self.logger.info("Bye")


__all__ = ["NumbersMaker"]
