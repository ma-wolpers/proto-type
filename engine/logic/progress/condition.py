import random

class ProtoCondition:
    def __init__(self, data):
        self._data = data
        self._parse_data()

    def progress(self):
        return self._progress()

    def check(self):
        return self._check()
    
    def print(self):
        return self._source() + " " + self._comparator + " " + str(self._value)
    
    def _parse_data(self):
        from engine.logic.progress import stats
        strsource = self._data.get("source", None)
        if strsource == "sent_bits":
            self._source = stats().sentbitcount
        elif strsource == "sent_content":
            self._source = stats().sentcontent
        elif strsource == "sent_0s":
            self._source = lambda: stats().sentcontent().count("0")
        elif strsource == "sent_1s":
            self._source = lambda: stats().sentcontent().count("1")
        else:
            raise ValueError("Unknown source")
        if "value" in self._data:
            self._value = int(self._data["value"])
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
            self._check = lambda: self._source() >= self._value
            self._progress = lambda: self._source()*100/self._value
        elif self._comparator == "endswith":
            self._check = lambda: self._source().endswith(self._value)
            self._progress = lambda: max(i for i in range(len(self._value)) if self._source().endswith(self._value[:i]))*100/len(self._value)
        else:
            raise ValueError("Unknown comparator")
        
    def fill_descr(self, descr):
        return descr.replace("{?}", str(self._value))