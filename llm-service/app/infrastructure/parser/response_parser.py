from domain.interfaces.parser import Parser
from functools import reduce
import json, logging

class ResponseParser(Parser):

    def __init__(self):
        self._logger = logging.getLogger(__name__)
        self._content = ""

    def parse(self, content: str) -> str:
        self._logger.info(f"Parsing the response: {content}")
        self._content = content.strip()
        self._remove_space_nl_()
        self._logger.info(f"Parsed response: {self._content}")
        return json.loads(self._content)
    
    def _remove_space_nl_(self):
        rules = [ ("     ", ""), ("    ", ""), ("   ", ""), ("  ", " "),  ("\n", ""), ("\\n", ""), ("\\", ""), ("`", "")]
        self._content = reduce(lambda c, r: c.replace(*r), rules, self._content)
        