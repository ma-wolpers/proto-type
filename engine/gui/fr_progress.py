from tkinter import ttk

from tkinter import font  # import for the fill-in-the-blank test

class ProgressFrame(ttk.Frame):
    """
    A frame that displays the current challenge and its progress.
    """
    def __init__(self, master, flow):
        """
        Initialize the ProgressFrame.

        Parameters:
            master: The parent widget.
            flow: The flow controller for the application.
        """
        super().__init__(master)
        self.flow = flow
        # Level title
        self.lvl_title = ttk.Label(self, text="Level Titel")
        self.lvl_title.grid(row=0, column=0, sticky="w")

        # Help button for current challenge
        self.challenge_help = ttk.Button(self, text="Hilfe", command=lambda: "self.show_help")
        self.challenge_help.grid(row=0, column=1, sticky="nes")

        # Title of current challenge
        self.challenge_title = ttk.Label(self, text="Aktuelle Herausforderung")
        self.challenge_title.grid(row=1, columnspan=2, column=0, sticky="w")

        # Description of current challenge
        self.challenge_description = ttk.Label(self, text="Noch keine Beschreibung vorhanden.")
        self.challenge_description.grid(row=2, column=0, columnspan=2, sticky="w")

        # Progress bar of current challenge
        self.progress_bar = ttk.Progressbar(self, orient="horizontal", length=200, mode="determinate")
        self.progress_bar.grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
        self.progress_bar["maximum"] = 100

        # Fill-in-the-blank area
        self.fill_blank_frame = ttk.Frame(self)
        self.fill_blank_frame.grid(row=2, column=0, columnspan=2, sticky="ew")
        self.fill_blank_frame.grid_remove()  # Initially hide the fill-in-the-blank area

        # Button to submit the fill-in-the-blank answer
        self.btn_fbsubmit = ttk.Button(self, text="Absenden", command=self.submit_answers)
        self.btn_fbsubmit.grid(row=3, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
        self.btn_fbsubmit.grid_remove()  # Initially hide the button

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

    def update_on(self, data):
        if "level" in data:
            self.lvl_title.config(text=data['level']['title'])
        if "challenge" in data:
            self.challenge_title.config(text=data["challenge"]['title'])
            self.challenge_description.config(text=data["challenge"]['descr'])
        if "chlg_bar" in data:
            self.progress_bar.config(value=data["chlg_bar"])


    # Fill in the blank test
    def start_fill_blanks(self, testdata, width):
        """
        Show the fill-in-the-blank area and hide the description and progress bar.

        Called:
            gui.py show_fill_blanks(): when a fill-in-the-blank test is initiated

        Parameters:
            testdata (dict): A dictionary containing the data (text_parts and options) for the fill-in-the-blank test.
            width (int): The maximum width of the fill-in-the-blank area in pixels.
        """
        self.challenge_description.grid_remove()  # Hide the description label
        self.progress_bar.grid_remove()  # Hide the progress bar
        self.fill_blank_frame.grid()
        self.btn_fbsubmit.grid()  # Show the submit button

        # empty the fill-in-the-blank area
        for widget in self.fill_blank_frame.winfo_children():
            widget.destroy()

        self.comboboxes = self.create(self.fill_blank_frame, testdata["text_parts"], testdata["options"], frame_width=width)

    def submit_answers(self):
        """
        Collects the answers from the comboboxes and submits them to the flow.

        Called:
            button btn_fbsubmit: when the submit button is clicked
        """
        answers = [combobox.get() for combobox in self.comboboxes]
        self.flow.submit_answers(answers)

    def end_fill_blanks(self):
        """
        Closes the fill-in-the-blank area and shows the description and progress bar again.

        Called:
            flow.py end_fill_blanks(): when the fill-in-the-blank test is completed
        """
        self.fill_blank_frame.grid_remove()
        for combobox in self.comboboxes:
            combobox.destroy()
        self.comboboxes = []
        self.fill_blank_frame.grid_remove()

        self.challenge_description.grid()
        self.progress_bar.grid()

    @staticmethod
    def create(text_frame, text_parts, options, frame_width):
        """
        Create the fill-in-the-blank text with comboboxes.

        Parameters:
            text_frame (ttk.Frame): The frame containing the text.
            text_parts (list): List of text sections (before and after the blanks).
            options (list): List of options for each blank.
            frame_width (int): Maximum width of the frame in pixels.

            Returns:
                list: A list of comboboxes for the fill-in-the-blank areas.
        """
        comboboxes = []

        # Schriftart des Labels
        label_font = font.nametofont("TkDefaultFont")
        space_width = label_font.measure(" ")

        current_row = 0
        current_column = 0
        remaining_width = frame_width  # Verfügbare Breite in der aktuellen Zeile

        def place_text_in_lines(text, font, max_width, starting_width):
            """
            Places the text in lines that fit within the frame. The first line is already started, so it is not fully available.

            Parameters:
                text (str): The text to be placed.
                font (Font): The font of the text.
                max_width (int): Maximum width in pixels.
                starting_width (int): Available width in the current line.

            Returns:
                list: A list of lines with the placed text.
            """
            lines = []
            avaliable_width = starting_width
            current_line = ""
            for i, word in enumerate(text.split(" ")):
                if i != 0:
                    current_line += " "
                    avaliable_width -= space_width
                word_width = font.measure(word)
                if word_width <= avaliable_width:
                    current_line += word
                    avaliable_width -= word_width
                else:
                    lines.append(current_line)
                    current_line = word
                    avaliable_width = max_width - word_width
            lines.append(current_line)
            return lines, avaliable_width

        # Frame für die erste Zeile
        current_line_frame = ttk.Frame(text_frame)
        current_line_frame.grid(row=current_row, column=0, sticky="w", padx=0, pady=0)

        for i, part in enumerate(text_parts):
            lines, remaining_width = place_text_in_lines(part, label_font, frame_width, remaining_width)
            for n, line_text in enumerate(lines):
                label = ttk.Label(current_line_frame, text=line_text)
                label.grid(row=0, column=current_column, padx=0, pady=0)
                current_column += 1

                #last line needs no line break
                if n == len(lines) - 1:
                    break
                
                # Zeilenumbruch
                current_row += 1
                current_column = 0

                # Neues Frame für die nächste Zeile
                current_line_frame = ttk.Frame(text_frame)
                current_line_frame.grid(row=current_row, column=0, sticky="w", padx=0, pady=0)


            # Combobox für die Lücke (falls Optionen vorhanden sind)
            if i < len(options):
                combobox_width = max(label_font.measure(op) for op in options[i])  # Breite der Combobox berechnen
                actual_cb_width = combobox_width + 25

                if actual_cb_width > remaining_width:
                    # Zeilenumbruch, wenn die Combobox nicht mehr passt
                    current_row += 1
                    current_column = 0
                    remaining_width = frame_width

                    # Neues Frame für die nächste Zeile
                    current_line_frame = ttk.Frame(text_frame)
                    current_line_frame.grid(row=current_row, column=0, sticky="w", padx=0, pady=0)

                # Combobox erstellen
                combobox = ttk.Combobox(current_line_frame, values=options[i], state="readonly", width=combobox_width//8)
                combobox['font'] = label_font
                combobox.grid(row=0, column=current_column, padx=0, pady=0)
                comboboxes.append(combobox)
                
                current_column += 1
                remaining_width -= actual_cb_width

        # Passe das Gridlayout an
        text_frame.grid_columnconfigure(0, weight=1)
        for i in range(current_row + 1):
            text_frame.grid_rowconfigure(i, weight=1)

        return comboboxes
    
    
    