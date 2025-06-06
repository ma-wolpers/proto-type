class ProtoLevel:
    def __init__(self, id, title, challenges, fill_blanks, unlock_features=[]):
        self._id = id
        self._title = title
        self._challenges = challenges
        self._unlock_features = unlock_features
        self._fill_blanks = fill_blanks
    
    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title
    
    @property
    def challenges(self):
        return self._challenges

    """ Returns a list of features that are unlocked at this level """
    @property
    def unlock(self):
        return self._unlock_features
    
    """ Returns the fill-in-the-blanks text that constitutes the final challenge of this level """
    @property
    def fill_blanks(self):
        return self._fill_blanks
