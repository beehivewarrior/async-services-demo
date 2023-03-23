
from typing import Any, List

from mode import Service
from mode.utils.objects import cached_property

from services.service_a import NumbersMaker
from services.service_b import NumbersSorter


class App(Service):

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)

    def on_init_dependencies(self) -> List:
        return [
            self.service_a,
            self.service_b
        ]

    @cached_property
    def service_a(self) -> NumbersMaker:
        return NumbersMaker(loop=self.loop, beacon=self.beacon)

    @cached_property
    def service_b(self) -> NumbersSorter:
        return NumbersSorter(loop=self.loop, beacon=self.beacon)


if __name__ == "__main__":
    from mode.worker import Worker

    app = App()
    Worker(app, loglevel="info", daemon=True).execute_from_commandline()