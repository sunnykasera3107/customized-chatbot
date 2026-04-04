from abc import abstractmethod

class IntentDetector():

    @abstractmethod
    def detect(self, query: str) -> str:
        pass