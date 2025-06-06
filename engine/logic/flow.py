class ProtoFlow:
    def __init__(self, filemanager, settings, bicoder, filter, signature, stats, progress, gui):
        """
        Initialize the ProtoFlow class.

        Parameters:
            filemanager (FilesManager): The file manager instance.
            settings (ProtoSettings): The settings instance.
            bicoder (BinaryCoder): The binary coder instance.
            gui (ProtoGUI): The GUI instance.
        """
        self.filemanager = filemanager
        self.settings = settings
        self.bicoder = bicoder
        self.filter = filter
        self.signature = signature
        self.stats = stats
        self.progress = progress
        self.gui = gui
        

        # Initialize variables
        self.mode_binary = True  # Initialize the mode to binary
        self.overlay_visible = False  # Initialize the overlay visibility

        # Initialize the everythings
        self.gui.build(self)
        self.create_achievements()
        self.finish_setup()


    def create_achievements(self):
        """
        Create achievements and their conditions.
        """
        # Example achievements with descriptions and XP points
        self.achievements = {}
        ach = ProtoAchievement(name="First message sent", condition=lambda: self.stats.sentmsgcount() >= 1, descr="Send your first message.", xp=10)
        self.achievements[ach.title] = ach
        ach = ProtoAchievement(name="10 messages sent", condition=lambda: self.stats.sentmsgcount() >= 10, descr="Send 10 messages.", xp=20)
        self.achievements[ach.title] = ach
        ach = ProtoAchievement(name="First message encoded", condition=lambda: 0 >= 1, descr="Encode your first message.", xp=15)
        self.achievements[ach.title] = ach
        
        

    def finish_setup(self):
        self.xp_max = sum(ach.xp for ach in self.achievements.values())
        self.unlocked_achievements = []
        self.locked_achievements = list(self.achievements.values())
        self.update_xp_bar()
        self.gui.initialize_locked_achievements(self.locked_achievements)
        self.gui.choose_username()
        self.update_gui(on_keys=["guiprogress"])
        
        self.gui.toggle_textfield(init=True) # Initialize the input mode to buttons (including removal of the input field, labels and buttons)
        self.switch_mode(init=True) # Initialize the input field to binary (including removal of the words fields)

        ### LAST COMMAND TO RUN
        self.gui.start()


    

    # Network operations
    def network_reload(self, checkforchanges=False): #formerly load_file
        if checkforchanges:
            if not self.filemanager.changes_in_network():
                return
        try:
            content = self.filemanager.load_network_file()  # Load the file content
        except Exception as e:
            # Show an error message if loading fails
            self.gui.display({"display":f"Fehler beim Laden: {e}"})
            return
        
        # Update the binary display
        self.stats.update({"net_content":content})
        self.gui.display({"binary":content})

        textlines = self.bicoder.split_eol(content)

        # Decode the text lines if the mode is not binary
        if self.mode_binary:
            # If the mode is binary, simply filter the lines
            textlines = self.filter.filter_lines(textlines)
        else:
            # If the mode is not binary, decode the lines and filter them
            decoded_lines = []
            for line in textlines:
                # Decode each line of text
                text = self.bicoder.decode_text(line)
                if self.filter.check_text(text):
                    decoded_lines.append(text)
            textlines = decoded_lines
        # Join the filtered lines into a single text
        displaytext = "\n>".join(textlines)

        # Update the file display with the decoded text
        self.gui.display({"display":displaytext})

        # Apply bold formatting to 0s and 1s
        """ start_index = "1.0"
        if self.bicoder.code_dict: # Check if a code dictionary is available
            while True:
                start_index = self.gui.decoded_display.search("[01]", start_index, tk.END, regexp=True)
                if not start_index:
                    break
                end_index = f"{start_index} + 1 char"
                self.decoded_display.tag_add("bold", start_index, end_index)
                start_index = end_index """

    def network_send(self, binary_text): #formerly append_file
        self.stats.send_content(binary_text)  # inform the stats manager about the new message

        # Append the binary text to the file
        self.filemanager.append_network(binary_text)

        # Update history
        self.gui.display({"history":binary_text})

        # Update file content
        self.network_reload()

        # Check for achievements
        self.check_progress()

    def network_change(self):
        # Open a file dialog to select a new file
        filepath = self.gui.choose_network()
        if filepath:  # if a file was selected
            self.filemanager.update(network=filepath)
            # Set default file name to selected file name
            self.network_reload()  # Load the selected file content


    # Text handlers
    def check_and_submit(self, text):

        if not text:  # Check if the input field is empty
            self.gui.show_message("Kein Text eingegeben!")
            return
        
        # Check if only allowed characters are entered
        if self.mode_binary:
            if not all(c in {"0", "1"} for c in text):
                self.gui.show_message("Nur 0 und 1 erlaubt!")
                return
        self.gui.show_message()


        # Add signatures and eol
        text = self.signature.sign(text)
        text = self.bicoder.append_eol(text)
        # Encode the text line by line
        if not self.mode_binary:
            text = self.bicoder.encode_text(text)

        # Clear input field
        self.gui.clear_input()

        self.network_send(text)  # Append the binary text to the file

    # Achievement methods
    def check_progress(self):
        completed, chlgprogress = self.progress.check_challenge()
        if completed:
            self.gui.show_message("Challenge completed!", warn=False)
            self.stats.reset()
            if chlgprogress == 1: # all challenges completed
                testdata = self.progress.start_fb()
                self.gui.show_fill_blanks(testdata)
            else:
                self.update_gui(on_keys=["guiprogress"])
        self.gui.update(data={"chlg_bar":chlgprogress})
        for ach in self.achievements.values():
            if ach.condition() and (ach not in self.unlocked_achievements):
                self.unlocked_achievements.append(ach)
                self.locked_achievements.remove(ach)
                self.gui.unlock_achievement(ach)
                self.update_xp_bar()
    
    def submit_answers(self, submission):
        """
        Check the solution for the fill-in-the-blanks test.

        Parameters:
            submission (list(str)): The user's submission for the fill-in-the-blanks test.
        Returns:
            None
        """
        if self.progress.score_fb(submission):
            self.gui.show_message("Test bestanden!", warn=False)
        else:
            self.gui.show_message("Falsche Antwort! Löse die Challenges nochmal.", warn=True)
        self.gui.end_fill_blanks()
        self.update_gui(on_keys=["guiprogress"])
        
    def update_xp_bar(self):
        # Calculate total XP based on unlocked achievements
        total_xp = sum(ach.xp for ach in self.achievements.values() if ach in self.unlocked_achievements)
        xp = total_xp
        self.gui.update(data={"xp":total_xp,"xp_max":self.xp_max})


    # User functions
    def save_all(self, filepath):
        if filepath:
            newpath = self.settings.export_file(filepath) # Write the configuration data to the file
            self.gui.show_message(text="Konfiguration gespeichert!", warn=False)

    def load_all(self, filepath):
        if filepath:
            newkeys = self.settings.import_file(filepath)
            self.update_gui(on_keys=newkeys)
            self.gui.show_message(text="Konfiguration geladen!", warn=False)
            self.network_reload()


    # Configuration functions
    def export_config(self, filepath):
        if filepath: # Check if a file was selected
            newpath = self.settings.export_file(filepath, user=False) # Write the configuration data to the file
            self.gui.show_message(text="Konfiguration gespeichert!", warn=False) # Show a success message

    def import_config(self, filepath): # Load a configuration from a file
        if filepath:
            newkeys = self.settings.import_file(filepath, user=False)
            self.update_gui(on_keys=newkeys)
            self.gui.show_message(text="Konfiguration geladen!", warn=False) # Show a success message

    # Togglers
    def switch_mode(self, init=False):
        if init:
            self.mode_binary = True
            self.gui.adjust_tomode(self.mode_binary)
            return
        
        oldmode_is_binary = self.mode_binary
        olddata = self.settings.collect_data(["filter", "signature"])
        if oldmode_is_binary:
            newdata = self.bicoder.decode_data(olddata)
        else:
            newdata = self.bicoder.encode_data(olddata)
        
        self.mode_binary = not oldmode_is_binary # Toggle the mode, except at the initialisation: then set to binary
        self.settings.parse_data(newdata)
        self.gui.update(newdata)
        self.gui.adjust_tomode(self.mode_binary)
        self.network_reload()
    

    # GUI
    def gui_change(self, data={}):
        autosaved = self.settings.parse_data(data=data)
        self.update_gui(on_keys=list(data))
        if autosaved:
            self.gui.show_message (text="automatisch gespeichert", warn=False)
        if any(x in data for x in ["code_text","network","eol","filter","code_length"]):

            self.network_reload()
        self.settings.check_integrity(on_keys=list(data), for_binary=self.mode_binary)

    def update_gui(self, on_keys=[]):
        data = self.settings.collect_for_gui(keys=on_keys)
        self.gui.update(data) 
        
    


# Main function to run the application
def main():
    app = ProtoTypeApp() # Create the application instance

if __name__ == "__main__": # Check if the script is run directly
    main()
