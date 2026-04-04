from domain.interfaces.validator import Validator

class OutputValidator(Validator):

    def __init__(self):
        pass

    def validate(self, llm_response: str) -> str:
        if not "intent" in llm_response:
            return False
        
        if not "entities" in llm_response:
            return False
        
        if not "answer" in llm_response:
            return False
        
        if not "external_tools" in llm_response:
            return False
        
        if not "confidence" in llm_response:
            return False

        return True