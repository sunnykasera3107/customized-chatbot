from infrastructure.clients.groq_llm import GroqLLM
from infrastructure.prompt.prompt_builder import PromptBuilder
from infrastructure.parser.response_parser import ResponseParser
from infrastructure.validator.output_validator import OutputValidator
from infrastructure.utils.file_loader import load_json
import logging

class LLMService:

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._prompt_builder = PromptBuilder()
        self._intent_data = load_json("infrastructure/data/intents.json")
        self._groq_llm = GroqLLM()
        self._parser = ResponseParser()
        self._validator = OutputValidator()
        self._messages = [
            {"role": "system", "content": "I am here to assist you."}
        ]

    async def handle(self, query: str, messages: list):
        self._messages = messages
        intents = "".join(["-   " + intent + " \n        " for intent in self._intent_data.get("intents")])
        prompt_template = self._prompt_builder.build()
        prompt = prompt_template.format(query=query, intents=intents)
        self._messages.append(
            {"role": "user", "content": prompt}
        )
        for i in range(3):
            llm_response = self._groq_llm.invoke(self._messages)
            clean_reponse = self._parser.parse(llm_response.choices[0].message.content)
            if self._validator.validate(clean_reponse):
                return clean_reponse
        
        self._logger.error(f"Invalid response: {clean_reponse}")
        return {"error": f"Invalid response: {clean_reponse}"}
    

    
