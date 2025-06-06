import os  # Import the os module for file operations
import json

# FilesManager class
class FileManager:
    def __init__(self):
        self.__network_path = "./data/wan.net"  # Default path for the network file
        self._last_checked_timestamp = 0

    
    def update(self, network=""):
        if network:
            self.__network_path = network
            self._ensure_file_exists(self.__network_path)  # Ensure the selected file exists
            self._last_checked_timestamp = 0

    def get_net(self):
        return self.__network_path

    def _ensure_file_exists(self, filepath):
        # Check if the file exists, and create it if not
        if not os.path.exists(filepath):  # Check if file does not exist
            try:
                with open(filepath, "w", encoding="utf-8") as f:  # Open file in write mode
                    f.write("")  # Create an empty file
            except Exception as e:
                print(f"Fehler beim Erstellen der Datei: {e}")
                exit(1)  # Exit the program with an error code

    def load_file(self, filepath):
        # Open the file and read its content
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    
    def changes_in_network(self):
        try:
            current_timestamp = os.path.getmtime(self.__network_path)  # Get the current last-modified timestamp of the file 
            return current_timestamp != self._last_checked_timestamp                
        except FileNotFoundError:
            self._ensure_file_exists(self.__network_path)
            self._last_checked_timestamp = 0
            return True  # Consider file creation a 'change'

    def load_network_file(self):
        self._last_checked_timestamp = os.path.getmtime(self.__network_path)
        return self.load_file(self.__network_path)

    def load_json(self, filepath):
        if not filepath:
            return {}
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    def append_network(self, text):
        # Append the text to the network file
        with open(self.__network_path, "a", encoding="utf-8") as f:
            f.write(text)

    def save_file(self, filepath, text):
        # Save the text to the file
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(text)
        return filepath

_filemanager = FileManager()  # Create a global instance of FileManager
def get_filemanager():
    """
    Returns the global instance of FileManager.
    If the instance does not exist, it creates a new one.
    
    Returns:
        FileManager: The global instance of FileManager.
    """
    global _filemanager
    if _filemanager is None:
        _filemanager = FileManager()
    return _filemanager





