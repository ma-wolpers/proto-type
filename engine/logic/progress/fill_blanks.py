import random

class ProtoFillBlanks:
    """
    This class is used to manage the data for the fill-in-the-blanks test.
    It contains the text parts and the options for each part.
    Parameters:
        test_data (dict): The test data containing the text parts and options.
    """
    def __init__(self, test_data):
        self._text_parts = test_data["text_parts"]
        self._options = test_data["options"]
        self._solutions = []
        for i in range(len(self._options)):
            self._solutions.append(self._options[i][0])
        
    def start(self):
        for i in range(len(self._options)):
            random.shuffle(self._options[i])
        return {
            "text_parts": self._text_parts,
            "options": self._options
        }

    def solve(self, answers):
        """
        Checks the answers for the fill-in-the-blanks test.
        It compares the answers with the solutions and returns a boolean indicating if all answers are correct.
        """
        for i in range(len(answers)):
            if answers[i] != self._solutions[i]:
                return False
        # if all answers are correct, the level is completed
        return True
