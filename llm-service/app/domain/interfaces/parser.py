from abc import abstractmethod

class Parser():

    @abstractmethod
    def parse(self, content: str) -> str:
        pass