from abc import abstractmethod

class Cleaner():

    @abstractmethod
    def clean(self, query: str) -> str:
        pass