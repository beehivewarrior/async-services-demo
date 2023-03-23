from typing import Any, Optional

from kombu import Connection
from mode.threads import ServiceThread

from services.service_b.worker import NumbersWorker


class NumbersSorter(ServiceThread):
    def __init__(self, **kwargs: Any):
        self._connection: Optional[Connection] = None
        self.worker = None
        super().__init__(**kwargs)

    async def on_start(self) -> None:
        self._connection = Connection("memory://")
        self.worker = NumbersWorker(self._connection)

    @ServiceThread.task
    async def run_worker(self) -> None:
        print("Running Numbers Worker")
        try:
            while not self.should_stop:
                self.worker.run()
        except KeyboardInterrupt:
            self.logger.info("Bye")

    async def on_stop(self) -> None:
        if self.worker is not None:
            self.worker = None
        if self._connection is not None:
            self._connection.release()


__all__ = ["NumbersSorter", ]
