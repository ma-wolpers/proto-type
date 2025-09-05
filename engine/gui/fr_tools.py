import tkinter as tk
from tkinter import ttk


class ToolFrame(ttk.Frame):
    """
    A frame that contains the tool settings (entry fields for various tools).
    """
    def __init__(self, master, flow, msg, warn):
        """
        Initialize the ToolFrame.

        Parameters:
            master: The parent widget.
            flow: The flow controller for the application.
            msg: The message display function.
            warn: The warning display function.
        """
        super().__init__(master)
        self.flow = flow
        self.msg_gui = msg
        self.warn_gui = warn

        self.pckg_frame = PckgFrame(self, flow, msg, warn)
        self.pckg_frame.grid(row=0, column=0, sticky="news")

        self.dict_frame = DictFrame(self, flow, msg, warn)
        self.dict_frame.grid(row=1, column=0, sticky="news")

        self.address_frame = AddressFrame(self, flow, msg, warn)
        self.address_frame.grid(row=2, column=0, sticky="new", pady=10)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def update_on(self, data):
        """
        Update the input fields based on the provided data.

        Parameters:
            data: The data to update the input fields with.
        """
        if any(x in data for x in ("eol", "code_length")):
            self.pckg_frame.update_on(data)
        if "code_text" in data:
            self.dict_frame.update_on(data)
        if any(x in data for x in ("filter", "signature")):
            self.address_frame.update_on(data)

    def relabel(self, label):
        """
        Relabel the input fields.

        Parameters:
            label (str): The new label for the input fields.
        """
        self.address_frame.relabel(label)

    ## VISIBILITY

    def toggle_frame(self, frame):
        """
        Toggle the visibility of the packaging frame.

        Parameters:
            frame (str): The name of the frame to toggle ("pckg", "dict", or "address").
        """
        if frame == "pckg":
            frame = self.pckg_frame
        elif frame == "dict":
            frame = self.dict_frame
        elif frame == "address":
            frame = self.address_frame
        else:
            print("Error: Unknown or unspecified frame to toggle:", frame)
        if frame.winfo_ismapped():
            frame.grid_remove()
        else:
            frame.grid()

def get_clean_text(tktext):
    """
    Get the clean text from a Tkinter Text widget.
    """
    return tktext.get("1.0", "end-1c")



class PckgFrame(ttk.Frame):
    """
    A frame that contains the packaging settings (entry fields for EOL and code length).
    """
    def __init__(self, master, flow, msg, warn):
        """
        Initialize the PckgFrame.

        Parameters:
            master: The parent widget.
            flow: The flow controller for the application.
            msg: The message display function.
            warn: The warning display function.
        """
        super().__init__(master)
        self.flow = flow
        self.msg_gui = msg
        self.warn_gui = warn
        self.eol_label = ttk.Label(self, text="Ende einer Nachricht:")
        self.eol_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.eol_entry = ttk.Entry(self)
        self.eol_entry.bind('<FocusOut>', self.notify_eol)
        self.eol_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
        self.code_length_label = ttk.Label(self, text="feste Code-Länge:")
        self.code_length_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.code_length_entry = ttk.Entry(self)
        self.code_length_entry.bind('<FocusOut>', self.notify_code_length)
        self.code_length_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

    def update_on(self, data):
        """
        Update the input fields based on the provided data.

        Parameters:
            data: The data to update the input fields with.
        """
        if "eol" in data:
            self.eol_entry.delete(0, tk.END)
            self.eol_entry.insert(0, data["eol"])
        if "code_length" in data:
            self.code_length_entry.delete(0, tk.END)
            cl = data["code_length"]
            if cl:
                self.code_length_entry.insert(0, cl)

    def notify_eol(self, event):
        """
        Notify the flow about the updated end-of-line (EOL) character.

        Parameters:
            event: The event that triggered the notification.
        """
        try:
            self.flow.gui_change(data={"eol":self.eol_entry.get()})
            self.msg_gui(text="Zeilenende aktualisiert", warn=False)
        except Warning as w:
            self.warn_gui(w.args)

    def notify_code_length(self, event):
        """
        Notify the flow about the updated code length.

        Parameters:
            event: The event that triggered the notification.
        """
        try:
            newlength = self.code_length_entry.get()
            try:
                code_length = int(newlength) if newlength else None
            except ValueError:
                raise Warning("Code-Länge","Bitte eine gültige Zahl eingeben.")
            self.flow.gui_change(data={"code_length":code_length})
            self.msg_gui(text="Code-Länge aktualisiert", warn=False)
        except Warning as w:
            self.warn_gui(w.args)



class DictFrame(ttk.Frame):
    """
    A frame that contains the dictionary settings (entry field for code dictionary).
    """
    def __init__(self, master, flow, msg, warn):
        """
        Initialize the DictFrame.

        Parameters:
            master: The parent widget.
            flow: The flow controller for the application.
            msg: The message display function.
            warn: The warning display function.
        """
        super().__init__(master)
        self.flow = flow
        self.msg_gui = msg
        self.warn_gui = warn
        self.code_label = ttk.Label(self, text="Wörterbuch (z.B. 'a=011, b=001'):")
        self.code_label.grid(row=0, column=0, sticky="nw")
        self.code_field = tk.Text(self, height=6)
        for event in ("<FocusOut>","<Return>", "<space>", ","):
            self.code_field.bind(event, self.notify_dict)
        self.code_field.grid(row=1, column=0, sticky="news")
   
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def update_on(self, data):
        """
        Update the input fields based on the provided data.

        Parameters:
            data: The data to update the input fields with.
        """
        if "code_text" in data:
            self.code_field.delete(1.0, tk.END)
            self.code_field.insert(tk.END, data["code_text"])

    def notify_dict(self, event):
        """
        Notify the flow about the updated dictionary.

        Parameters:
            event: The event that triggered the notification.
        """
        try:
            self.flow.gui_change(data={"code_text":get_clean_text(self.code_field)})
            self.msg_gui(text="Wörterbuch aktualisiert", warn=False)
        except Warning as w:
            self.warn_gui(w.args)



