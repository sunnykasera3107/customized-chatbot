import logging
from domain.interfaces.intent_detector import IntentDetector
from domain.interfaces.cleaner import Cleaner
from infrastructure.utils.file_loader import load_json

class RuleBasedIntentDetector(IntentDetector):
    def __init__(self, cleaner: Cleaner, json_path: str):
        self._logger = logging.getLogger(__name__)
        self._cleaner = cleaner
        self._logger.info("Reading intent map file")
        self._intent_map = load_json(json_path)
        self._logger.info(f"Intent map: {self._intent_map}")

    def detect(self, query: str) -> str:
        clean_query = self._cleaner.clean(query)
        best_intent = None
        best_score, required_confidence, priority = 0, 0, 1
        self._logger.info(f"Detecting intent")
        for intent, data in self._intent_map.items():
            score = 0
            for word in data.get('keywords'):
                if word in clean_query:
                    score += 1
                elif clean_query in word or query in word:
                    score += 1
            
            score = (score / (min(5, len(data.get('keywords')) / 3)))

            if score > best_score:
                best_score = score
                best_intent = intent
                required_confidence = data.get("required_confidence")
                priority = data.get("priority")

        self._logger.info(f"Intent: {best_intent or "unknown"}")
        return {
            'intent': best_intent or 'unknown',
            'initial_query': query,
            'clean_query': clean_query,
            'confidence': best_score,
            'required_confidence': required_confidence,
            'id': priority
        }
    
    