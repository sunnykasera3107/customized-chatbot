from infrastructure.cleaner.query_cleaner import QueryCleaner
from infrastructure.detectors.rule_based_detector import RuleBasedIntentDetector
import logging

class ExtractorService:

    def __init__(self):
        self._logger = logging.Logger(__name__)
        self._query_cleaner = QueryCleaner('infrastructure/data/query_cleaner_vocab.json')
        self._intent_detector = RuleBasedIntentDetector(self._query_cleaner, 'infrastructure/data/intent_dictionary.json')

    def handle(self, query: str):
        self._logger.info("Detecting intent")
        return self._intent_detector.detect(query)
    
