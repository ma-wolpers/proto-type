import json  # Import the json module for handling JSON data

from lib.managers.file_managers import FilesManager, ProtoSettings
from lib.bicoder import BinaryCoder, ProtoFilter, ProtoSignature
from ProtoType.logic.progress.progress import ProtoProgress, ProtoStats, ProtoAchievement
from lib.gui import ProtoGUI


# Main application class
class ProtoType:
    def __init__(self):
        """
        Initialize the main application. 
        """
        
        self.filemanager = FilesManager(network="./data/wan.net")  # file manager
        self.bicoder = BinaryCoder()  # internal coding engine
        self.filter = ProtoFilter()  # filter for text lines
        self.signature = ProtoSignature()  # signature for text lines
        self.stats = ProtoStats()  # Initialize the statistics manager
        self.progress = ProtoProgress(self.stats, self.filemanager)  # Initialize the progress manager
        self.settings = ProtoSettings(self.filemanager, self.bicoder, self.filter, self.signature, self.stats, self.progress)  # data organiser

        self.gui = ProtoGUI()  # graphic user interface
        self.flow = ProtoFlow(self.filemanager, self.settings, self.bicoder, self.filter, self.signature, self.stats, self.progress, self.gui)  # controller of program flow

        
