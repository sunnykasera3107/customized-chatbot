import logging

class ResponseGenerator:
    def __init__(self, tool_list: dict):
        self._logger = logging.getLogger(__name__)
        self._tools_list = tool_list
        self._processed_data = ""

    def generate(self, data: dict) -> str:
        answer = data.get("answer")
        if not answer == "None" and not answer == None:
            return answer
        
        self._logger.info("Genrating standard response for query.")
        intent = data.get("intent")
        if intent in self._tools_list:
            entities = data.get("entities")
            required_entity = self._tools_list.get(intent)
            for entity in required_entity.get("responses"):
                if not entity in entities:
                    return required_entity.get(entity)
        
        return "I do not understand your question. Can you explore it bit more?"