class AddressFrame(ttk.Frame):
    """
    A frame that contains the address settings (entry fields for sender and recipient addresses).
    """
    def __init__(self, master, flow, msg, warn):
        """
        Initialize the AddressFrame.

        Parameters:
            master: The parent widget.
            flow: The flow controller for the application.
            msg: The message display function.
            warn: The warning display function.
        """
        super().__init__(master, width=800, height=100)
        self.flow = flow
        self.msg_gui = msg
        self.warn_gui = warn
        self.filter_labels = {}
        self.filter_fields = {}
        self.signature_labels = {}
        self.signature_fields = {}
        
        self.label_binary = "(0en oder 1en)"
        self.label_words = "(kodierbar)"

        self.filter_label = ttk.Label(self, text="Filter "+self.label_binary+":")
        self.filter_label.grid(row=0, column=0, sticky="w")
        self.filter_starts_with_label = ttk.Label(self, text="Nachricht beginnt mit:")
        self.filter_starts_with_label.grid(row=1, column=0, sticky="w")
        self.filter_labels["starts"] = self.filter_starts_with_label
        self.filter_starts_entry = ttk.Entry(self)
        self.filter_starts_entry.bind('<FocusOut>', self.notify_filter)
        self.filter_starts_entry.grid(row=2, column=0, sticky="ew")
        self.filter_fields["starts"] = self.filter_starts_entry
        self.filter_ends_label = ttk.Label(self, text="Nachricht endet mit:")
        self.filter_ends_label.grid(row=3, column=0, sticky="w")
        self.filter_labels["ends"] = self.filter_ends_label
        self.filter_ends_entry = ttk.Entry(self)
        self.filter_ends_entry.bind('<FocusOut>', self.notify_filter)
        self.filter_ends_entry.grid(row=4, column=0, sticky="ew")
        self.filter_fields["ends"] = self.filter_ends_entry
        self.signature_label = ttk.Label(self, text="Signaturen: (nur Wörter?)")
        self.signature_label.grid(row=0, column=1, sticky="w")
        self.signature_start_label = ttk.Label(self, text="Anfangssignatur:")
        self.signature_start_label.grid(row=1, column=1, sticky="w")
        self.signature_labels["start"] = self.signature_start_label
        self.signature_start_entry = ttk.Entry(self)
        self.signature_start_entry.bind('<FocusOut>', self.notify_signature)
        self.signature_start_entry.grid(row=2, column=1, sticky="ew")
        self.signature_fields["start"] = self.signature_start_entry
        self.signature_end_label = ttk.Label(self, text="Endsignatur:")
        self.signature_end_label.grid(row=3, column=1, sticky="w")
        self.signature_labels["end"] = self.signature_end_label
        self.signature_end_entry = ttk.Entry(self)
        self.signature_end_entry.bind('<FocusOut>', self.notify_signature)
        self.signature_end_entry.grid(row=4, column=1, sticky="ew")
        self.signature_fields["end"] = self.signature_end_entry

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)


    def update_on(self, data):
        """
        Update the input fields based on the provided data.

        Parameters:
            data: The data to update the input fields with.
        """
        if "filter" in data:
            for mode in self.filter_fields:
                self.filter_fields[mode].delete(0, tk.END)
                self.filter_fields[mode].insert(0, data["filter"].get(mode,""))
        if "signature" in data:
            for mode in self.signature_fields:
                self.signature_fields[mode].delete(0, tk.END)
                self.signature_fields[mode].insert(0, data["signature"].get(mode,""))

    def notify_filter(self, event):
        """
        Notify the flow about the updated filter settings.

        Parameters:
            event: The event that triggered the notification.
        """
        filter = {}
        for mode in self.filter_fields:
            filter[mode] = self.filter_fields[mode].get()
        try:
            self.flow.gui_change(data = {"filter":filter})
            self.msg_gui(text="Filter aktualisiert", warn=False)
        except Warning as w:
            self.warn_gui(w.args)


    def notify_signature(self, event):
        """
        Notify the flow about the updated signature settings.

        Parameters:
            event: The event that triggered the notification.
        """
        signature = {}
        for mode in self.signature_fields:
            signature[mode] = self.signature_fields[mode].get()
        try:
            self.flow.gui_change(data = {"signature":signature})
            self.msg_gui(text="Signaturen aktualisiert", warn=False)
        except Warning as w:
            self.warn_gui(w.args)

    def relabel(self, label):
        """
        Relabel the input fields.

        Parameters:
            label (str): The new label for the input fields.
        """
        self.filter_label.config(text="Filter "+label+":")
        self.filter_starts_with_label.config(text="Nachricht beginnt mit:")
        self.filter_ends_label.config(text="Nachricht endet mit:")
        self.signature_label.config(text="Signaturen "+label+":")
        self.signature_start_label.config(text="Anfangssignatur:")
        self.signature_end_label.config(text="Endsignatur:")