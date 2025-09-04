class ProtoChallenge:
    """
    This class represents a challenge in the progress system.
    Challenges are tasks that players must complete to progress in a level.

    Example:
        challenge = ProtoChallenge(
            title="Send 100 bits",
            condition=ProtoCondition({
                "source": "sent_bits",
                "value": 100,
                "comparator": ">="
            }),
            descr="Send at least 100 bits to complete this challenge."
        )
    """
    def __init__(self, title, condition, descr):
        """
        Initializes the ProtoChallenge with the given parameters.

        Parameters:
            title (str): The title of the challenge.
            condition (ProtoCondition): The condition that must be met to complete the challenge.
            descr (str): The description of the challenge.
        """
        self._title = title
        self._condition = condition
        self._descr = descr

    @property
    def title(self):
        """
        Returns the title of the challenge.

        Returns:
            str: The title of the challenge.
        """
        return self._title
    @property
    def descr(self):
        """
        Returns the description of the challenge.

        Returns:
            str: The description of the challenge.
        """
        return self._descr
    @property
    def condition(self):
        """
        Returns the condition of the challenge.

        Returns:
            ProtoCondition: The condition of the challenge.
        """
        return self._condition
    
    def check(self):
        """
        Checks if the challenge is complete.

        Returns:
            bool: True if the challenge is complete, False otherwise.
        """
        return self._condition.check()
    def progress(self):
        """
        Returns the progress of the challenge.

        Returns:
            float: The progress of the challenge as a percentage.
        """
        return self._condition.progress()

    #non static method to generate a new instance of the class based on the data
    @staticmethod
    def parse(data):
        """
        Parses the challenge data from a dictionary.

        Parameters:
            data (dict): The challenge data as a dictionary.

        Returns:
            ProtoChallenge: A new instance of ProtoChallenge or None if data is empty.

        Raises:
            TypeError: If the data is not a dictionary.
        """
        if not data:
            return None
        if not type(data) is dict:
            raise TypeError("Challenge data must be a dictionary / json object")
        title = data.get('title')
        descr = data.get('descr')
        cond_data = data.get('condition')
        from . import Condition
        condition = Condition(cond_data)
        descr = condition.fill_descr(descr)
        return ProtoChallenge(title, condition, descr)



class ProtoAchievement(ProtoChallenge):
    """
    This class represents an achievement.
    Achievements are special types of bonus challenges that provide experience points but are not required for level progression.

    Example:
        achievement = ProtoAchievement(
            name="Send 100 bits",
            condition=ProtoCondition({
                "source": "sent_bits",
                "value": 100,
                "comparator": ">="
            }),
            descr="Send at least 100 bits to complete this achievement.",
            xp=50
        )
    """
    def __init__(self, name, condition, descr, xp):
        """
        Initializes the ProtoAchievement with the given parameters.

        Parameters:
            name (str): The name of the achievement.
            condition (ProtoCondition): The condition that must be met to complete the achievement.
            descr (str): The description of the achievement.
            xp (int): The amount of experience points awarded for completing the achievement.
        """
        super().__init__(name, condition, descr)
        self._xp = xp
    
    @property
    def xp(self):
        """
        Returns the experience points awarded for completing the achievement.

        Returns:
            int: The experience points awarded for completing the achievement.
        """
        return self._xp