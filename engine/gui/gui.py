import tkinter as tk  # Import tkinter for GUI elements
from tkinter import ttk, scrolledtext, filedialog  # Import specific tkinter modules

from tkinter import font  # import for the fill-in-the-blank test

class ProtoGUI:
    def __init__(self):
        # Initialize the texts and labels
        self.label_binary = "(0en oder 1en)"  # Label for binary input field
        self.label_words = "(kodierbar)"  # Label for words input field

        # Initialize the XP values
        self.xp_max = 100  # Maximum XP value
        self.xp_value = 0  # Current XP value
        
        # Initialize the overlay visibility
        self.overlay_visible = False
    
    def build(self, flow):
        self.flow = flow # controller of program flow
        
        # Initialize the application
        self.__root = tk.Tk() # Create the main window
        self.__root.title("ProtoType - Messenger")  # Set window title
        self.__root.geometry("1000x600")
        self.__root.iconbitmap('./lib/favicon.ico')
        self.__root.resizable(1, 1)

        # Fill the GUI
        self._create_menu()  # Create menu bar
        self._create_widgets()  # Create UI widgets
        self.__configure_grid()  # Configure grid layout

    def start(self):
        self.periodic_refresh()
        self.__root.mainloop() # necessary to keep the application 'open' and running

    def periodic_refresh(self):
        self.flow.network_reload(checkforchanges = True) # Check if the file has been modified since the last check

        self.__root.after(1000, self.periodic_refresh)  # Schedule the method to be called again after 1000 milliseconds (1 second)

    def initialize_locked_achievements(self, locked_ach):
        self.locked_achievements_tree.delete(*self.locked_achievements_tree.get_children())  # Clear the treeview
        for ach in locked_ach:
            self.locked_achievements_tree.insert("", "end", iid=ach.title, values=(ach.descr, ach.xp))  # Insert the achievement into the treeview

    def unlock_achievement(self, ach):
        self.unlocked_achievements_list.insert(tk.END, f"{ach.title} - {ach.descr} ({ach.xp} XP)")
        if self.locked_achievements_tree.exists(ach.title):
            self.locked_achievements_tree.delete(ach.title)


    # LAYOUT
    def _create_menu(self):
        self.__root.option_add('*tearOff', False) # Disable tear-off menus

        # Create menu bar
        menu_bar = tk.Menu(self.__root)  # Create a menu bar
        self.__root.config(menu=menu_bar)  # Set the menu bar to the root window
        menu_bar.config(bg="white", bd=40)  # Set the background color of the menu bar

        # "Optionen" menu
        options_menu = tk.Menu(menu_bar)  # Create "Optionen" menu
        menu_bar.add_cascade(label="Optionen", menu=options_menu)  # Add "Optionen" menu to the menu bar
        options_menu.add_command(label="Adressierung aktivieren/deaktivieren", command=self.toggle_addressing)  # Add command to toggle filters
        options_menu.add_command(label="EOL aktivieren/deaktivieren", command=self.toggle_eol)  # Add command to toggle signatures
        options_menu.add_command(label="Code-Dictionary aktivieren/deaktivieren", command=self.toggle_code_dict)  # Add command to toggle code dictionary
        """ # Disable the filter, signature, and code dictionary toggles for now
        options_menu.entryconfigure("Filter aktivieren/deaktivieren", state="disabled")
        options_menu.entryconfigure("Signaturen aktivieren/deaktivieren", state="disabled")
        options_menu.entryconfigure("Code-Dictionary aktivieren/deaktivieren", state="disabled") """

        # "Einstellungen" menu
        settings_menu = tk.Menu(menu_bar)  # Create "Einstellungen" menu
        menu_bar.add_cascade(label="Einstellungen", menu=settings_menu)  # Add "Einstellungen" menu to the menu bar
        settings_menu.add_command(label="Netz wechseln", command=self.flow.network_change)  # Add command to change binary file
        settings_menu.add_command(label="Fortschritt speichern", command=self.choose_allsave)  # Add command to save configuration
        settings_menu.add_command(label="Fortschritt laden", command=self.choose_allload)  # Add command to load configuration
        settings_menu.add_command(label="Einstellungen exportieren", command=self.choose_configexport)  # Add command to save configuration
        settings_menu.add_command(label="Einstellungen importieren", command=self.choose_configimport)  # Add command to load configuration

    def _create_widgets(self):
        # Main frame for dynamic resizing
        self._main_frame = ttk.Frame(self.__root)  # Create main frame
        self._main_frame.grid(row=0, column=0, sticky="news")  # Place main frame in grid




        ##### COLUMN 1 #####

        # Lvl information

        # Challenge information
        self.progress_frame = ttk.Frame(self._main_frame)  # Create frame for progress information
        self.progress_frame.grid(row=0, rowspan=2, column=1, sticky="news", padx=5, pady=5)

        def placefr_progress(self):
            # Level title
            self.lvl_title = ttk.Label(self.progress_frame, text="Level Titel")
            self.lvl_title.grid(row=0, column=0, sticky="w")

            # Help button for current challenge
            self.challenge_help = ttk.Button(self.progress_frame, text="Hilfe", command=lambda: "self.show_help")
            self.challenge_help.grid(row=0, column=1, sticky="e")

            # Title of current challenge
            self.challenge_title = ttk.Label(self.progress_frame, text="Aktuelle Herausforderung")
            self.challenge_title.grid(row=1, columnspan=2, column=0, sticky="w")

            # Fill-in-the-blank area
            self.fill_blank_frame = ttk.Frame(self.progress_frame)
            self.fill_blank_frame.grid(row=2, column=0, columnspan=2, sticky="ew")
            self.fill_blank_frame.grid_remove()  # Initially hide the fill-in-the-blank area

            # Button to submit the fill-in-the-blank answer
            self.btn_submit_fill_blank = ttk.Button(self.progress_frame, text="Absenden", command=self.submit_answers)
            self.btn_submit_fill_blank.grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
            self.btn_submit_fill_blank.grid_remove()  # Initially hide the button            

            # Description of current challenge
            self.challenge_description = ttk.Label(self.progress_frame, text="Noch keine Beschreibung vorhanden.")
            self.challenge_description.grid(row=2, column=0, columnspan=2, sticky="w")

            # Progress bar of current challenge
            self.progress_bar = ttk.Progressbar(self.progress_frame, orient="horizontal", length=200, mode="determinate")
            self.progress_bar.grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
            self.progress_bar["maximum"] = 100
        placefr_progress(self)

        
        # Warning label
        self.warning_label = ttk.Label(self._main_frame, text="", foreground="red")
        self.warning_label.grid(row=2, column=1, sticky="ws")



        ## TOOLS AREA ##
        self.tools_frame = ttk.Frame(self._main_frame)  # Create frame for tools
        self.tools_frame.grid(row=3, rowspan=3, column=1, sticky="news", padx=5, pady=5)  # Place frame in grid

        # EOL area
        self.eol_frame = ttk.Frame(self.tools_frame)  # Create frame for EOL
        self.eol_frame.grid(row=0, column=0, sticky="news")  # Place frame in grid

        def placefr_eol(self):
            # EOL Binary Code Input
            self.eol_label = ttk.Label(self.eol_frame, text="Zeilenende:")
            self.eol_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
            self.eol_entry = ttk.Entry(self.eol_frame)
            wdgt = self.eol_entry
            wdgt.bind('<FocusOut>', self.notify_eol)
            wdgt.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

            # Binary Code length input
            self.code_length_label = ttk.Label(self.eol_frame, text="feste Code-Länge:")
            self.code_length_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
            self.code_length_entry = ttk.Entry(self.eol_frame)
            wdgt = self.code_length_entry
            wdgt.bind('<FocusOut>', self.notify_code_length)
            wdgt.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        placefr_eol(self)

        # Code dictionary input area
        self.dict_frame = ttk.Frame(self.tools_frame)  # Create frame for code dictionary
        self.dict_frame.grid(row=1, column=0, sticky="news")  # Place frame in grid
        
        def placefr_dict(gui):

            # Code dictionary area
            gui.code_label = ttk.Label(gui.dict_frame, text="Code-Dictionary (z.B. 'a=011, b=001'):")  # Create label for code dictionary
            gui.code_label.grid(row=0, column=0, sticky="nw")  # Place label in grid
            gui.code_field = tk.Text(gui.dict_frame, height=6)  # Create text widget for code dictionary
            wdgt = gui.code_field
            # Update the dict if any button is pressed
            for event in ("<FocusOut>","<Return>", "<space>", ","):
                wdgt.bind(event, gui.notify_dict)
            wdgt.grid(row=1, column=0, sticky="news")  # Place text widget in grid
        placefr_dict(self)

        # Address area
        self.address_frame = ttk.Frame(self.tools_frame, width=800, height=100)  # Create frame for addresses
        self.address_frame.grid(row=2, column=0, sticky="new", pady=10)  # Place frame in grid

        def placefr_address(gui):
            gui.filter_label = ttk.Label(gui.address_frame, text="Filter "+gui.label_binary+":")  # Create label for filters
            gui.filter_label.grid(row=0, column=0, sticky="w")  # Place label in grid

            # Filters area
            gui.filter_labels = {}
            gui.filter_fields = {}

            gui.filter_starts_with_label = ttk.Label(gui.address_frame, text="Nachricht beginnt mit:")
            wdgt = gui.filter_starts_with_label
            wdgt.grid(row=1, column=0, sticky="w")
            gui.filter_labels["starts"]=wdgt

            wdgt = ttk.Entry(gui.address_frame)
            wdgt.bind('<FocusOut>', gui.notify_filter)
            wdgt.grid(row=2, column=0, sticky="ew")
            gui.filter_fields["starts"]=wdgt

            wdgt = ttk.Label(gui.address_frame, text="Nachricht endet mit:")
            wdgt.grid(row=3, column=0, sticky="w")
            gui.filter_labels["ends"]=wdgt

            wdgt = ttk.Entry(gui.address_frame)
            wdgt.bind('<FocusOut>', gui.notify_filter)
            wdgt.grid(row=4, column=0, sticky="ew")
            gui.filter_fields["ends"]=wdgt

            # Signature area
            gui.signature_labels = ttk.Label(gui.address_frame, text="Signaturen: (nur Wörter?)")
            gui.signature_labels.grid(row=0, column=1, sticky="w")

            gui.signature_labels = {}
            gui.signature_fields = {}

            wdgt = ttk.Label(gui.address_frame, text="Anfangssignatur:")
            wdgt.grid(row=1, column=1, sticky="w")
            gui.signature_labels["start"]=wdgt

            wdgt = gui.signature_fields_start_entry = ttk.Entry(gui.address_frame)  # Create entry widget for start signature
            wdgt.bind('<FocusOut>', gui.notify_signature)
            wdgt.grid(row=2, column=1, sticky="ew")
            gui.signature_fields["start"]=wdgt
            wdgt = ttk.Label(gui.address_frame, text="Endsignatur:")
            wdgt.grid(row=3, column=1, sticky="w")
            gui.signature_labels["end"]=wdgt
            wdgt = gui.signature_fields_end_entry = ttk.Entry(gui.address_frame)  # Create entry widget for end signature
            wdgt.bind('<FocusOut>', gui.notify_signature)
            wdgt.grid(row=4, column=1, sticky="ew")
            gui.signature_fields["end"]=wdgt
        placefr_address(self)



        ##### COLUMN 2 #####

        # User information
        self.user_info_frame = ttk.Frame(self._main_frame)  # Create frame for user information
        self.user_info_frame.grid(row=0, column=2, sticky="news", padx=5, pady=5)  # Place frame in grid

        def placefr_user_infos(self):
            # User label
            self.username_label = ttk.Label(self.user_info_frame, text="Benutzer: ")
            self.username_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
            
            # Level label
            self.lvl_label = ttk.Label(self.user_info_frame, text="Level: 0")
            self.lvl_label.grid(row=0, column=1, sticky="news")
        placefr_user_infos(self)

        # Diplays
        self.display_frame = ttk.Frame(self._main_frame)  # Create frame for displays
        self.display_frame.grid(row=1, column=2, rowspan=4, sticky="news", padx=5, pady=5)
        
        def placefr_display(self):
            # Notebook for tabs
            self.notebook = ttk.Notebook(self.display_frame)  # Create notebook
            self.notebook.grid(row=0, column=0, sticky="nsew")  # Place notebook in grid

            # Tab 1: Monitor
            self.tab_monitor = ttk.Frame(self.notebook)  # Create tab for monitor
            self.notebook.add(self.tab_monitor, text="Monitor")  # Add tab to notebook
            self.monitor_display = scrolledtext.ScrolledText(self.tab_monitor, wrap=tk.WORD, state="disabled", height=20, width=40)  # Create scrolled text widget for file display
            self.monitor_display.grid(row=0, column=0, sticky="nsew")  # Place file display widget in grid

            # Define a tag for bold formatting
            self.monitor_display.tag_configure("bold", font=("TkDefaultFont", 10, "bold"))

            # Tab 2: Binary content
            self.tab_binaryfile = ttk.Frame(self.notebook)  # Create tab for binary content
            self.notebook.add(self.tab_binaryfile, text="Binärinhalt")  # Add tab to notebook
            self.binaryfile_display = scrolledtext.ScrolledText(self.tab_binaryfile, wrap=tk.WORD, state="disabled", height=20, width=40)  # Create scrolled text widget for binary display
            self.binaryfile_display.grid(row=0, column=0, sticky="nsew")  # Place binary display widget in grid

            # Tab 3: History
            self.tab_history = ttk.Frame(self.notebook)  # Create tab for history
            self.notebook.add(self.tab_history, text="Historie")  # Add tab to notebook
            self.history_display = scrolledtext.ScrolledText(self.tab_history, wrap=tk.WORD, state="disabled", height=20, width=40)  # Create scrolled text widget for history display
            self.history_display.grid(row=0, column=0, sticky="nsew")  # Place history display widget in grid
        placefr_display(self)

        # Submitting
        self.submit_frame_buttons = ttk.Frame(self._main_frame)  # Create frame for submitting
        #(bd=2, bg="lightblue")
        self.submit_frame_buttons.grid(row=5, column=2, sticky="news", padx=5, pady=5)
        self.submit_frame_field = ttk.Frame(self._main_frame)  # Create frame for submitting
        self.submit_frame_field.grid(row=5, column=2, sticky="news", padx=5, pady=5)

        def placefr_submit(self):
            ### Button Frame mit Buttons für 0 und 1
            self.btn_zero = ttk.Button(self.submit_frame_buttons, text="0", command=lambda: self.flow.network_send("0"))  # Create button to insert "0" into the file
            self.btn_zero.grid(row=0, column=0, sticky="news", pady=5)
            self.btn_one = ttk.Button(self.submit_frame_buttons, text="1", command= lambda: self.flow.network_send("1")) # Create button to insert "1" into the file
            self.btn_one.grid(row=0, column=1, sticky="news", pady=5)


            ### Field Frame mit Textfeld für Eingabe und Absenden-Button
            # Submit button to send text to file (Enter key also sends text)
            self.btn_send = ttk.Button(self.submit_frame_field, text="Absenden", command=self.submit_text)  # Create button to send text
            self.btn_send.grid(row=0, column=0, sticky="ew", pady=5)

            # Input label for new text
            self.input_label = ttk.Label(self.submit_frame_field, text="Text eingeben "+self.label_binary+":")
            self.input_label.grid(row=1, column=0, sticky="w")
            # Input field for new text
            wdgt = self.input_field = tk.Text(self.submit_frame_field, height=5, width=30)
            wdgt.bind("<Return>", self.on_enter)
            wdgt.grid(row=2, column=0, sticky="ew")
        placefr_submit(self)



        ##### COLUMN 0 #####

        # Buttons
        self.buttons_frame = ttk.Frame(self._main_frame)  # Create frame for buttons
        self.buttons_frame.grid(row=0, column=0, rowspan=6, sticky="news", padx=5, pady=5)  # Place frame in grid
        self.switch_mode_buttons = []
        self.xp_buttons = []
        self.toggle_textfield_buttons = []

        def _placefr_buttons(self, master):
            # Button to enforce a reload of the file content
            self.btn_network_reload = ttk.Button(master, text="Reload", command=self.flow.network_reload)  # Create button to apply filter
            self.btn_network_reload.grid(row=0, column=0, sticky="", pady=5)  # Place button in grid
            
            # Toggle button to switch between buttons and textfield
            button = ttk.Button(master, text="", command=self.toggle_textfield)
            button.grid(row=1, column=0, sticky="", pady=5)
            self.toggle_textfield_buttons.append(button)
            
            # Toggle button to switch between binary and words
            button = ttk.Button(master, text="", command=self.try_switch_mode)
            button.grid(row=2, column=0, sticky="", pady=5)
            self.switch_mode_buttons.append(button)

            # Toggle overlay button
            button = ttk.Button(master, text="Open XP", command=self.toggle_overlay)
            button.grid(row=3, column=0, sticky="", pady=5)
            self.xp_buttons.append(button)
        _placefr_buttons(self, self.buttons_frame)



        ##### OVERLAY PANEL #####

        # Overlay frame for achievements and XP bar
        self.overlay_frame = ttk.Frame(self.__root)
        self.overlay_frame.place(relx=0, rely=0, relwidth=0.4, relheight=1)
        self.overlay_frame.lower()  # Initially hide the overlay

        # XP and Achievements
        self.xp_frame = ttk.Frame(self.overlay_frame)
        self.xp_frame.grid(row=0, column=0, padx=10, pady=10)

        def placefr_xp(self, master):
            # XP bar
            self.xp_bar = ttk.Progressbar(master, orient="horizontal", length=200, mode="determinate")
            self.xp_bar.grid(row=0, column=0, padx=10, pady=10)
            self.XP_label = ttk.Label(master, text="XP: "+str(self.xp_bar['value'])+"/max")
            self.XP_label.grid(row=1, column=0, sticky="w")
        
            # Unlocked achievements list
            self.unlocked_achievements_label = ttk.Label(master, text="Unlocked Achievements:")
            self.unlocked_achievements_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
            self.unlocked_achievements_list = tk.Listbox(master)
            self.unlocked_achievements_list.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

            # Locked achievements list (Treeview)
            self.locked_achievements_label = ttk.Label(master, text="Locked Achievements:")
            self.locked_achievements_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
            self.locked_achievements_tree = ttk.Treeview(master, columns=("Description", "XP"), show="headings")
            self.locked_achievements_tree.heading("Description", text="Description")
            self.locked_achievements_tree.heading("XP", text="XP")
            self.locked_achievements_tree.column("Description", width=200)
            self.locked_achievements_tree.column("XP", width=50)
            self.locked_achievements_tree.grid(row=5, column=0, padx=10, pady=5, sticky="ew")
        placefr_xp(self, self.xp_frame)

        # Buttons
        self.buttonsoverlay_frame = ttk.Frame(self.overlay_frame)  # Create frame for buttons
        self.buttonsoverlay_frame.grid(row=0, column=1, rowspan=4, sticky="nsew", padx=5, pady=5)  # Place frame in grid

        _placefr_buttons(self, self.buttonsoverlay_frame)

    def __configure_grid(self):
        self.col1size = 500
        self._main_frame.grid_columnconfigure(1, minsize=self.col1size)
        self._main_frame.grid_columnconfigure(2, minsize=400)
        self._main_frame.grid_columnconfigure(0, minsize=100)
        self._main_frame.grid_rowconfigure(0)  # Zeile 0 startet mit 100 Pixeln Höhe
        self._main_frame.grid_rowconfigure(5, minsize=150)  # Zeile 1 startet mit 200 Pixeln Höhe
        self.overlay_frame.grid_columnconfigure(0, minsize=280)
        self.progress_frame.grid_rowconfigure(2, minsize=150)
        
        
        
        """ Right now I'm allowing the program to be resized.
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
        # button frame = mainframe column 0
        self.buttons_frame.grid_rowconfigure(0, weight=1)
        self.buttons_frame.grid_rowconfigure(1, weight=1)
        self.buttons_frame.grid_rowconfigure(2, weight=1)
        self.buttons_frame.grid_rowconfigure(3, weight=1)
        self.buttons_frame.grid_columnconfigure(0, weight=1)
        # progress frame = mainframe column 1, row 0-1
        self.progress_frame.grid_rowconfigure(0, weight=1)
        self.progress_frame.grid_rowconfigure(1, weight=1)
        self.progress_frame.grid_rowconfigure(2, weight=1)
        self.progress_frame.grid_rowconfigure(3, weight=1)
        self.progress_frame.grid_columnconfigure(0, weight=1)
        self.progress_frame.grid_columnconfigure(1, weight=0)
        # tool frame = mainframe column 1, row 3-5
        self.tools_frame.grid_rowconfigure(0, weight=1)
        self.tools_frame.grid_rowconfigure(1, weight=1)
        self.tools_frame.grid_rowconfigure(2, weight=1)
        self.tools_frame.grid_columnconfigure(0, weight=1)
        # eol frame = tool row 0
        self.eol_frame.grid_rowconfigure(0, weight=1)
        self.eol_frame.grid_rowconfigure(1, weight=1)
        self.eol_frame.grid_columnconfigure(0, weight=1)
        self.eol_frame.grid_columnconfigure(1, weight=0)
        # dict frame = tool row 1
        self.dict_frame.grid_rowconfigure(0, weight=1)
        self.dict_frame.grid_rowconfigure(1, weight=1)
        self.dict_frame.grid_columnconfigure(0, weight=1)
        # address frame = tool row 2
        self.address_frame.grid_rowconfigure(0, weight=1)
        self.address_frame.grid_rowconfigure(1, weight=1)
        self.address_frame.grid_rowconfigure(2, weight=1)
        self.address_frame.grid_rowconfigure(3, weight=1)
        self.address_frame.grid_rowconfigure(4, weight=1)
        self.address_frame.grid_columnconfigure(0, weight=1)
        self.address_frame.grid_columnconfigure(1, weight=0)
        # user infos = mainframe column 2, row 0
        self.user_info_frame.grid_rowconfigure(0, weight=1)
        self.user_info_frame.grid_columnconfigure(0, weight=1)
        # display frame = mainframe column 2, row 1
        self.display_frame.grid_rowconfigure(0, weight=1)
        self.display_frame.grid_columnconfigure(0, weight=1)
        # submit button frame = mainframe column 2, row 2
        self.submit_frame_buttons.grid_rowconfigure(0, weight=1)
        self.submit_frame_buttons.grid_columnconfigure(0, weight=1)
        self.submit_frame_buttons.grid_columnconfigure(1, weight=1)
        # submit field frame = mainframe column 2, row 2
        self.submit_frame_field.grid_rowconfigure(0, weight=1)
        self.submit_frame_field.grid_rowconfigure(1, weight=1)
        self.submit_frame_field.grid_rowconfigure(2, weight=1)
        self.submit_frame_field.grid_columnconfigure(0, weight=1)
        # overlay frame
        self.overlay_frame.grid_rowconfigure(0, weight=1)
        self.overlay_frame.grid_columnconfigure(0, weight=1)





    # PROMPTERS
    def choose_network(self):
        newpath = filedialog.askopenfilename(filetypes=[("Netzwerk", "*.net")])  # Open file dialog
        self.flow.gui_change(data={"network":newpath})

    def choose_username(self):
        name = tk.simpledialog.askstring("Benutzername", "Bitte gib einen Nutzernamen an: ")  # Open file dialog
        self.flow.gui_change(data={"username":name})

    def choose_allload(self):
        filepath = filedialog.askopenfilename(filetypes=[("Benutzerdatei", "*.user")])  # Open file dialog
        self.flow.load_all(filepath)

    def choose_allsave(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".user", filetypes=[("Benutzerdatei", "*.user")])
        self.flow.save_all(filepath)

    def choose_configimport(self):
        filepath = filedialog.askopenfilename(filetypes=[("Konfiguration", "*.config")])  # Open file dialog
        self.flow.import_config(filepath)

    def choose_configexport(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".config", filetypes=[("Konfiguration", "*.config")])
        self.flow.export_config(filepath)
        



    # Communication with Flow

    def update(self, data={}):
        if "username" in data:
            username = data["username"]
            self.username_label.config(text=f"Benutzer: {username}")
        if "xp" in data:
            self.xp_value = data["xp"]
            self.xp_bar['value'] = self.xp_value*100/self.xp_max
        if "xp_max" in data:
            self.xp_max = data["xp_max"]
            self.XP_label.config(text=f"XP: {self.xp_value}/{self.xp_max}")
        if "achievements" in data:
            if "locked" in data["achievements"]:
                locked_achievements = data["achievements"]["locked"]
                self.initialize_locked_achievements(locked_achievements)
            if "unlocked" in data["achievements"]:
                unlocked_achievements = data["achievements"]["unlocked"]
                self.unlocked_achievements_list.delete(0, tk.END)
                for ach in unlocked_achievements:
                    self.unlocked_achievements_list.insert(tk.END, f"{ach.title} - {ach.descr} ({ach.xp} XP)")
        if "filter" in data:
            for mode in self.filter_fields:
                self.filter_fields[mode].delete(0, tk.END)
                self.filter_fields[mode].insert(0, data["filter"].get(mode,""))
        if "signature" in data:
            for mode in self.signature_fields:
                self.signature_fields[mode].delete(0, tk.END)
                self.signature_fields[mode].insert(0, data["signature"].get(mode,""))
        if "code_length" in data:
            self.code_length_entry.delete(0, tk.END)
            cl = data["code_length"]
            if cl:
                self.code_length_entry.insert(0, cl)
        if "eol" in data:
            self.eol_entry.delete(0, tk.END)
            self.eol_entry.insert(0, data["eol"])
        if "code_text" in data:
            self.code_field.delete("1.0", tk.END)
            self.code_field.insert(tk.END, data["code_text"])
        if "level" in data:
            self.lvl_label.config(text=f"Level: {data['level']['id']}")
            self.lvl_title.config(text=data['level']['title'])
        if "challenge" in data:
            self.challenge_title.config(text=data["challenge"]['title'])
            self.challenge_description.config(text=data["challenge"]['descr'])
        if "chlg_bar" in data:
            self.progress_bar.config(value=data["chlg_bar"])

    def notify_eol(self, event):
        try:
            self.flow.gui_change(data={"eol":self.eol_entry.get()})
            self.show_message(text="Zeilenende aktualisiert", warn=False)
        except Warning as w:
            self.show_warning(w.args)

    def notify_code_length(self, event):
        try:
            newlength = self.code_length_entry.get()
            try:
                code_length = int(newlength) if newlength else None
            except ValueError:
                raise Warning("Code-Länge","Bitte eine gültige Zahl eingeben.")
            self.flow.gui_change(data={"code_length":code_length})
            self.show_message(text="Code-Länge aktualisiert", warn=False)
        except Warning as w:
            self.show_warning(w.args)

    def get_clean_text(tktext):
        return tktext.get("1.0", "end-1c")

    def notify_dict(self, event):
        try:
            self.flow.gui_change(data={"code_text":ProtoGUI.get_clean_text(self.code_field)})
            self.show_message(text="Wörterbuch aktualisiert", warn=False)
        except Warning as w:
            self.show_warning(w.args)

    def notify_filter(self, event):
        filter = {}
        for mode in self.filter_fields:
            filter[mode] = self.filter_fields[mode].get()
        try:
            self.flow.gui_change(data = {"filter":filter})
            self.show_message(text="Filter aktualisiert", warn=False)
        except Warning as w:
            self.show_warning(w.args)

    def notify_signature(self, event):
        signature = {}
        for mode in self.signature_fields:
            signature[mode] = self.signature_fields[mode].get()
        try:
            self.flow.gui_change(data = {"signature":signature})
            self.show_message(text="Signaturen aktualisiert", warn=False)
        except Warning as w:
            self.show_warning(w.args)
    




    # Fill in the blank test
    def show_fill_blanks(self, testdata):
        """
        Zeigt den Lückentext-Bereich an und versteckt die Beschreibung und den Fortschrittsbalken.
        Parameters:
            testdata (dict): Ein Dictionary mit den Daten für den Lückentext, das die Schlüssel "text_parts" und "options" enthält.
        """
        self.challenge_description.grid_remove()  # Hide the description label
        self.progress_bar.grid_remove()  # Hide the progress bar
        self.fill_blank_frame.grid()
        self.btn_submit_fill_blank.grid()  # Show the submit button

        # empty the fill-in-the-blank area
        for widget in self.fill_blank_frame.winfo_children():
            widget.destroy()
        
        self.comboboxes = self.create_fill_in_the_blank(self.fill_blank_frame, testdata["text_parts"], testdata["options"], frame_width=self.col1size)

    @staticmethod
    def create_fill_in_the_blank(text_frame, text_parts, options, frame_width):
        """
        Erstellt den Lückentext mit Comboboxen.
        :param text_parts: Liste der Textabschnitte (vor und nach den Lücken).
        :param options: Liste der Auswahlmöglichkeiten für jede Lücke.
        :param frame_width: Maximale Breite des Frames in Pixeln.
        """
        comboboxes = []

        # Schriftart des Labels
        label_font = font.nametofont("TkDefaultFont")

        current_row = 0
        current_column = 0
        remaining_width = frame_width  # Verfügbare Breite in der aktuellen Zeile

        def place_text_in_lines(text, font, max_width, starting_width):
            """
            Platziert den Text in Zeilen, die in den Frame passen. Dabei ist die erste Zeile bereits angefangen, daher also nicht in voller Breite verfügbar.
            :param text: Der Text, der platziert werden soll.
            :param font: Schriftart des Textes.
            :param max_width: Maximale Breite in Pixeln.
            :param starting_width: Verfügbare Breite in der aktuellen Zeile.
            """
            lines = []
            avaliable_width = starting_width
            current_line = ""
            for word in text.split():
                if font.measure(current_line + " " + word) <= avaliable_width:
                    current_line += " " + word
                else:
                    lines.append(current_line)
                    current_line = word
                    avaliable_width = max_width
            lines.append(current_line)
            return lines

        # Frame für die erste Zeile
        current_line_frame = ttk.Frame(text_frame)
        current_line_frame.grid(row=current_row, column=0, sticky="w", padx=0, pady=0)

        for i, part in enumerate(text_parts):
            lines = place_text_in_lines(part, label_font, remaining_width, remaining_width)
            for n, line_text in enumerate(lines):
                label = ttk.Label(current_line_frame, text=line_text)
                label.grid(row=0, column=current_column, padx=0, pady=0)
                current_column += 1

                #last line needs no line break
                if n == len(lines) - 1:
                    remaining_width -= label_font.measure(line_text)  # Verbleibende Breite aktualisieren
                    break
                
                # Zeilenumbruch
                current_row += 1
                current_column = 0
                remaining_width = frame_width

                # Neues Frame für die nächste Zeile
                current_line_frame = ttk.Frame(text_frame)
                current_line_frame.grid(row=current_row, column=0, sticky="w", padx=0, pady=0)


            # Combobox für die Lücke (falls Optionen vorhanden sind)
            if i < len(options):
                combobox_width = max(len(op) for op in options[i])  # Breite der Combobox berechnen

                if combobox_width > remaining_width:
                    # Zeilenumbruch, wenn die Combobox nicht mehr passt
                    current_row += 1
                    current_column = 0
                    remaining_width = frame_width

                    # Neues Frame für die nächste Zeile
                    current_line_frame = ttk.Frame(text_frame)
                    current_line_frame.grid(row=current_row, column=0, sticky="w", padx=0, pady=0)

                # Combobox erstellen
                combobox = ttk.Combobox(current_line_frame, values=options[i], state="readonly", width=combobox_width)
                combobox['font'] = label_font
                combobox.grid(row=0, column=current_column, padx=0, pady=0)
                comboboxes.append(combobox)
                
                current_column += 1
                remaining_width -= combobox_width
    
        # Passe das Gridlayout an
        text_frame.grid_columnconfigure(0, weight=1)
        for i in range(current_row + 1):
            text_frame.grid_rowconfigure(i, weight=1)

        return comboboxes

    def submit_answers(self):
        """
        Übergibt die Antworten an die Flow-Klasse.
        """
        answers = [combobox.get() for combobox in self.comboboxes]
        self.flow.submit_answers(answers)

    def end_fill_blanks(self):
        """
        Schließt den Lückentext-Bereich und zeigt die Beschreibung und den Fortschrittsbalken wieder an.
        """
        self.fill_blank_frame.grid_remove()
        for combobox in self.comboboxes:
            combobox.destroy()
        self.comboboxes = []
        self.fill_blank_frame.grid_remove()

        self.challenge_description.grid()
        self.progress_bar.grid()
    
    # TEXT FIELDS

    def display(self, content={}):
        
        def insert(display, content, replace=True):
            display.config(state="normal")
            if replace:
                display.delete("1.0", tk.END)
            display.insert(tk.END, content)
            display.config(state="disabled")
            display.yview(tk.END)  # Scroll to the end of the text field

        if "binary" in content:
            insert(self.binaryfile_display, content=content["binary"], replace=True)
        if "display" in content:
            insert(self.monitor_display, content=content["display"], replace=True)
        if "history" in content:
            insert(self.history_display, content=content["history"], replace=False)

    def clear_input(self):
        self.input_field.delete("1.0", tk.END)








    # Warnings and messages

    def show_message(self, text="", warn=True): # Remove warning if valid
        if text:
            if warn:
                self.warning_label.config(text="❌ "+text, foreground="red")
            else:
                self.warning_label.config(text="✅ "+text, foreground="green")
        else:
            self.warning_label.config(text="")
            
    def show_warning(self, args):
        self.show_message(text=f"{args[0]}: {args[1]}")





    # Event handlers

    def on_enter(self, event):
        if event.state & 0x1:  # Check if Shift is pressed
            return  # Keep normal line break function
        self.submit_text()
        return "break"  # Prevent a new line from being created
    
    def submit_text(self):
        try:
            self.flow.check_and_submit(ProtoGUI.get_clean_text(self.input_field))  # Send message
        except Warning as w:
            self.show_warning(w.args)





    # Togglers

    def toggle_textfield(self, init=False):
        if init:
            self.mode_textfield = False # At the initialisation set to textfield
        else:
            self.mode_textfield = not self.mode_textfield # Toggle the mode
        if self.mode_textfield:
            self.submit_frame_buttons.grid_remove()
            self.submit_frame_field.grid()
            for button in self.toggle_textfield_buttons:
                button.config(text="-> Knöpfe")
        else:
            self.submit_frame_field.grid_remove()
            self.submit_frame_buttons.grid()
            for button in self.toggle_textfield_buttons:
                button.config(text="-> Feld")

    def try_switch_mode(self):
        try:
            self.flow.switch_mode()
        except Warning as w:
            self.show_warning(w.args)

    def adjust_tomode(self, binary):
        if binary:
            #self.filter_entry_words.grid_remove()
            self.filter_label.config(text="Filter "+self.label_binary+":")
            #self.filter_entry_binary.grid()
            self.input_label.config(text="Text eingeben "+self.label_binary+":")
            for button in self.switch_mode_buttons:
                button.config(text="-> Wörter")
        else:
            #self.filter_entry_binary.grid_remove()
            self.filter_label.config(text="Filter "+self.label_words+":")
            #self.filter_entry_words.grid()
            self.input_label.config(text="Text eingeben "+self.label_words+":")
            for button in self.switch_mode_buttons:
                button.config(text="-> Binär")
    
    def toggle_overlay(self):
        self.overlay_visible = not self.overlay_visible
        if self.overlay_visible:
            self.overlay_frame.lift()
            for button in self.xp_buttons:
                button.config(text="Schließe XP")
        else:
            self.overlay_frame.lower()
            for button in self.xp_buttons:
                button.config(text="Zeige XP")

    def toggle_addressing(self): # Toggle the visibility of the filters area
        if self.address_frame.winfo_ismapped(): # Check if the filters frame is visible
            self.address_frame.grid_remove() # Hide the filters frame
        else: # If the filters frame is hidden
            self.address_frame.grid() # Show the filters frame

    def toggle_eol(self): # Toggle the visibility of the signatures area
        if self.eol_frame.winfo_ismapped(): # Check if the signatures frame is visible
            self.eol_frame.grid_remove() # Hide the signatures frame
        else: # If the signatures frame is hidden
            self.eol_frame.grid() # Show the signatures frame

    def toggle_code_dict(self): # Toggle the visibility of the code dictionary area
            if self.dict_frame.winfo_ismapped(): # Check if the code dictionary frame is visible
                self.dict_frame.grid_remove() # Hide the code dictionary frame
            else: # If the code dictionary frame is hidden
                self.dict_frame.grid() # Show the code dictionary frame

