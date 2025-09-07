import tkinter as tk
from tkinter import ttk, scrolledtext

class DisplayFrame(ttk.Frame):
    """
    A frame for all the different networks displays.
    """
    def __init__(self, master, flow):
        """
        Initialize the DisplayFrame.

        Parameters:
            master: The parent widget.
            flow: The flow controller for the application.
        """
        super().__init__(master)
        self.flow = flow
        # Notebook for tabs
        self.notebook = ttk.Notebook(self)  # Create notebook
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

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def display(self, content={}):
        """
        Display content in the appropriate text fields.

        Parameters:
            content (dict): The content to be displayed, with keys for each text field.
        """

        def insert(display, content, replace=True):
            """Insert content into a text field.
            
            Parameters:
                display: The text field to insert content into.
                content: The content to insert.
                replace (bool): Whether to replace existing content or append.
            """
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

