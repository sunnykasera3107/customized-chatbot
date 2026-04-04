from abc import abstractmethod

class LLMClient():

    @abstractmethod
    def invoke(self, messages: list) -> str:
        pass