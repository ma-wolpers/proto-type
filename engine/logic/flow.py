from . import bicoder, filemanager, filter, signature, stats, progress, settings, Achievement as ProtoAchievement
from .. import gui

class ProtoFlow:
    def __init__(self):
        """
        Initialize the ProtoFlow class.
        """
        # Initialize variables
        self.mode_binary = True  # Initialize the mode to binary
        self.overlay_visible = False  # Initialize the overlay visibility

        # Initialize the everythings
        self.create_achievements()


    def create_achievements(self):
        """
        Create achievements and their conditions.
        """
        # Example achievements with descriptions and XP points
        self.achievements = {}
        ach = ProtoAchievement(name="First message sent", condition=lambda: stats().sentmsgcount() >= 1, descr="Send your first message.", xp=10)
        self.achievements[ach.title] = ach
        ach = ProtoAchievement(name="10 messages sent", condition=lambda: stats().sentmsgcount() >= 10, descr="Send 10 messages.", xp=20)
        self.achievements[ach.title] = ach
        ach = ProtoAchievement(name="First message encoded", condition=lambda: 0 >= 1, descr="Encode your first message.", xp=15)
        self.achievements[ach.title] = ach
        
        

    def run(self):
        """
        Starts the main program loop.
        """
        self.xp_max = sum(ach.xp for ach in self.achievements.values())
        self.unlocked_achievements = []
        self.locked_achievements = list(self.achievements.values())
        self.update_xp_bar()
        _gui = gui()
        _gui.initialize_locked_achievements(self.locked_achievements)
        _gui.choose_username()
        self.update_gui(on_keys=["guiprogress"])
        
        _gui.toggle_textfield(init=True) # Initialize the input mode to buttons (including removal of the input field, labels and buttons)
        self.switch_mode(init=True) # Initialize the input field to binary (including removal of the words fields)

        ### LAST COMMAND TO RUN
        _gui.start()


    

    # Network operations
    def network_reload(self, checkforchanges=False): #formerly load_file
        """
        Updates the displayed network content with the latest setting changes.

        Parameters:
            checkforchanges (bool): Whether to check for changes in the network file before reloading.
        """
        _filemanager = filemanager()
        if checkforchanges:
            if not _filemanager.changes_in_network():
                return
        _gui = gui()
        try:
            content = _filemanager.load_network_file()  # Load the file content
        except Exception as e:
            # Show an error message if loading fails
            _gui.display({"display":f"Fehler beim Laden: {e}"})
            return
        
        # Update the binary display
        stats().update({"net_content":content})
        _gui.display({"binary":content})

        _bicoder = bicoder()
        textlines = _bicoder.split_eol(content)

        # Decode the text lines if the mode is not binary
        if self.mode_binary:
            # If the mode is binary, simply filter the lines
            textlines = filter().filter_lines(textlines)
        else:
            # If the mode is not binary, decode the lines and filter them
            decoded_lines = []
            for line in textlines:
                # Decode each line of text
                text = _bicoder.decode_text(line)
                if filter().check_text(text):
                    decoded_lines.append(text)
            textlines = decoded_lines
        # Join the filtered lines into a single text
        displaytext = "\n>".join(textlines)

        # Update the file display with the decoded text
        _gui.display({"display":displaytext})

        # Apply bold formatting to 0s and 1s
        """ start_index = "1.0"
        if _bicoder.code_dict: # Check if a code dictionary is available
            while True:
                start_index = _gui.decoded_display.search("[01]", start_index, tk.END, regexp=True)
                if not start_index:
                    break
                end_index = f"{start_index} + 1 char"
                self.decoded_display.tag_add("bold", start_index, end_index)
                start_index = end_index """

    def network_send(self, binary_text): #formerly append_file
        """
        Sends the binary text to the network.

        Parameters:
            binary_text (str): The binary text to send.
        """
        stats().send_content(binary_text)  # inform the stats manager about the new message

        # Append the binary text to the file
        filemanager().append_network(binary_text)

        # Update history
        gui().display({"history":binary_text})

        # Update file content
        self.network_reload()

        # Check for achievements
        self.check_progress()

    def network_change(self):
        """
        Changes the network file to a new file selected by the user.
        """
        # Open a file dialog to select a new file
        filepath = gui().choose_network()
        if filepath:  # if a file was selected
            filemanager().update(network=filepath)
            # Set default file name to selected file name
            self.network_reload()  # Load the selected file content


    # Text handlers
    def check_and_submit(self, text):
        """
        Checks the submitted text for validity and sends it to the network.

        Parameters:
            text (str): The text to check and submit.
        """
        _gui = gui()
        if not text:  # Check if the input field is empty
            _gui.show_message("Kein Text eingegeben!")
            return
        
        # Check if only allowed characters are entered
        if self.mode_binary:
            if not all(c in {"0", "1"} for c in text):
                _gui.show_message("Nur 0 und 1 erlaubt!")
                return
        _gui.show_message()


        # Add signatures and eol
        _bicoder = bicoder()
        text = signature().sign(text)
        text = _bicoder.append_eol(text)
        # Encode the text line by line
        if not self.mode_binary:
            text = _bicoder.encode_text(text)

        # Clear input field
        _gui.clear_input()

        self.network_send(text)  # Append the binary text to the file

    # Achievement methods
    def check_progress(self):
        """
        Checks the progress of the current challenge and sends updates to the GUI.
        """
        _progress = progress()
        completed, chlgprogress = _progress.check_challenge()
        _gui = gui()
        if completed:
            _gui.show_message("Challenge completed!", warn=False)
            stats().reset()
            if chlgprogress == 1: # all challenges completed
                testdata = _progress.start_fb()
                _gui.show_fill_blanks(testdata)
            else:
                self.update_gui(on_keys=["guiprogress"])
        _gui.update(data={"chlg_bar":chlgprogress})
        for ach in self.achievements.values():
            if ach.condition() and (ach not in self.unlocked_achievements):
                self.unlocked_achievements.append(ach)
                self.locked_achievements.remove(ach)
                _gui.unlock_achievement(ach)
                self.update_xp_bar()
    
    def submit_answers(self, submission):
        """
        Check the solution for the fill-in-the-blanks test.

        Parameters:
            submission (list(str)): The user's submission for the fill-in-the-blanks test.
        """
        _gui = gui()
        if progress().score_fb(submission):
            _gui.show_message("Test bestanden!", warn=False)
        else:
            _gui.show_message("Falsche Antwort! Löse die Challenges nochmal.", warn=True)
        _gui.end_fill_blanks()
        self.update_gui(on_keys=["guiprogress"])
        
    def update_xp_bar(self):
        """
        Updates the XP bar in the GUI.
        """
        # Calculate total XP based on unlocked achievements
        total_xp = sum(ach.xp for ach in self.achievements.values() if ach in self.unlocked_achievements)
        xp = total_xp
        gui().update(data={"xp":total_xp,"xp_max":self.xp_max})


    # User functions
    def save_all(self, filepath):
        """
        Saves all user data to the specified file.

        Parameters:
            filepath (str): The path to the file where user data will be saved.
        """
        if filepath:
            newpath = settings().export_file(filepath) # Write the configuration data to the file
            gui().show_message(text="Konfiguration gespeichert!", warn=False)

    def load_all(self, filepath):
        """
        Loads all user data from the specified file.

        Parameters:
            filepath (str): The path to the file from which user data will be loaded.
        """
        if filepath:
            newkeys = settings().import_file(filepath)
            self.update_gui(on_keys=newkeys)
            gui().show_message(text="Konfiguration geladen!", warn=False)
            self.network_reload()


    # Configuration functions
    def export_config(self, filepath):
        """
        Exports the current configuration to a file.

        Parameters:
            filepath (str): The path to the file where the configuration will be saved.
        """
        if filepath: # Check if a file was selected
            newpath = settings().export_file(filepath, user=False) # Write the configuration data to the file
            gui().show_message(text="Konfiguration gespeichert!", warn=False) # Show a success message

    def import_config(self, filepath): # Load a configuration from a file
        """
        Imports a configuration from a file.

        Parameters:
            filepath (str): The path to the file from which the configuration will be loaded.
        """
        if filepath:
            newkeys = settings().import_file(filepath, user=False)
            self.update_gui(on_keys=newkeys)
            gui().show_message(text="Konfiguration geladen!", warn=False) # Show a success message

    # Togglers
    def switch_mode(self, init=False):
        """
        Switches the mode between binary and text.

        Parameters:
            init (bool): If True, initializes the mode to binary. If False (default), toggles the mode.
        """
        _gui = gui()
        if init:
            self.mode_binary = True
            _gui.adjust_tomode(self.mode_binary)
            return
        
        oldmode_is_binary = self.mode_binary
        olddata = settings().collect_data(["filter", "signature"])
        if oldmode_is_binary:
            newdata = bicoder().decode_data(olddata)
        else:
            newdata = bicoder().encode_data(olddata)
        
        self.mode_binary = not oldmode_is_binary # Toggle the mode, except at the initialisation: then set to binary
        settings().parse_data(newdata)
        _gui.update(newdata)
        _gui.adjust_tomode(self.mode_binary)
        self.network_reload()
    

    # GUI
    def gui_change(self, data={}):
        """
        Handles changes in the GUI and updates the internal state.

        Parameters:
            data (dict): The data containing the changes to be applied.
        """
        autosaved = settings().parse_data(data=data)
        self.update_gui(on_keys=list(data))
        if autosaved:
            gui().show_message (text="automatisch gespeichert", warn=False)
        if any(x in data for x in ["code_text","network","eol","filter","code_length"]):

            self.network_reload()
        settings().check_integrity(on_keys=list(data), for_binary=self.mode_binary)

    def update_gui(self, on_keys=[]):
        """
        Updates the GUI with the current state.
        """
        data = settings().collect_for_gui(keys=on_keys)
        gui().update(data) 