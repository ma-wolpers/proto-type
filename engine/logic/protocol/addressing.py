class ProtoFilter:
    """
    This class is used to filter messages based on their binary representation.
    It allows you to specify patterns for the start and end of the messages.

    Example:
        filter = ProtoFilter({
            "starts": "110",
            "ends": "001"
        })
    """

    def __init__(self, filter={}):
        """Initialize the ProtoFilter with a filter dictionary.

        Parameters:
            filter (dict): A dictionary containing the filter criteria.
        """
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
    """
    This class is used to represent the signature of a message.
    It allows you to specify a start and end string that will be added to each message.

    Example:
        signature = ProtoSignature({
            "start": "Anna",
            "end": "Bob"
        })
    """
    def __init__(self, signature={}):
        """
        Initializes the ProtoSignature with the given signature (a string that is automatically added to each message's start or end).

        Parameters:
            signature (dict): A dictionary containing the signature information.
        """
        self._start = ""
        self._end = ""
        self.update(signature)

    def update(self, signature={}):
        """
        Updates the signature with the given dictionary.

        Parameters:
            signature (dict): A dictionary containing the signature information:
                "start": The start string (str)
                "end": The end string (str)
        """
        if not isinstance(signature, dict):
            print(f"Achtung: {signature} ist kein Dictionary!")
        if not all(isinstance(v, str) for v in signature.values()):
            print(f"Achtung: {signature} sind keine Strings!")
        self._start = signature.get("start", "")
        self._end = signature.get("end", "")
    
    def get(self):
        """
        Gets the signature information as a dictionary.

        Returns:
            dict: A dictionary containing the signature information:
                "start": The start string (str)
                "end": The end string (str)
        """
        return {
            "start": self._start,
            "end": self._end
        }
    
    def sign(self, text):
        """
        Signs the given text by adding the start and end strings.

        Parameters:
            text (str): The text to sign.

        Returns:
            str: The signed text.
        """
        return "\n".join([f"{self._start}{line}{self._end}" for line in text.split("\n")])
    

_filter = None
_signature = None

def get_filter():
    """Get the singleton instance of ProtoFilter.
    If the instance does not exist, it will be created.

    Returns:
        ProtoFilter: The singleton instance of ProtoFilter.
    """
    global _filter
    if _filter is None:
        _filter = ProtoFilter()
    return _filter

def get_signature():
    """Get the singleton instance of ProtoSignature.
    If the instance does not exist, it will be created.

    Returns:
        ProtoSignature: The singleton instance of ProtoSignature.
    """
    global _signature
    if _signature is None:
        _signature = ProtoSignature()
    return _signature