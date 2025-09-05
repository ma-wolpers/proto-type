import tkinter as tk
from tkinter import ttk

from . import ButtonsFrame

class OverlayFrame(ttk.Frame):
    """
    An overlay frame that displays the journal and buttons.
    """
    def __init__(self, master, flow, transform):
        """
        Initialize the OverlayFrame.

        Parameters:
            master: The parent widget.
        """
        super().__init__(master)

        self.journal_frame = JournalFrame(self)
        self.journal_frame.grid(row=0, column=0, padx=10, pady=10)

        self.buttons_overlayframe = ButtonsFrame(self, flow, transform)  # Create frame for buttons
        self.buttons_overlayframe.grid(row=0, column=1, rowspan=8, sticky="news", padx=5, pady=5)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def initialize_locked_achievements(self, locked_ach):
        """
        Initialize the locked achievements tree view.

        Parameters:
            locked_ach: The list of locked achievements to display.
        """
        self.journal_frame.initialize_locked_achievements(locked_ach)

    def unlock_achievement(self, ach):
        """
        Unlock an achievement and update the GUI.

        Parameters:
            ach: The achievement to unlock.
        """
        self.journal_frame.unlock_achievement(ach)

    def update_on(self, data):
        """
        Update the overlay frame with new data.

        Parameters:
            data: The new data to display.
        """
        self.journal_frame.update_on(data)



class JournalFrame(ttk.Frame):
    """
    A frame that displays the journal (currently: achievement-related information).
    """
    def __init__(self, master):
        """
        Initialize the JournalFrame.

        Parameters:
            master: The parent widget.
        """
        super().__init__(master)

        # XP bar
        self.xp_bar = ttk.Progressbar(master, orient="horizontal", length=200, mode="determinate")
        self.xp_bar.grid(row=0, column=0, padx=10, pady=10)
        self.XP_label = ttk.Label(master, text="EP: "+str(self.xp_bar['value'])+"/max")
        self.XP_label.grid(row=1, column=0, sticky="w")
    
        # Unlocked achievements list
        self.unlocked_achievements_label = ttk.Label(master, text="Freigeschaltete Erfolge:")
        self.unlocked_achievements_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.unlocked_achievements_list = tk.Listbox(master)
        self.unlocked_achievements_list.grid(row=3, column=0, padx=10, pady=5, sticky="ew")

        # Locked achievements list (Treeview)
        self.locked_achievements_label = ttk.Label(master, text="Offene Erfolge:")
        self.locked_achievements_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.locked_achievements_tree = ttk.Treeview(master, columns=("Beschreibung", "EP"), show="headings")
        self.locked_achievements_tree.heading("Beschreibung", text="Beschreibung")
        self.locked_achievements_tree.heading("EP", text="EP")
        self.locked_achievements_tree.column("Beschreibung", width=200)
        self.locked_achievements_tree.column("EP", width=50)
        self.locked_achievements_tree.grid(row=5, column=0, padx=10, pady=5, sticky="ew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Initialize the XP values
        self.xp_max = 100  # Maximum XP value
        self.xp_value = 0  # Current XP value


    def initialize_locked_achievements(self, locked_ach):
        """
        Initialize the locked achievements tree view.

        Parameters:
            locked_ach: The list of locked achievements to display.
        """
        self.locked_achievements_tree.delete(*self.locked_achievements_tree.get_children())  # Clear the treeview
        for ach in locked_ach:
            self.locked_achievements_tree.insert("", "end", iid=ach.title, values=(ach.descr, ach.xp))  # Insert the achievement into the treeview

    def unlock_achievement(self, ach):
        """
        Unlock an achievement and update the GUI.
        """
        self.unlocked_achievements_list.insert(tk.END, f"{ach.title} - {ach.descr} ({ach.xp} EP)")
        if self.locked_achievements_tree.exists(ach.title):
            self.locked_achievements_tree.delete(ach.title)

    def update_on(self, data):
        """
        Update the overlay frame with new data.

        Parameters:
            data: The new data to display.
        """
        if "xp" in data:
            self.xp_value = data["xp"]
            self.xp_bar['value'] = self.xp_value*100/self.xp_max
        if "xp_max" in data:
            self.xp_max = data["xp_max"]
            self.XP_label.config(text=f"EP: {self.xp_value}/{self.xp_max}")
        if "achievements" in data:
            if "locked" in data["achievements"]:
                locked_achievements = data["achievements"]["locked"]
                self.initialize_locked_achievements(locked_achievements)
            if "unlocked" in data["achievements"]:
                unlocked_achievements = data["achievements"]["unlocked"]
                self.unlocked_achievements_list.delete(0, tk.END)
                for ach in unlocked_achievements:
                    self.unlocked_achievements_list.insert(tk.END, f"{ach.title} - {ach.descr} ({ach.xp} EP)")
