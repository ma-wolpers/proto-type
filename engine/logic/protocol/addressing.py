class ProtoFilter:
    def __init__(self, filter={}):
        self.update(filter)

    def update(self, filter):
        """Update the filter criteria with a dictionary.

        Parameters:
            filter (dict): A dictionary containing the filter criteria:
                "starts" : binary code (str)
                "ends" : binary code (str)
        """
        
        # check if the filter is a valid dictionary
        if not isinstance(filter, dict):
            raise Warning("Filter", "Filter muss ein Dictionary sein!")
        if not all(isinstance(v, str) for v in filter.values()):
            raise Warning("Filter", "Filterwerte müssen Strings sein!")
        # check if the filter items are binary codes
        if not all(c in "01" for v in filter.values() for c in v):
            raise Warning("Filter", "Nur 0 und 1 erlaubt!")
        self._starts = filter.get("starts", "")
        self._ends = filter.get("ends", "")
    
    def get(self):
        """Get the filter criteria as a dictionary.
        
        Returns:
            dict: A dictionary containing the filter criteria:
                "starts" : binary code (str)
                "ends" : binary code (str)
        """
        return {
            "starts": self._starts,
            "ends": self._ends
        }
    
    def is_empty(self):
        """Checks if the filter is empty.
        Returns:
            bool: True if the filter is empty, False otherwise.
        """
        return not (self._starts or self._ends)
    
    def filter_lines(self, lines):
        """Apply the filter to a list of lines.
        
        Parameters:
            lines (list): A list of lines to filter.
        Returns:
            list: A list of lines that match the filter criteria.
        """
        if not lines:
            return []
        if self._starts:
            lines = [line for line in lines if line.startswith(self._starts)]
        if self._ends:
            lines = [line for line in lines if line.endswith(self._ends)]
        return lines

    def check_text(self, text):
        """Check if the text matches the filter criteria.
        
        Parameters:
            text (str): The text to check.
        Returns:
            bool: True if the text matches the filter criteria, False otherwise.
        """

        if self.is_empty():
            return True
        if not text:
            return False
        if self._starts and not text.startswith(self._starts):
            return False
        if self._ends and not text.endswith(self._ends):
            return False
        return True



class ProtoSignature:
    def __init__(self, signature={}):
        self.update(signature)

    def update(self, signature={}):
        self._start = signature.get("start", "")
        self._end = signature.get("end", "")
    
    def get(self):
        return {
            "start": self._start,
            "end": self._end
        }
    
    def sign(self, text):
        return "\n".join([f"{self._start}{line}{self._end}" for line in text.split("\n")])