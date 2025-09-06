from . import filemanager
from .. import bicoder, filter, signature, stats, progress
import json

class ProtoSettings:
    """
    Manages the user and setting data for the application.
    """

    def __init__(self):
        """
        Initialize the settings manager.
        """
        self._user_data = {
            "autosave": False,
            "username": "",
            "xp":0,
            "max_xp":100,
            "achievements":{},
            "stats":{},
            "progress":{},
        }
        self._config_data = {
        }
        "ACHTUNG: config wird als 'config':{data} Paar im .user-json mitgespeichert!"

    def find_keys(self, user):
        """
        Find and return the keys to be used for data collection and export.

        Parameters:
            user (bool): Whether to include user-specific data.
        Returns:
            list: List of keys to be used for data collection and export.
        """
        keys = ["code_dict", "network", "eol", "filter", "signature", "code_length"] + list(self._config_data)
        if user:
            keys += list(self._user_data)
        return keys


    ## IMPORT data

    def parse_data(self, data, save=True):
        """
        Parse the provided data and update the settings accordingly.

        Parameters:
            data (dict): Data to be parsed and updated.
            save (bool): Whether to save the user data after parsing.
        Returns:
            bool: True if data was saved, False otherwise.
        """
        if not data:
            return False
        for x in data:
            if x=="encoding":  # special case for filter and signature
                continue
            elif x=="network":
                filemanager().update(network=data[x])
            elif x=="eol":
                bicoder().update_eol(eol=data[x])
            elif x=="code_length":
                bicoder().update_code_length(code_length=data[x])
            elif x=="code_text":
                bicoder().parse(code_text=data[x])
            elif x=="code_dict":
                bicoder().update_dict(code_dict=data[x])
            elif x=="filter":
                if "encoding" in data:
                    filter().update(filter=data[x], words=data["encoding"])
                else:
                    print("Achtung: Kein Encoding-Status übergeben, Filter wird nicht aktualisiert!")
            elif x=="signature":
                if "encoding" in data:
                    signature().update(signature=data[x], words=data["encoding"])
                else:
                    print("Achtung: Kein Encoding-Status übergeben, Signatur wird nicht aktualisiert!")
            elif x=="stats":
                stats().update(data[x])
            elif x=="progress":
                progress().update(data[x])
            elif x in self._user_data.keys():
                self._user_data[x]=data[x]
                if x == "username" and not data[x]:       # if no username is given, set to "Gast"
                    self._user_data[x]="Gast"
            elif x in self._config_data.keys():
                self._config_data[x]=data[x]
            else:
                print(f"Achtung: Unbekannter Key! '{x}'")
        if save and self._user_data["autosave"] and self._user_file:
            self.export_file()
            return True
        return False
    
    def import_file(self, path, user=True):
        """
        Import data from a JSON file and parse it.
        
        Parameters:
            path (str): Path to the JSON file to be imported.
            user (bool): Whether to include user-specific data in the import.
        Returns:
            dict: The imported data as a dictionary.
        """
        if not path:
           return {}
        if user:
            self._user_file = path
        filedata = filemanager().load_json(path)
        self.parse_data(data=filedata, save=False)
        return list(filedata)

    ## EXPORT data

    def collect_data(self, keys):
        """
        Collect data based on the provided keys. If no keys are provided, return an empty dictionary.

        Parameters:
            keys (list): List of keys to collect data for.
        Returns:
            dict: Dictionary containing the collected data.
        """
        if not keys:
            return {}
        data={}
        for x in keys:
            if x=="encoding":  # special case for filter and signature
                continue
            elif x=="network":
                data[x] = filemanager().network
            elif x=="eol":
                data[x] = bicoder().eol
            elif x=="code_text":
                data[x] = bicoder().dict_to_text()
            elif x=="code_dict":
                data[x] = bicoder().dict
            elif x=="code_length":
                data[x] = bicoder().code_length
            elif x=="filter":
                data[x] = filter().get()
            elif x=="signature":
                data[x] = signature().get()
            elif x=="stats":
                data[x] = stats().get()
            elif x=="guiprogress":
                _progress = progress()  
                data["level"] = _progress.leveldata
                data["challenge"] = _progress.chlgdata
            elif x=="progress":   # for saving to file
                _progress = progress()	
                data["level_id"] = _progress.get_ids().get("level_id")
                data["challenge_id"] = _progress.get_ids().get("challenge_id")
            elif x in self._user_data.keys():
                data[x] = self._user_data[x]
            elif x in self._config_data.keys():
                data[x] = self._config_data[x]
            else:
                print(f"Achtung: Unbekannter Key! '{x}'")
        return data
    
    def collect_for_gui(self, keys):
        """
        Collect data for GUI display, modifying keys as necessary.

        Parameters:
            keys (list): List of keys to collect data for.
        Returns:
            dict: Dictionary containing the collected data.
        """
        if not keys:
            return {}
        if "code_dict" in keys:
            keys.remove("code_dict")
            keys.append("code_text")
        if "code_length" in keys:
            keys.append("code_text")
            keys.append("eol")
        return self.collect_data(keys)

    def export_file(self, path="", user=True):
        """
        Export the collected data to a JSON file.

        Parameters:
            path (str): Path to the file where data will be saved.
            user (bool): Whether to include user-specific data in the export.
        Returns:
            bool: True if the file was saved successfully, False otherwise.
        """
        if not path:
            if user and self._user_file: # empty path for .user-file can be fixed by stored user path
                path = self._user_file
            else:
                raise Warning("Speicherung", "kein Pfad angegeben")  # NOTFALL-Warnung!
        else:
            self._user_file = path
        keys = self.find_keys(user=user)
        data = self.collect_data(keys=keys)
        return filemanager().save_file(path, json.dumps(data, indent=4))
        
    
    ## CHECK data integrity
    def check_integrity(self, on_keys, encoding):
        """
        Check the integrity of the data based on the provided keys.
        
        Parameters:
            on_keys (list): List of keys to check for integrity.
            encoding (bool): Whether to check for encoding or binary compliance.
        
        Raises:
            Warning: If the integrity check fails.
        """
        word_fields = ["filter", "signature"]
        coding_fields = ["code_text", "eol"]
        if any (x in on_keys for x in coding_fields) or any (x in on_keys for x in word_fields):
            bicoder().check_dict_compliance(self.collect_data(word_fields), encoding=encoding)

_settings = None
def get_settings():
    """
    Returns the global instance of ProtoSetting.
    If the instance does not exist, it creates a new one.

    Returns:
        ProtoSettings: The initialized settings instance.
    """
    global _settings
    if _settings is None:
        _settings = ProtoSettings()
    return _settings