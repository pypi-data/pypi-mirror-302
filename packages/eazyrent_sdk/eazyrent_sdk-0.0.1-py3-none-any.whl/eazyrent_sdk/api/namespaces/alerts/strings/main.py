import re
import unicodedata

from Levenshtein import distance


class Strings:
    def normalize(self, string: str) -> str:
        """Normalize a string for a proper comparison.

        args:
            - string (str): The string to normalize

        returns:
            - normalized_string (str): The normalized string.

        examples:
            >>>normalize("De--Fransiscô)
            de-fransisco
        """
        normalized = string.lower()
        normalized = unicodedata.normalize("NFD", normalized)
        normalized = "".join(c for c in normalized if unicodedata.category(c) != "Mn")
        normalized = re.sub(r"\s*-\s*", "-", normalized)
        normalized = re.sub(r"\s+", " ", normalized)
        normalized = re.sub(r"-+", "-", normalized)
        normalized = normalized.strip()
        return normalized

    def strings_distances(self, string: str, reference: str) -> int:
        """Compute strings distances using Levenshtein distance.

        args:
            - string (str): The string to compare to reference
            - reference (str): Reference to compare with.

        returns:
            - distance (int): The levenshtein distance between the two strings.
        """
        return distance(string, reference)
