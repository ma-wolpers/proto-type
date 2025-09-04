class ProtoLevel:
    """
    This class represents a level in the progress system.
    A level consists of various challenges that the user must progressively complete and a fill-in-the-blanks task at the end to assess their understanding.

    Example:
        level = ProtoLevel(
            id=1,
            title="Level 1",
            challenges=[...],
            fill_blanks=ProtoFillBlanks(test_data),
            unlock_features=["feature_1"]
        )
    """
    def __init__(self, id, title, challenges, fill_blanks, unlock_features=[]):
        """
        Initializes the ProtoLevel with the given parameters.

        Parameters:
            id (int): The number of the level.
            title (str): The title of the level.
            challenges (list): A list of challenges for this level.
            fill_blanks (ProtoFillBlanks): The fill-in-the-blanks instance for this level.
            unlock_features (list): A list of features that are unlocked at this level.
        """
        self._id = id
        self._title = title
        self._challenges = challenges
        self._unlock_features = unlock_features
        self._fill_blanks = fill_blanks
    
    @property
    def id(self):
        """Returns the ID of the level."""
        return self._id

    @property
    def title(self):
        """Returns the title of the level."""
        return self._title
    
    @property
    def challenges(self):
        """Returns a list of challenges for this level."""
        return self._challenges

    @property
    def unlock(self):
        """ Returns a list of features that are unlocked at this level """
        return self._unlock_features
    
    @property
    def fill_blanks(self):
        """Returns the fill-in-the-blanks instance that constitutes the final challenge of this level."""
        return self._fill_blanks
