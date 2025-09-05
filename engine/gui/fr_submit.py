import tkinter as tk
from tkinter import ttk
from . import get_clean_text

class SubmitFrame(ttk.Frame):
    """
    A frame that contains fields and buttons for submitting data into the network.
    """
    def __init__(self, master, flow, warn):
        """
        Initialize the SubmitFrame.

        Parameters:
            master: The parent widget.
            flow: The flow controller for the application.
        """
        super().__init__(master)

        self.submit_frame_buttons = SubmitButtonsFrame(self, flow)
        self.submit_frame_buttons.grid(row=0, column=0, sticky="news", padx=5, pady=5)
        self.submit_frame_field = SubmitFieldFrame(self, flow, warn)
        self.submit_frame_field.grid(row=0, column=0, sticky="news", padx=5, pady=5)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def input_mode(self, textfield):
        """
        Sets the input mode of the submit frame.

        Parameters:
            textfield (bool): If True, displays the text field; otherwise, displays the buttons.
        """
        if textfield:
            self.submit_frame_buttons.grid_remove()
            self.submit_frame_field.grid()
        else:
            self.submit_frame_field.grid_remove()
            self.submit_frame_buttons.grid()

    def relabel(self, label):
        """
        Relabel the input field.

        Parameters:
            label (str): The new label for the input field.
        """
        self.submit_frame_field.relabel(label)

    def clear_input(self):
        """
        Clears the input field.
        """
        self.submit_frame_field.clear_input()


class SubmitButtonsFrame(ttk.Frame):
    """
    A frame that contains buttons for submitting "0"s or "1"s.
    """
    def __init__(self, master, flow):
        """
        Initialize the SubmitButtonsFrame.

        Parameters:
            master: The parent widget.
            flow: The flow controller for the application.
        """
        super().__init__(master)
        self.flow = flow

        # Create buttons
        self.submit_0_button = ttk.Button(self, text="0", command=lambda: self.submit("0"))
        self.submit_0_button.grid(row=0, column=0, sticky="news", padx=5, pady=5)

        self.submit_1_button = ttk.Button(self, text="1", command=lambda: self.submit("1"))
        self.submit_1_button.grid(row=0, column=1, sticky="news", padx=5, pady=5)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def submit(self, value):
        """
        Submit the given value.

        Parameters:
            value (str): The value to submit (0 or 1).
        """
        self.flow.network_send(value)


class SubmitFieldFrame(ttk.Frame):
    """
    A frame that contains a text field and a button to submit the content of the text field.
    """
    def __init__(self, master, flow, warn):
        """
        Initialize the SubmitFieldFrame.

        Parameters:
            master: The parent widget.
            flow: The flow controller for the application.
        """
        super().__init__(master)
        self.flow = flow
        self.warn_gui = warn

        # Submit button to send text to file (Enter key also sends text)
        self.btn_send = ttk.Button(self, text="Absenden", command=self.submit_text)  # Create button to send text
        self.btn_send.grid(row=0, column=0, sticky="ew", pady=5)

        # Input label for new text
        self.input_label = ttk.Label(self)
        self.input_label.grid(row=1, column=0, sticky="w")
        # Input field for new text
        wdgt = self.input_field = tk.Text(self, height=5, width=30)
        wdgt.bind("<Return>", self.on_enter)
        wdgt.grid(row=2, column=0, sticky="ew")

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)


    def on_enter(self, event):
        """
        Handles the Enter key event in the input field.
        If Shift is pressed, a normal line break is allowed.

        Parameters:
            event (tk.Event): The event object containing information about the key press.
        """
        if event.state & 0x1:  # Check if Shift is pressed
            return  # Keep normal line break function
        self.submit_text()
        return "break"  # Prevent a new line from being created
    
    def submit_text(self):
        """
        Submits the text from the input field to the flow.
        """
        try:
            self.flow.check_and_submit(get_clean_text(self.input_field))  # Send message
        except Warning as w:
            self.warn_gui(w.args)

    def relabel(self, label):
        """
        Sets the mode of the submit frame.

        Parameters:
            binary (bool): If True, sets the mode to binary; otherwise, sets it to text.
        """
        self.input_label.config(text="Text eingeben "+label+":")

    def clear_input(self):
        """
        Clears the input field.
        """
        self.input_field.delete("1.0", tk.END)
