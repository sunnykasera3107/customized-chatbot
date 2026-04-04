from abc import abstractmethod

class Prompt():

    @abstractmethod
    def build(self) -> str:
        pass