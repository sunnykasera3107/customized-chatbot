from abc import abstractmethod

class Validator():

    @abstractmethod
    def validate(self, llm_response: str) -> str:
        pass