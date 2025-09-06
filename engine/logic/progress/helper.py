class ProtoHelper:
    """
    This class provides advice for the current challenge.

    Example:
        hints = [
            {
                "condition": lambda: challenge.progress() == 0,
                "advice": '''Schau dich ein wenig um und probier aus, was du anklicken kannst.'''
            },
            {
                "condition": lambda: challenge.progress() < 100,
                "advice": '''Du hast die relevante Schaltfläche schon gefunden!
                Was hast du angeklickt, so dass sich der Fortschrittsbalken gefüllt hat?'''
            }
        ]
        helper = ProtoHelper(hints)
        advice = helper.get_advice()
    """
    def __init__(self, hints):
        """Initialize the ProtoHelper with the given app instance.

        Parameters:
            hints (list): A list of hint dictionaries containing conditions and advice.
        """
        self.hints = hints

    def get_advice(self):
        """
        Provides advice for the current challenge.

        Returns:
            str: Advice for the current challenge.
        """
        for hint in self.hints:
            if hint["condition"]():
                return hint["advice"]

        return "Vielleicht haben deine Mitspieler oder eine Lehrperson einen Tipp."
