class ProtoSettings:
    def __init__(self, filemanager, bicoder, filter, signature, stats, progress, user_file=""):
        self._filemanager = filemanager
        self._bicoder = bicoder
        self._filter = filter
        self._signature = signature
        self._stats = stats
        self._progress = progress
        self._user_file = user_file
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
        keys = ["code_dict", "network", "eol", "filter", "signature", "code_length"] + list(self._config_data)
        if user:
            keys += list(self._user_data)
        return keys


    ## IMPORT data

    def parse_data(self, data={}, save=True):
        for x in data:
            if x=="network":
                self._filemanager.update(network=data[x])
            elif x=="eol":
                self._bicoder.update_eol(eol=data[x])
            elif x=="code_length":
                self._bicoder.update_code_length(code_length=data[x])
            elif x=="code_text":
                self._bicoder.parse(code_text=data[x])
            elif x=="code_dict":
                self._bicoder.update_dict(code_dict=data[x])
            elif x=="filter":
                self._filter.update(filter=data[x])
            elif x=="signature":
                self._signature.update(signature=data[x])
            elif x=="stats":
                self._stats.update(data[x])
            elif x=="progress":
                self._progress.update(data[x])
            elif x in self._user_data.keys():
                self._user_data[x]=data[x]
                if x == "username" and not data[x]:
                    self._user_data[x]="Gast"
            elif x in self._config_data.keys():
                self._config_data[x]=data[x]
            else:
                print(f"Achtung: Unbekannter Key! '{x}'")
        if save and self._user_data["autosave"] and self._user_file:
            self.save_user()
            return True
        return False
    
    def import_file(self, path, user=True):
        if not path:
           return {}
        if user:
            self._user_file = path
        filedata = self._filemanager.load_json(path)
        self.parse_data(data=filedata, save=False)
        return list(filedata)

    ## EXPORT data

    def collect_data(self, keys=[]):
        data={}
        for x in keys:
            if x=="network":
                data[x] = self._filemanager.get_net()
            elif x=="eol":
                data[x] = self._bicoder.eol
            elif x=="code_text":
                data[x] = self._bicoder.dict_to_text()
            elif x=="code_dict":
                data[x] = self._bicoder.dict
            elif x=="code_length":
                data[x] = self._bicoder.code_length
            elif x=="filter":
                data[x] = self._filter.get()
            elif x=="signature":
                data[x] = self._signature.get()
            elif x=="stats":
                data[x] = self._stats.get()
            elif x=="guiprogress":    
                data["level"] = self._progress.leveldata
                data["challenge"] = self._progress.chlgdata
            elif x=="progress":   # for saving to file
                data["level_id"] = self._progress.get().get("level_id")
                data["challenge_id"] = self._progress.get().get("challenge_id")
            elif x in self._user_data.keys():
                data[x] = self._user_data[x]
            elif x in self._config_data.keys():
                data[x] = self._config_data[x]
            else:
                print(f"Achtung: Unbekannter Key! '{x}'")
        return data
    
    def collect_for_gui(self, keys=[]):
        if "code_dict" in keys:
            keys.remove("code_dict")
            keys.append("code_text")
        if "code_length" in keys:
            keys.append("code_text")
            keys.append("eol")
        return self.collect_data(keys)

    def export_file(self, path="", user=True):
        if not path:
            if user and self._user_file: # empty path for .user-file can be fixed by stored user path
                path = self._user_file
            else:
                raise NameError("kein Pfad angegeben")  # NOTFALL-Warnung!
        else:
            self._user_file = path
        keys = self.find_keys(user=user)
        data = self.collect_data(keys=keys)
        return self._filemanager.save_file(path, json.dumps(data, indent=4))
        
    
    ## CHECK data integrity
    def check_integrity(self, on_keys, for_binary):
        word_fields = ["filter", "signature"]
        coding_fields = ["code_text", "eol"]
        if any (x in on_keys for x in coding_fields):
            self._bicoder.check_dict_compliance(self.collect_data(word_fields), for_binary = for_binary)
        if any (x in on_keys for x in word_fields):
            self._bicoder.check_dict_compliance(self.collect_data(word_fields), for_binary = for_binary)