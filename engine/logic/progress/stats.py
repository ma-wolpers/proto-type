class ProtoStats:
    def __init__(self):
        self._sentmsgcount = 0
        self._sentbitcount = 0
        self._sentcontent = ""
        """ self._netmsgcount = 0
        self._netcontent = "" """

    def sentmsgcount(self):
        return self._sentmsgcount
    def sentbitcount(self):
        return self._sentbitcount
    def sentcontent(self):
        return self._sentcontent
    """ def netmsgcount(self):
        return self._netmsgcount
    def netcontent(self):
        return self._netcontent """

    def reset(self):
        self._sentmsgcount = 0
        self._sentbitcount = 0
        self._sentcontent = ""
        """ self._netmsgcount = 0
        self._netcontent = "" """

    def update(self, data):
        if "sentmsgcount" in data:
            self._sentmsgcount = data['sentmsgcount']
        if "sentbitcount" in data:
            self._sentbitcount = data['sentbitcount']
        if "sent_content" in data:
            self._sentcontent = data['sent_content']
        """ if "net_content" in data:
            self._netcontent = data['net_content']
            self._netmsgcount = len(data['net_content'].split("\n")) """
    
    # export data for Settings
    def get(self):
        return {
            'sentmsgcount': self._sentmsgcount,
            'sentbitcount': self._sentbitcount,
            'sent_content': self._sentcontent
        }
    
    def send_content(self, binarytext):
        # Increase the message count
        self._sentcontent += binarytext
        self._sentbitcount += len(binarytext)