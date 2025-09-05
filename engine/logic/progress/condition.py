import random

class ProtoCondition:
    """
    This class represents a condition that can be checked and monitored.
    
    Example:
        condition = ProtoCondition({
            "source": "sent_bits",
            "value": 100,
            "comparator": ">="
        })
    """
    def __init__(self, data):
        """Initializes the condition with the provided data.
        
        Parameters:
            data (dict): A dictionary containing the condition's configuration:
                - "source": A string indicating the source of the data (e.g., "sent_bits", "sent_content").
                - "value": An integer or a dictionary for random value generation.
                - "comparator": A string indicating the comparison operation (e.g., ">=", "endswith").
        Raises:
            ValueError: If the data does not contain valid source, value, or comparator.
        """
        self._data = data
        self._parse_data()

    def progress(self):
        """Calculates the progress based on the source and value.
        Returns:
            float: The progress as a percentage of the source value relative to the target value.
        """
        return self._progress()*100

    def check(self):
        """
        Checks if the condition is met.

        Returns:
            bool: True if the condition is met, False otherwise.
        """
        return self._check()
    
    def print(self):
        """
        Returns a string representation of the condition.

        Returns:
            str: A string representation of the condition.
        """
        return str(self._source()) + " " + self._comparator + " " + str(self._value)
    
    def _parse_data(self):
        """
        Parses the condition data to set up the source, value, comparator, and check function.
        
        Raises:
            ValueError: If the data does not contain valid source, value, or comparator.
        """
        from engine.logic.progress import stats
        strsource = self._data.get("source", None)
        if strsource == "sent_bits":
            self._source = lambda: str(stats().sentbitcount)
        elif strsource == "sent_content":
            self._source = lambda: stats().sentcontent
        elif strsource == "sent_0s":
            self._source = lambda: str(stats().sentcontent.count("0"))
        elif strsource == "sent_1s":
            self._source = lambda: str(stats().sentcontent.count("1"))
        else:
            raise ValueError("Unknown source")
        if "value" in self._data:
            self._value = self._data["value"]
        elif "random" in self._data:
            rtype = self._data["random"]["type"]
            rlength = self._data["random"]["length"]
            rsymmetry = self._data["random"].get("symmetry", None)
            if rtype == "bits":
                self._value = format(random.getrandbits(rlength), f'0{rlength}b')
            else:
                raise ValueError("Unknown random type")
            if type(rsymmetry) is int:
                for i in range(rsymmetry):
                    self._value = self._value + self._value[::-1]
            else:
                raise ValueError("Symmetry must be an integer")
        else:
            raise ValueError("No value given")
        
        self._comparator = self._data.get("comparator", None)

        if self._comparator == ">=":
            self._check = lambda: float(self._source()) >= float(self._value)
            self._progress = lambda: float(self._source())/float(self._value)
        elif self._comparator == "endswith":
            self._check = lambda: self._source().endswith(self._value)
            self._progress = lambda: float(max(i for i in range(len(self._value)) if self._source().endswith(self._value[:i])))/float(len(self._value))
        else:
            raise ValueError("Unknown comparator")
        
    def fill_descr(self, descr):
        """
        Completes the description with the generated value.

        Parameters:
            descr (str): The description template containing "{?}" placeholders.

        Returns:
            str: The filled description with the generated value.
        """
        return descr.replace("{?}", str(self._value))