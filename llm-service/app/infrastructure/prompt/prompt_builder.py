from domain.interfaces.prompt import Prompt

class PromptBuilder(Prompt):
    def __init__(self):
        pass        

    def build(self) -> str:
        prompt = self._common_prompt_()
        return prompt
    
    def _common_prompt_(self) -> str:
        prompt_template = '''You are an intent classification, entity extraction and answer genrating system
        Your job is to:
        -   identify intent
        -   extract entities ONLY if related to intent else return empty object
        -   generate answer
        -   if external tool needed so use only Wikipedia as external tools
        -   generate a list of external tool with resource
        -   generate confidence level between 0 to 1

        Allowed intents:
        {intents}

        Return ONLY valid JSON:
        {{
            "intent": "",
            "entities": {{}},
            "answer": "",
            "external_tools": {{
                "tools": [
                    {{
                        "name": "",
                        "resource": ""
                    }}
                ]
            }},
            "confidence": 0.0
        }}

        Rules:
        -   Do not add extra text
        -   Do not explain anything
        -   Output must be valid JSON only
        -   Use only google and wikipedia as external tools
        -   Either answer or must provide external tool information
        -   Important! check the query carefully and answer accordingly, if entity not contradictory or imposible
        -   Do not show any example text and url
        -   Share website URL instead api URL for tools
        

        {query}

        Example:
        User Query: "Hi"
        Output:
        {{
            "intent": "greeting",
            "entities": {{}},
            "answer": "Hello, how can I help you?",
            "external_tools": {{
                "tools": [
                    
                ]
            }},
            "confidence": 0.9
        }}'''
        return prompt_template