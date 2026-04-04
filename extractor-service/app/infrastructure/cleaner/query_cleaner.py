import string, logging
from domain.interfaces.cleaner import Cleaner
from infrastructure.utils.file_loader import load_json

class QueryCleaner(Cleaner):
    def __init__(self, file_path: str):
        self._logger = logging.getLogger(__name__)
        self._logger.info(f"Reading cleaner vocab")
        self._query_cleaner_vocab = load_json(file_path)
        self._logger.info(f"Cleaner vocab: {self._query_cleaner_vocab}")
        self._query, self._clean_query = "", ""
    
    def clean(self, query: str) -> str:
        self._logger.info(f"Cleaning query: {query}")
        self._query = query
        self._clean_query = query.lower().strip()
        self._clean_contraction_()
        self._clean_ambiguous_()
        self._remove_punctuation_()
        self._lemmatization_()
        self._convert_number_name_()
        self._clear_extra_space_()
        return self._clean_query
    
    def _lemmatization_(self) -> str:
        self._logger.info(f"Performing lemmatization")
        word_to_remove = self._query_cleaner_vocab['words_to_remove']
        words = self._clean_query.split(" ")
        clean_words = [word if not word in word_to_remove else '' for word in words]
        self._clean_query = ' '.join(clean_words).strip()
        self._logger.info(f"Lemmatized: {self._clean_query}")
    
    def _remove_punctuation_(self) -> str:
        self._logger.info(f"Removing punctuations")
        table = str.maketrans({p: ' ' for p in string.punctuation})
        self._clean_query = self._clean_query.translate(table)
        self._logger.info(f"Removed punctuations: {self._clean_query}")
    
    def _clean_contraction_(self) -> str:
        self._logger.info(f"Replacing contraction words")
        words = self._clean_query.split(" ")
        pronoun_contractions = self._query_cleaner_vocab.get('pronoun_contractions')
        list_word = [word if word not in pronoun_contractions else pronoun_contractions.get(word) for word in words]
        if len(list_word) == 0:
            raise ValueError(f"Value not found: {list_word}")
        self._clean_query = ' '.join(list_word)
        self._logger.info(f"Replacing contraction words: {self._clean_query}")
    
    def _clean_ambiguous_(self) -> str:
        self._logger.info(f"Replacing ambiguities")
        words = self._clean_query.split(" ")
        ambiguous = self._query_cleaner_vocab.get('ambiguous')
        new_words = []
        for i in range(len(words)):
            current = words[i]
            next_word = words[i + 1] if i < len(words) - 1 else None
            if current in ambiguous:
                current_ambiguous = ambiguous.get(current)
                past_ambiguous = current_ambiguous.get("past")
                if next_word[-2:] in past_ambiguous:
                    new_words.append(past_ambiguous.get(next_word[-2:]))
                else:
                    new_words.append(current_ambiguous.get("fall_back"))
            else:
                new_words.append(current)
        
        self._clean_query = " ".join(new_words)
        self._logger.info(f"Replaced ambiguities: {self._clean_query}")

    def _clear_extra_space_(self):
        self._logger.info(f"Removing extra space")
        self._clean_query = self._clean_query.replace("   ", " ").replace("  ", " ")

    def _convert_number_name_(self) -> str:
        self._logger.info(f"Replacing number name into number")
        one_word = { 'zero': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 
                    'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10, 'eleven': 11, 
                    'twelve': 12, 'thirteen': 13, 'fourteen': 14, 'fifteen': 15, 'sixteen': 16, 
                    'seventeen': 17, 'eighteen': 18, 'nineteen': 19}
        tens_joiner = { 'twenty': 20, 'thirty': 30, 'forty': 40, 'fifty': 50, 'sixty': 60, 
                       'seventy': 70, 'eighty': 80, 'ninety': 90 }
        
        other_joiner = { 'hundred': 100, 'thousand': 1000, 'million': 1000000, 'billion': 10000000 }

        result = []
        current = 0
        total = 0
        in_number = False

        i = 0
        while i < len(self._clean_query):
            w = self._clean_query[i]

            if w in one_word:
                current += one_word[w]
                in_number = True

            elif w in tens_joiner:
                current += tens_joiner[w]
                in_number = True

            elif w == "hundred":
                current *= 100
                in_number = True

            elif w in ("thousand", "million", "billion"):
                current *= other_joiner[w]
                total += current
                current = 0
                in_number = True

            else:
                if in_number:
                    total += current
                    result.append(str(total))
                    current = 0
                    total = 0
                    in_number = False

                result.append(w)

            i += 1

        if in_number:
            total += current
            result.append(str(total))

        self._clean_query = "".join(result)
        self._logger.info(f"Replaced number name into number: {self._clean_query}")
        