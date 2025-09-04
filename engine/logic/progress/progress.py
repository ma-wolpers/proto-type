from . import Challenge, FillBlanks, Level

class ProtoProgress:
    """
    This class is used to manage the progress of the user through the levels and challenges.
    """

    def __init__(self):
        """
        Initializes the ProtoProgress with the available levels and challenges.
        """
        self.alllevels = self.load_levels()

        self._lvl_id = 1
        self._chlng_id = 0

        self.unlocked_features = []

    # def get_unlocked_features(self):
    #     return self.unlocked_features.get(self.level, [])
    
    @property
    def level(self):
        """
        Gets the current level.

        Returns:
            Level: The current level object, or None if the level is not found.
        """
        if self._lvl_id > len(self.alllevels):
            return None
        return self.alllevels[self._lvl_id]

    @property
    def challenge(self):
        """
        Gets the current challenge.

        Returns:
            Challenge: The current challenge object, or None if the challenge is not found.
        """
        if not self.level or self._chlng_id < 0:
            return None
        if self._chlng_id >= len(self.level.challenges):
            return None
        return self.level.challenges[self._chlng_id]

    @property
    def leveldata(self):
        """
        Gets the current level data.

        Returns:
            dict: A dictionary containing the current level data.
        """
        id = self._lvl_id
        name = self.alllevels[id].title
        return {
            'id': id,
            'title': name
        }
    
    @property
    def chlgdata(self):
        """
        Gets the current challenge data. If the challenge is not found, an empty dictionary is returned.

        Returns:
            dict: A dictionary containing the current challenge data.
        """
        chlg = self.challenge
        if not chlg:
            return {
                'id': self._chlng_id,
                'title': '',
                'descr': ''
            }
        title = chlg.title
        descr = chlg.descr
        return {
            'id': self._chlng_id,
            'title': title,
            'descr': descr
        }

    def update(self, data):
        """
        Updates the progress data with the given dictionary. If the dictionary is invalid, a warning is raised.

        Parameters:
            data (dict): A dictionary containing the progress data:
                "level": The current level ID (int)
                "challenge": The current challenge ID (int)
        """
        if not isinstance(data, dict):
            print(f"Achtung: {data} ist kein Dictionary!")
            return
        if not all(k in data for k in ['level', 'challenge']):
            print(f"Achtung: {data} enthält nicht alle erforderlichen Schlüssel!")
            return
        self._lvl_id = data['level']
        self._chlng_id = data['challenge']

    def get_ids(self):
        """
        Gets the current level and challenge IDs.

        Returns:
            dict: A dictionary containing the current level and challenge IDs.
        """
        return {
            'level_id': self._lvl_id,
            'challenge_id': self._chlng_id
        }

    def check_challenge(self):
        """
        Checks if the current challenge is completed.

        Called:
            By the Flow (check_progress) whenever anything changes.

        Returns:
            tuple: (bool, int) - True if the challenge is completed, False if not.
                If True, the second value is 1 if all challenges are completed, otherwise 0.
                If False, the second value is the progress of the challenge.
        """
        if not (self.challenge and self.level):
            return False, 0
        if self.challenge.check():
            self._chlng_id += 1
            if self._chlng_id >= len(self.level.challenges):
                return True, 1 # all Challenges completed
            return True, 0 # Challenge completed
        else:
            progress = self.challenge.progress()
        return False, progress

    def start_fb(self):
        """ 
        Starts the fill-in-the-blanks test.
        
        Called:
            By the Flow (check_progress) when the user finishes with all challenges.
        
        Returns:
            dict: A dictionary containing the text parts and options for the fill-in-the-blanks test.
        """
        if not self.level or not self.level.fill_blanks:
            return None
        return self.level.fill_blanks.start()
    
    def score_fb(self, answers):
        """
        Checks the answers for the fill-in-the-blanks test.

        Called:
            By the Flow (submit_answers) when the user submits answers for the fill-in-the-blanks test.
        
        Returns:
            bool: True if all answers are correct, False otherwise.
        """
        if not self.level or not self.level.fill_blanks:
            return False
        if self.level.fill_blanks.solve(answers):
            self.level_up()
            return True
        self._chlng_id = 0
        return False
        

    def level_up(self):
        """
        Increments the level ID and resets the challenge ID.

        Called:
            By the Progress (score_fb) when the user has sumitted a currect answer to the fill-in-the-blanks test.

        This method is called when the user completes the fill-in-the-blanks test.
        """
        self._lvl_id += 1
        self._chlng_id = 0

    def load_levels(self):
        """
        Loads the levels from the JSON file.

        Returns:
            dict: A dictionary containing the levels, where the keys are level IDs and the values are ProtoLevel objects.
        """
        from .. import filemanager
        levelsdata = filemanager().load_json("data/.progress.json")

        levels = {}
        for levelid, level in levelsdata.items():
            challenges = []
            for cdata in level['challenges']:
                new_challenge = Challenge.parse(data=cdata)
                challenges.append(new_challenge)
            levelnum = int(levelid)
            fillblanktest = FillBlanks(level['fill_blanks'])
            levels[levelnum] = Level(levelnum, level['title'], challenges, fillblanktest, level['unlock'])
        return levels
    
_progress = None
def get_progress():
    """
    Returns the global instance of ProtoProgress.
    If the instance does not exist, it creates a new one.

    Returns:
        ProtoProgress: The global instance of ProtoProgress.
    """
    global _progress
    if _progress is None:
        _progress = ProtoProgress()
    return _progress