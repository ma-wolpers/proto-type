class BinaryCoder:
    def __init__(self, code_dict={}, eol=""):
        self.__code_dict = code_dict
        self.__eol = eol
        self.__code_length = None # This will be set when the code dictionary is updated

    def update_dict(self, code_dict):
        self.__code_dict = code_dict
        self.match_code_length_dict()
        return self.__code_dict

    def update_eol(self, eol):
        self.__eol = eol
        self.match_code_length_eol()
        return self.__eol
    
    def update_code_length(self, code_length):
        """Update the code length and adjust the eol and code dictionary accordingly."""
        if not code_length:
            self.__code_length = None
            return self.__code_length
        # Validate the code length
        if not isinstance(code_length, int) or code_length < 1:
            raise Warning("Wörterbuch", "Ungültige Code-Länge!")
        self.__code_length = code_length
        self.match_code_length_eol()
        self.match_code_length_dict()
        return self.__code_length
        
    def match_code_length_eol(self):
        """Adjust the eol to match the specified code length.

        Raises:
            Warning: If the eol cannot be adjusted to the specified code length.
        Returns:
            bool: True if the eol is successfully adjusted, false if the new eol code is already in the dictionary.
        """
        if not self.__eol or not self.__code_length:
            return True
        # Update the eol to ensure it is of the specified length
        match = self.match_code_length(self.__eol)
        if not match:
            raise Warning("Wörterbuch", f"Zeilenende kann nicht auf die Länge {self.__code_length} gekürzt werden!")
        self.__eol = match
        return not self.is_in_dict(match) # Ensure the eol is still unique after matching lengths

    def match_code_length_dict(self):
        if self.__code_length is None:
            return True # No code length set, nothing to match
        # Update the code dictionary to ensure all codes are of the specified length
        code_dict = {}
        for word in self.__code_dict:
            match = self.match_code_length(self.__code_dict[word])
            if not match:
                raise Warning("Wörterbuch", f"Code für \"{word}\" kann nicht auf die Länge {self.__code_length} gekürzt werden!")
            else:
                code_dict[word] = match
        self.is_unidec(code_dict) # Ensure the dictionary is still uniquely decodable after matching lengths
        self.__code_dict = code_dict
        return True

    def match_code_length(self, code):
        code_length = self.__code_length
        if code_length is None:
            return code # No code length set, nothing to match
        if len(code) < code_length:
                # Pad the eol with zeros to the left
                code = code.zfill(code_length)
        elif len(code) > code_length:
            # try to cut leading zeros
            if "1" in code[:-code_length]:
                return False # Cannot shorten the code
            else:
                code = code[-code_length:]
        return code

    @property
    def dict(self):
        return self.__code_dict
    @property
    def eol(self):
        return self.__eol
    @property
    def code_length(self):
        return self.__code_length

    def parse(self, code_text):
        """Parse the code text and update the code dictionary."""
        # Read entries from the text field and update the dictionary
        if not code_text:
            self.__code_dict = {}
            return self.__code_dict
        code_dict = {}
        code_list = code_text.strip().strip(",").split(",")
        for code in code_list:
            if not code.strip():
                raise Warning("Wörterbuch", 'ein \",\" zu viel?')
            terms = code.split("=")
            if len(terms)<2:
                raise Warning("Wörterbuch", f'in \"{code}\" fehlt das \"=\".')
            if len(terms)>2:
                raise Warning("Wörterbuch", f'in \"{code}\" fehlt ein \",\" oder ist ein \"=\" zu viel.')
            word, binary = terms
            if not binary:
                raise Warning("Wörterbuch", f"Binärcode für {word} fehlt!")
            # Check if only 0 and 1 are used in the binary code
            if not all(c in "01" for c in binary.strip()):
                raise Warning("Wörterbuch", "Nur 0 und 1 erlaubt!")
            cleanword = word.strip().strip('\"')
            if cleanword in code_dict:
                raise Warning("Wörterbuch", f"\"{cleanword}\" mehrfach kodiert!")
            code_dict[cleanword] = binary.strip()
        
        self.is_unidec(code_dict)
        self.update_dict(code_dict)
        return self.__code_dict
    
    def dict_to_text(self):
        return ", ".join(f'"{k}"={v}' for k, v in self.__code_dict.items()) + ","

    def find_common_multiple(self, codewords):
        # Sardinas–Patterson algorithm
        track = {}

        suffixes = set(codewords)
        s_sets = [suffixes]

        while suffixes:
            new_suffixes = set()
            for suffix in suffixes:
                for codeword in codewords:
                    if suffix.startswith(codeword):
                        new_suffix = suffix[len(codeword):]
                        if new_suffix == "":
                            continue
                        track[new_suffix] = track.get(codeword,codeword)+new_suffix
                        if new_suffix in codewords:
                            return track[new_suffix]
                        new_suffixes.add(new_suffix)
                    if codeword.startswith(suffix):
                        new_suffix = codeword[len(suffix):]
                        if new_suffix == "":
                            continue
                        track[new_suffix] = track.get(suffix,suffix)+new_suffix
                        if new_suffix in codewords:
                            return track[new_suffix]
                        new_suffixes.add(new_suffix)
            suffixes = new_suffixes
            for s in s_sets:
                if s == suffixes:
                    return ""
            else:
                s_sets.append(suffixes)
        return ""

    def is_unidec(self, code_dict):
        """Check if the binary codes in the dictionary are uniquely decodable.
        
        Raises a Warning if there are duplicates or common multiples.
        
        Parameters:
            code_dict (dict): The dictionary containing words and their binary codes.
        """

        if not code_dict:
            return None
        
        # Check for uniqueness of the binary codes
        binary_codes = list(code_dict.values())
        # Find double entries in the binary codes
        for code in binary_codes:
            if binary_codes.count(code) > 1:
                raise Warning("Wörterbuch", f"Nicht eindeutige Kodierung - \"{code}\" mehrfach vergeben")
        # Check for common multiple in binary codes
        checkbinary = self.find_common_multiple(binary_codes)
        if checkbinary:
            raise Warning("Wörterbuch", f"Nicht eindeutig: \"{checkbinary}\"")
        
        # Check for uniqueness of the codewords
        checkwords = self.find_common_multiple(list(self.__code_dict.keys()))
        if checkwords:
            raise Warning("Wörterbuch", f"Nicht eindeutige Kodierung, von z.B. \"{checkwords}\"")

    def is_in_dict(self, code):
        """Check if the given code is in the dictionary.

        Parameters:
            code (str): The binary code to check.
        Returns:
            bool: True if the code is in the dictionary, False otherwise.
        """
        
        if code:
            if code in list(self.__code_dict.values()):
                return True
        return False
    
    
    def encode_text(self, text):
        if not text:
            return text
        if not self.__code_dict:
            raise Warning("Kodierprozess", "Wörterbuch ist leer!")
        i = 0
        binary_code = ""
        maxwordlength = max(len(word) for word in self.__code_dict.keys())
        while i < len(text):
            if text[i] == "\n":
                binary_code += self.__eol
                i += 1
            for length in range(maxwordlength, 0, -1): # Check for the longest word first
                if text[i:i+length] in self.__code_dict:
                    binary_code += self.__code_dict[text[i:i+length]]
                    i += length
                    break
            else:
                raise Warning("Kodierprozess", f"\"{text[i:]}\" nicht kodierbar")
        return True, binary_code

    # OLD
    # def decode_text(self, binary_code, warn=False):
    #     if not (binary_code and self.__code_dict):
    #         return binary_code
    #     revdict = {v: k for k, v in self.__code_dict.items()}  # Reverse the dictionary for decoding
    #     text = ""
    #     i = 0
    #     while i < len(binary_code):
    #         for length in range(1, 9):  # Assuming binary codes are up to 8 bits long
    #             if binary_code[i:i+length] in revdict:
    #                 text += revdict[binary_code[i:i+length]]
    #                 i += length
    #                 break
    #         else:
    #             if warn:
    #                 raise Warning("Dekodierprozess", f"\"{binary_code[i:]}\" nicht dekodierbar")
    #             else:
    #                 text += binary_code[i]
    #                 i += 1
    #     return text

    def decode_text(self, binary_code, warn=False):
        if not (binary_code and self.__code_dict):
            return binary_code
        if not self.__code_length:
            return self.dec_wo_length(binary_code, warn=warn)
        else:
            return self.dec_with_length(binary_code, warn=warn)
    
    def dec_with_length(self, binary_code, warn=False):
        """Decode a binary code considering the code length.

        Parameters:
            binary_code (str): The binary code to decode.
            warn (bool): If True, raises a Warning if the code cannot be decoded.
        Raises:
            Warning: If the binary code cannot be decoded and warn is True.
        Returns:
            str: The decoded text or the original binary code if decoding fails.
        """

        # reverse the code dictionary for decoding
        revdict = {v: k for k, v in self.__code_dict.items()}
        # Check if all binary codes in the dictionary have the correct length
        for bcode in revdict.keys():
            if len(bcode) != self.__code_length:
                raise Warning("Dekodierprozess", f"Binärcode \"{bcode}\" von \"{revdict[bcode]}\" hat nicht die Länge {self.__code_length}!")
        for k in range(0, len(binary_code), self.__code_length):
            if k + self.__code_length > len(binary_code):
                if warn:
                    raise Warning("Dekodierprozess", f"\"{binary_code[k:]}\" nicht dekodierbar")
                return binary_code
            code = binary_code[k:k + self.__code_length]
            if code in revdict:
                word = revdict[code]
            else:
                if warn:
                    raise Warning("Dekodierprozess", f"\"{code}\" nicht dekodierbar")
                word = code
            if k == 0:
                text = word
            else:
                text += word
        return text

            

    def dec_wo_length(self, binary_code, warn=False):
        """Decode a binary code without considering the code length.

        Parameters:
            binary_code (str): The binary code to decode.
            warn (bool): If True, raises a Warning if the code cannot be decoded.
        Raises:
            Warning: If the binary code cannot be decoded and warn is True.
        Returns:
            str: The decoded text or the original binary code if decoding fails.
        """

        # reverse the code dictionary for decoding
        revdict = {v: k for k, v in self.__code_dict.items()}
        n = len(binary_code)
        max_code_len = max(len(code) for code in revdict)
        # dp[i] = (prev_index, word) if binary_code[:i] can be decoded, else None
        dp = [None] * (n + 1)
        dp[0] = (None, None)

        for i in range(1, n + 1):
            for l in range(1, max_code_len + 1):
                if i - l < 0:
                    continue
                code = binary_code[i - l:i]
                if code in revdict and dp[i - l] is not None:
                    dp[i] = (i - l, revdict[code])
                    break  # Only need one valid path due to unique decodability

        if dp[n] is not None:
            # Reconstruct the decoded string
            result = []
            idx = n
            while idx > 0:
                prev_idx, word = dp[idx]
                result.append(word)
                idx = prev_idx
            return ''.join(reversed(result))
        else:
            if warn:
                raise Warning("Dekodierprozess", f"\"{binary_code}\" nicht dekodierbar")
            return binary_code

    def append_eol(self, text):
        return text+self.__eol

    def split_eol(self, binary_code):
        if not self.__eol:
            return [binary_code]
        if not self.all_binary(self.__eol):
            raise Warning("Zeilenende", "Nur 0 und 1 erlaubt!")
        if self.__code_length:
            if len(self.__eol) != self.__code_length:
                raise Warning("Zeilenende", f"Zeilenende muss die Länge {self.__code_length} haben!")
            # Split the binary code by the eol, which is a fixed-length binary string
            parts = []
            current_part = ""
            start = 0
            while start + self.__code_length <= len(binary_code):
                current_block = binary_code[start:start+self.__code_length]
                if current_block == self.__eol:
                    parts.append(current_part)
                    current_part = ""
                else:
                    current_part += current_block
                start = start + self.__code_length
            current_part += binary_code[start:]
            parts.append(current_part)
            return parts
        else:
            return binary_code.split(self.__eol)

    def decode_data(self, data):
        if type(data) is str:
            return self.decode_text(data, warn=True)
        elif type(data) is dict:
            for key in data:
                data[key] = self.decode_data(data[key])
        return data

    def encode_data(self, data):
        if type(data) is str:
            return self.encode_text(data)
        elif type(data) is dict:
            for key in data:
                data[key] = self.encode_data(data[key])
        return data


    def all_binary(self, data):
        if type(data) is str:
            return all(c in "01" for c in data)
        elif type(data) is dict:
            return all(self.all_binary(data[key]) for key in data)
        
    def check_dict_compliance(self, data, for_binary):
        if for_binary:
            if not self.all_binary(data):
                raise Warning("", "Nur 0 und 1 erlaubt!")
        else:
            self.encode_data(data)
