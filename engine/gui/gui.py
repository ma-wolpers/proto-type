import tkinter as tk  # Import tkinter for GUI elements
from tkinter import ttk, filedialog, simpledialog  # Import specific tkinter modules


class ProtoGUI:
    """
    The main GUI class for the ProtoType application.

    Manages the layout, widgets, and user interactions.
    """
    def __init__(self):
        """
        Initialize the GUI default values.
        """
        # Initialize the texts and labels
        self.label_binary = "(0en oder 1en)"  # Label for binary input field
        self.label_words = "(kodierbar)"  # Label for words input field
        
        # Initialize the overlay visibility
        self.overlay_visible = False
    
    def build(self, flow):
        """
        Build the GUI components.

        Parameters:
            flow: The flow controller for the application.
        """
        self.flow = flow # controller of program flow
        
        # Initialize the application
        self.__root = tk.Tk() # Create the main window
        self.__root.title("ProtoType - Messenger")  # Set window title
        self.__root.geometry("1000x600")
        self.__root.resizable(True, True)

        # Fill the GUI
        self._create_menu()  # Create menu bar
        self._create_widgets()  # Create UI widgets
        self.__configure_grid()  # Configure grid layout

    def start(self):
        """
        Start the GUI main loop.
        """
        self.periodic_refresh()
        self.__root.mainloop() # necessary to keep the application 'open' and running

    def periodic_refresh(self):
        """
        Periodically check for changes in the network file.
        """
        self.flow.network_reload(checkforchanges = True) # Check if the file has been modified since the last check

        self.__root.after(1000, self.periodic_refresh)  # Schedule the method to be called again after 1000 milliseconds (1 second)

    def initialize_locked_achievements(self, locked_ach):
        """
        Initialize the locked achievements tree view.

        Parameters:
            locked_ach: The list of locked achievements to display.
        """
        self.overlay_frame.initialize_locked_achievements(locked_ach)

    def unlock_achievement(self, ach):
        """
        Unlock an achievement and update the GUI.
        """
        self.overlay_frame.unlock_achievement(ach)


    # LAYOUT
    def _create_menu(self):
        """
        Create the menu bar and its items.
        """
        self.__root.option_add('*tearOff', False) # Disable tear-off menus

        # Create menu bar
        menu_bar = tk.Menu(self.__root)  # Create a menu bar
        self.__root.config(menu=menu_bar)  # Set the menu bar to the root window
        menu_bar.config(bg="white", bd=40)  # Set the background color of the menu bar

        # "Optionen" menu
        options_menu = tk.Menu(menu_bar)  # Create "Optionen" menu
        menu_bar.add_cascade(label="Optionen", menu=options_menu)  # Add "Optionen" menu to the menu bar
        options_menu.add_command(label="Adressierung anzeigen/verstecken", command=self.toggle_addressing)  # Add command to toggle filters
        options_menu.add_command(label="Paketierung anzeigen/verstecken", command=self.toggle_pckg)  # Add command to toggle signatures
        options_menu.add_command(label="Kodierung anzeigen/verstecken", command=self.toggle_code_dict)  # Add command to toggle code dictionary

        # "Einstellungen" menu
        settings_menu = tk.Menu(menu_bar)  # Create "Einstellungen" menu
        menu_bar.add_cascade(label="Einstellungen", menu=settings_menu)  # Add "Einstellungen" menu to the menu bar
        settings_menu.add_command(label="Netz wechseln", command=self.flow.network_change)  # Add command to change binary file
        settings_menu.add_command(label="Fortschritt speichern", command=self.choose_allsave)  # Add command to save configuration
        settings_menu.add_command(label="Fortschritt laden", command=self.choose_allload)  # Add command to load configuration
        settings_menu.add_command(label="Einstellungen exportieren", command=self.choose_configexport)  # Add command to save configuration
        settings_menu.add_command(label="Einstellungen importieren", command=self.choose_configimport)  # Add command to load configuration

    def _create_widgets(self):
        """
        Create the GUI widgets.
        """
        from . import ProgressFrame, ToolFrame,DisplayFrame, UserFrame, SubmitFrame, ButtonsFrame, OverlayFrame

        # Main frame for dynamic resizing
        self._main_frame = ttk.Frame(self.__root)  # Create main frame
        self._main_frame.grid(row=0, column=0, sticky="news")  # Place main frame in grid


        ##### COLUMN 1 #####

        # Challenge information
        self.progress_frame = ProgressFrame(self._main_frame, self.flow)
        self.progress_frame.grid(row=0, rowspan=2, column=1, sticky="news", padx=5, pady=5)

        # Warning label
        self.warning_label = ttk.Label(self._main_frame, text="", foreground="red")
        self.warning_label.grid(row=2, column=1, sticky="ws")

        # Tools (eof, code dict, signatures, ...)
        self.tools_frame = ToolFrame(self._main_frame, self.flow, self.show_message, self.show_warning)
        self.tools_frame.grid(row=3, rowspan=3, column=1, sticky="news", padx=5, pady=5)


        ##### COLUMN 2 #####

        # User information
        self.user_frame = UserFrame(self._main_frame)  # Create frame for user information
        self.user_frame.grid(row=0, column=2, sticky="news", padx=5, pady=5)

        # Diplays
        self.display_frame = DisplayFrame(self._main_frame, self.flow)  # Create frame for displays
        self.display_frame.grid(row=1, column=2, rowspan=4, sticky="news", padx=5, pady=5)
        
        # Submitting
        self.submit_frame = SubmitFrame(self._main_frame, self.flow, self.show_warning)  # Create frame for submitting
        self.submit_frame.grid(row=5, column=2, sticky="news", padx=5, pady=5)


        ##### COLUMN 0 #####

        # Buttons
        self.buttons_mainframe = ButtonsFrame(self._main_frame, self.flow, self.transform)  # Create frame for buttons
        self.buttons_mainframe.grid(row=0, column=0, rowspan=6, sticky="news", padx=5, pady=5)  # Place frame in grid



        ##### OVERLAY PANEL #####

        # Overlay frame for achievements and XP bar
        self.overlay_frame = OverlayFrame(self.__root, self.flow, self.transform)
        self.overlay_frame.place(relx=0, rely=0, relwidth=0.4, relheight=1)
        self.overlay_frame.lower()  # Initially hide the overlay
    

    def __configure_grid(self):
        """
        Configure the grid layout for the main frames.
        """
        self.col1size = 500
        self._main_frame.grid_columnconfigure(1, minsize=self.col1size)
        self._main_frame.grid_columnconfigure(2, minsize=400)
        self._main_frame.grid_columnconfigure(0, minsize=100)
        self._main_frame.grid_rowconfigure(0)  # Zeile 0 startet mit 100 Pixeln Höhe
        self._main_frame.grid_rowconfigure(5, minsize=150)  # Zeile 1 startet mit 200 Pixeln Höhe
        self.overlay_frame.grid_columnconfigure(0, minsize=280)
        self.progress_frame.grid_rowconfigure(0, minsize=150)
        


        """
        Right now I'm allowing the program to be resized.
        """

        # Configure fitting & resizing of the grid
        self.__root.grid_rowconfigure(0, weight=1)
        self.__root.grid_columnconfigure(0, weight=1)
        self._main_frame.grid_rowconfigure(0, weight=0)
        self._main_frame.grid_rowconfigure(1, weight=1)
        self._main_frame.grid_rowconfigure(2, weight=1)
        self._main_frame.grid_rowconfigure(3, weight=1)
        self._main_frame.grid_rowconfigure(4, weight=1)
        self._main_frame.grid_rowconfigure(5, weight=1)
        self._main_frame.grid_columnconfigure(0, weight=0)
        self._main_frame.grid_columnconfigure(1, weight=3)
        self._main_frame.grid_columnconfigure(2, weight=0)




    # PROMPTERS
    def choose_network(self):
        """
        Prompt the user to choose a network file.
        """
        newpath = filedialog.askopenfilename(filetypes=[("Netzwerk", "*.net")])  # Open file dialog
        self.flow.gui_change(data={"network":newpath})

    def choose_username(self):
        """
        Prompt the user to choose a username and a network file.
        """
        name = simpledialog.askstring("Benutzername", "Bitte gib einen Nutzernamen an: ")
        self.flow.gui_change(data={"username":name})

        # Direkt im Anschluss Netzwerkdatei abfragen
        netpath = filedialog.askopenfilename(
            title="Netzwerk auswählen",
            filetypes=[("Netzwerkdatei", "*.net"), ("Alle Dateien", "*")]
        )
        if netpath:
            self.flow.gui_change(data={"network":netpath})

    def choose_allload(self):
        """
        Prompt the user to choose a file to load all data.
        """
        filepath = filedialog.askopenfilename(filetypes=[("Benutzerdatei", "*.user")])  # Open file dialog
        self.flow.load_all(filepath)

    def choose_allsave(self):
        """
        Prompt the user to choose a file to save all data.
        """
        filepath = filedialog.asksaveasfilename(defaultextension=".user", filetypes=[("Benutzerdatei", "*.user")])
        self.flow.save_all(filepath)

    def choose_configimport(self):
        """
        Prompt the user to choose a configuration file to import.
        """
        filepath = filedialog.askopenfilename(filetypes=[("Konfiguration", "*.config")])  # Open file dialog
        self.flow.import_config(filepath)

    def choose_configexport(self):
        """
        Prompt the user to choose a configuration file to export.
        """
        filepath = filedialog.asksaveasfilename(defaultextension=".config", filetypes=[("Konfiguration", "*.config")])
        self.flow.export_config(filepath)
        



    # Communication with Flow

    def update(self, data={}):
        """
        Update the GUI elements based on the provided data.
        """
        if any(x in data for x in ("xp","xp_max","achievements")):
            self.overlay_frame.update_on(data)
        if any(x in data for x in ("username","level")):
            self.user_frame.update_on(data)
        if any(x in data for x in ("eol","code_length","code_text","filter","signature")):
            self.tools_frame.update_on(data)
        if any(x in data for x in ("level","challenge","chlg_bar")):
            self.progress_frame.update_on(data)



    # FORWARD to FRAME subclasses

    def start_fill_blanks(self, testdata):
        """
        Show the fill-in-the-blank test interface.

        Parameters:
            testdata (dict): The data for the fill-in-the-blank test.

        Called:
            flow.py check_progress(): when all challenges are completed
        """
        self.progress_frame.start_fill_blanks(testdata, self.col1size-10)

    def end_fill_blanks(self):
        """
        Hides the fill-in-the-blank test interface.

        Called:
            flow.py submit_answers(): when the user has submits their answers
        """
        self.progress_frame.end_fill_blanks()

    def display(self, content={}):
        """
        Display content in the appropriate text fields.

        Parameters:
            content (dict): The content to be displayed, with keys for each text field.
        """

        self.display_frame.display(content)
    
    def clear_input(self):
        """
        Clears the input field.

        Called:
            flow.py check_and_submit(): when the input has been submitted to the network
        """
        self.submit_frame.clear_input()




    # Warnings and messages

    def show_message(self, text="", warn=True): # Remove warning if valid
        """
        Shows a message in the warning label.

        Parameters:
            text (str): The message text to display.
            warn (bool): Whether the message is a warning (True) or a success message (False).
        """
        if text:
            if warn:
                self.warning_label.config(text="❌ "+text, foreground="red")
            else:
                self.warning_label.config(text="✅ "+text, foreground="green")
        else:
            self.warning_label.config(text="")
            
    def show_warning(self, args):
        """
        Shows a warning message in the warning label.

        Parameters:
            args (tuple): A tuple containing the warning title and message.
        """
        self.show_message(text=f"{args[0]}: {args[1]}")




    





    # Transforming the GUI

    def transform(self, mode, init=False):
        """
        Transforms the GUI elements based on the selected mode.

        Parameters:
            mode (str): The mode to switch to:
                - "bt/text": Switch between button and text field submission.
                - "decode": Toggle automatic decoding.
                - "encode": Toggle automatic encoding.
                - "overlay": Toggle overlay visibility.
            init (bool): Whether to initialize the mode (True) or toggle it (False).
        """
        if mode == "bt/text":
            self.toggle_submit(init)
        elif mode == "decode":
            self.toggle_decode(init)
        elif mode == "encode":
            self.toggle_encode(init)
        elif mode == "overlay":
            self.toggle_overlay()
        else:
            print(f"Achtung: Unbekannter GUI-Transformationsmodus! '{mode}'")

    def toggle_submit(self, init):
        """
        Toggles the submission field mode between binary buttons and text field.

        Parameters:
            init (bool): Whether to initialize the mode (True, default) or toggle it (False).
        """
        if init:
            self.mode_textfield = False # At the initialisation set to textfield
        else:
            self.mode_textfield = not self.mode_textfield # Toggle the mode
        
        self.submit_frame.input_mode(self.mode_textfield)

        from . import ButtonsFrame
        ButtonsFrame.label_submit(self.mode_textfield)

    def toggle_decode(self, init):
        """
        Switches the automatic decoding off or on.
        """
        decoding = self.flow.toggle_decode(init=init)
        from . import ButtonsFrame
        ButtonsFrame.label_display(decoding)

    def toggle_encode(self, init):
        """
        Tries to switch the automatic encoding off or on.
        """
        try:
            encoding = self.flow.toggle_encode(init=init)
            label = self.label_words if encoding else self.label_binary
            self.tools_frame.swap(encoding, label)
            self.submit_frame.relabel(label)
            from . import ButtonsFrame
            ButtonsFrame.label_input(encoding)
        except Warning as w:
            self.show_warning(w.args)
    
    def toggle_overlay(self):
        """
        Toggles the visibility of the journal frame.
        """
        self.overlay_visible = not self.overlay_visible
        if self.overlay_visible:
            self.overlay_frame.lift()
        else:
            self.overlay_frame.lower()

    def toggle_addressing(self):
        """
        Toggles the visibility of the addressing frame.
        """
        self.tools_frame.toggle_frame("address")

    def toggle_pckg(self):
        """
        Toggles the visibility of the packaging frame.
        """
        self.tools_frame.toggle_frame("pckg")

    def toggle_code_dict(self):
        """
        Toggles the visibility of the code dictionary frame.
        """
        self.tools_frame.toggle_frame("dict")

_gui = None
def get_gui():
    """
    Returns the singleton instance of ProtoGUI.
    If the instance does not exist, it creates a new one.

    Returns:
        ProtoGUI: The singleton instance of ProtoGUI.
    """
    global _gui
    if _gui is None:
        _gui = ProtoGUI()
    return _gui