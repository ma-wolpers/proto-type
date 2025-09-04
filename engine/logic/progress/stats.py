class ProtoStats:
    """
    Tracks statistics relevant to determining challenge progress.

    Example:
        - sentmsgcount: 5
        - sentbitcount: 10
        - sentcontent: "0101010101"
    """
    def __init__(self):
        """
        Initializes the ProtoStats with default values.
        """
        self.reset()

    @property
    def sentmsgcount(self):
        return self._sentmsgcount

    @property
    def sentbitcount(self):
        """
        Returns the count of sent bits.

        Returns:
            int: The count of sent bits.
        """
        return self._sentbitcount

    @property
    def sentcontent(self):
        """
        Returns the content of sent messages.

        Returns:
            str: The content of sent messages.
        """
        return self._sentcontent

    
    # @property
    # def netmsgcount(self):
    #     """
    #     Returns the count of net messages.

    #     Returns:
    #         int: The count of net messages.
    #     """
    #     return self._netmsgcount

    # @property
    # def netcontent(self):
    #     """
    #     Returns the content of net messages.

    #     Returns:
    #         str: The content of net messages.
    #     """
    #     return self._netcontent
    

    def reset(self):
        """
        Resets all tracked statistics to their default values.

        Called by:
            stats.py __init__(): when the stats are initialized.
            flow.py check_progress(): when a challenge is completed.
        """
        self._sentmsgcount = 0
        self._sentbitcount = 0
        self._sentcontent = ""
        # self._netmsgcount = 0
        # self._netcontent = ""

    def update(self, data):
        """
        Updates the tracked statistics with new data.

        Parameters:
            data (dict): A dictionary containing the new statistics data.
        """
        if "sentmsgcount" in data:
            self._sentmsgcount = data['sentmsgcount']
        if "sentbitcount" in data:
            self._sentbitcount = data['sentbitcount']
        if "sent_content" in data:
            self._sentcontent = data['sent_content']
        # if "net_content" in data:
        #     self._netcontent = data['net_content']
        #     self._netmsgcount = len(data['net_content'].split("\n"))
    
    # export data for Settings
    def get(self):
        """
        Returns the current statistics data.

        Returns:
            dict: A dictionary containing the current statistics data.
        """
        return {
            'sentmsgcount': self._sentmsgcount,
            'sentbitcount': self._sentbitcount,
            'sent_content': self._sentcontent
        }
    
    def send_content(self, binarytext):
        """
        Updates the statistics.

        Parameters:
            binarytext (str): The binary content sent.
        """
        # Increase the message count
        self._sentcontent += binarytext
        self._sentbitcount += len(binarytext)


_stats = None
def get_stats():
    """ Returns the global Stats instance, creating it if it doesn't exist.
    
    Returns:
        Stats: The global Stats instance.
    """
    global _stats
    if _stats is None:
        _stats = ProtoStats()
    return _stats