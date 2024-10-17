from abc import ABC, abstractmethod


class BaseModule(ABC):
    @abstractmethod
    def run(self):
        pass


class ExampleModule(BaseModule):
    def run(self):
        print("Running ExampleModule")
