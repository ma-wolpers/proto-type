from engine import gui, Flow

# Main application class
class ProtoType:
    """
    The main application class for the ProtoType project.
    """
    def __init__(self):
        """
        Initialize the main application.
        """
        self.gui = gui()  # graphic user interface
        self.flow = Flow()  # controller of program flow

    def run(self):
        """
        Run the main application.
        """
        self.gui.build(self.flow)
        self.flow.run()