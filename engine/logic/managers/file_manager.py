import os  # Import the os module for file operations
import json

# FilesManager class
class FileManager:
    """
    Manages file operations for the application.
    """
    def __init__(self):
        """
        Initializes the FileManager with default values.
        """
        self.__network_path = "./data/wan.net"  # Default path for the network file
        self._last_checked_timestamp = 0

    
    def update(self, network=""):
        """
        Updates the network path.

        Parameters:
            network (str): The new network path.
        """
        if network:
            self.__network_path = network
            self._ensure_file_exists(self.__network_path)  # Ensure the selected file exists
            self._last_checked_timestamp = 0

    @property
    def network(self):
        """
        Returns the current network path.

        Returns:
            str: The current network path.
        """
        return self.__network_path

    def _ensure_file_exists(self, filepath):
        """
        Ensures that the specified file exists by creating it if necessary.

        Parameters:
            filepath (str): The path to the file to check.

        Raises:
            Exception: If there is an error creating the file.
        """
        if not os.path.exists(filepath):  # Check if file does not exist
            try:
                with open(filepath, "w", encoding="utf-8") as f:  # Open file in write mode
                    f.write("")  # Create an empty file
            except Exception as e:
                print(f"Fehler beim Erstellen der Datei: {e}")
                exit(1)  # Exit the program with an error code

    def load_file(self, filepath):
        """
        Loads the content of a file.

        Parameters:
            filepath (str): The path to the file to load.

        Returns:
            str: The content of the file.

        Raises:
            FileNotFoundError: If the file does not exist.
        """
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    
    def changes_in_network(self):
        """
        Checks for changes in the network file since the last check.

        Returns:
            bool: True if the network file has been changed, False otherwise.
        """
        try:
            current_timestamp = os.path.getmtime(self.__network_path)  # Get the current last-modified timestamp of the file 
            return current_timestamp != self._last_checked_timestamp                
        except FileNotFoundError:
            self._ensure_file_exists(self.__network_path)
            self._last_checked_timestamp = 0
            return True  # Consider file creation a 'change'

    def load_network_file(self):
        """
        Loads the content of the network file.

        Returns:
            str: The content of the network file.
        """
        self._last_checked_timestamp = os.path.getmtime(self.__network_path)
        return self.load_file(self.__network_path)

    def load_json(self, filepath):
        """
        Loads the content of a JSON file.

        Parameters:
            filepath (str): The path to the JSON file to load.

        Returns:
            dict: The content of the JSON file.

        Raises:
            FileNotFoundError: If the file does not exist.
        """
        if not filepath:
            return {}
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    def append_network(self, text):
        """
        Appends text to the network file.

        Parameters:
            text (str): The text to append to the network file.

        Raises:
            FileNotFoundError: If the network file does not exist.
        """
        with open(self.__network_path, "a", encoding="utf-8") as f:
            f.write(text)

    def save_file(self, filepath, text):
        """
        Saves the text to the specified file.

        Parameters:
            filepath (str): The path to the file to save.
            text (str): The text to save to the file.

        Returns:
            str: The path to the saved file.

        Raises:
            FileNotFoundError: If the file does not exist.
        """
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





