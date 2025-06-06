class ProtoChallenge:
    def __init__(self, title, condition, descr):
        self._title = title
        self._condition = condition
        self._descr = descr

    @property
    def title(self):
        return self._title
    @property
    def descr(self):
        return self._descr
    @property
    def condition(self):
        return self._condition
    
    def check(self):
        return self._condition.check()
    def progress(self):
        return self._condition.progress()

    #non static method to generate a new instance of the class based on the data
    @staticmethod
    def parse(data, stats):
        if not data:
            return None
        if not type(data) is dict:
            raise TypeError("Challenge data must be a dictionary / json object")
        title = data.get('title')
        descr = data.get('descr')
        cond_data = data.get('condition')
        condition = ProtoCondition(cond_data, stats)
        descr = condition.fill_descr(descr)
        return ProtoChallenge(title, condition, descr)



class ProtoAchievement(ProtoChallenge):
    def __init__(self, name, condition, descr, xp):
        super().__init__(name, condition, descr)
        self._xp = xp
    
    @property
    def xp(self):
        return self._xp