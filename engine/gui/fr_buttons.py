from tkinter import ttk


class ButtonsFrame(ttk.Frame):
    """
    A frame for all the different buttons.
    """

    submit_mode_bts = []
    input_mode_bts = []
    display_mode_bts = []
    overlay_bts = []

    lbl_activate = "🔟→🔤"
    lbl_deactivate = "🔤→🔟"

    def __init__(self, master, flow, transform_gui):
        """
        Initialize the ButtonsFrame.

        Parameters:
            master: The parent widget.
            flow: The flow controller for the application.
        """
        super().__init__(master)
        self.flow = flow
        self.transform_gui = transform_gui

        # Button to enforce a reload of the file content
        self.btn_network_reload = ttk.Button(self, text="Aktualisieren", command=self.flow.network_reload)  # Create button to apply filter
        self.btn_network_reload.grid(row=0, column=0, sticky="news", pady=5)  # Place button in grid
        
        # Toggle button to switch between buttons and textfield
        button = ttk.Button(self, text="", command=lambda: self.transform_gui("bt/text"))
        button.grid(row=1, column=0, sticky="news", pady=5)
        ButtonsFrame.submit_mode_bts.append(button)
        
        # Toggle button to switch automatic decoding on/off
        button = ttk.Button(self, text="", command=lambda: self.transform_gui("decode"))
        button.grid(row=2, column=0, sticky="news", pady=5)
        ButtonsFrame.display_mode_bts.append(button)
        
        # Toggle button to switch automatic encoding on/off
        button = ttk.Button(self, text="", command=lambda: self.transform_gui("encode"))
        button.grid(row=3, column=0, sticky="news", pady=5)
        ButtonsFrame.input_mode_bts.append(button)

        # Toggle overlay button
        button = ttk.Button(self, text="💡Journal", command=lambda: self.transform_gui("overlay"))
        button.grid(row=4, column=0, sticky="news", pady=5)
        ButtonsFrame.overlay_bts.append(button)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)

    @staticmethod
    def label_submit(textfield):
        """
        Label the submit-mode buttons based on the current mode.

        Parameters:
            textfield: Whether the textfield is active or not.
        """
        for button in ButtonsFrame.submit_mode_bts:
            button.config(text="📝→🔘\n\nKnöpfe\nnutzen" if textfield else "🔘→📝\n\nTextfeld\nnutzen")

    @staticmethod
    def label_display(active):
        """
        Label the display-mode buttons based on the current mode.

        Parameters:
            active: Whether the automatic decoding is active or not.
        """
        title = "📖 Monitor:"
        label = f"{title}\n{ButtonsFrame.lbl_deactivate}\n\nDekodierung\ndeaktivieren" if active else f"{title}\n{ButtonsFrame.lbl_activate}\n\nDekodierung\naktivieren"
        for button in ButtonsFrame.display_mode_bts:
            button.config(text=label)

    @staticmethod
    def label_input(active):
        """
        Label the input-mode buttons based on the current mode.

        Parameters:
            active: Whether the automatic encoding is active or not.
        """
        title = "📝 Eingabe:"
        label = f"{title}\n{ButtonsFrame.lbl_deactivate}\n\nKodierung\ndeaktivieren" if active else f"{title}\n{ButtonsFrame.lbl_activate}\n\nKodierung\naktivieren"
        for button in ButtonsFrame.input_mode_bts:
            button.config(text=label)

