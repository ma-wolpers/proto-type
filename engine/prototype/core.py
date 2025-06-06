from engine import gui, Flow

# Main application class
class ProtoType:
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
        
        self.gui.build(self)
        self.flow.run()