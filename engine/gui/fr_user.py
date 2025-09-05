from tkinter import ttk

class UserFrame(ttk.Frame):
    """
    A frame that displays user-related information.
    """
    def __init__(self, master):
        """
        Initialize the UserFrame.

        Parameters:
            master: The parent widget.
        """
        super().__init__(master)
        
        # User label
        self.username_label = ttk.Label(self, text="Benutzer: ")
        self.username_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
        
        # Level label
        self.lvl_label = ttk.Label(self, text="Level: 0")
        self.lvl_label.grid(row=0, column=1, sticky="news")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def update_on(self, data):
        """
        Update the user information displayed in the frame.

        Parameters:
            data (dict): A dictionary containing user information.
        """
        if "username" in data:
            self.username_label.config(text=f"Benutzer: {data.get('username', 'Unbekannt')}")
        if "level" in data:
            self.lvl_label.config(text=f"Level: {data.get('level', {}).get('id', 0)}")