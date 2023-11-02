import json

class Config:
    def __init__(self, filepath="config.json"):
        self.filepath = filepath
        self.config = self.load()

    def load(self):
        try:
            with open(self.filepath, "r") as f:
                return json.load(f)
        except:
            return {}
        
    def save(self):
        with open(self.filepath, "w") as f:
            json.dump(self.config, f)

    def get(self, key, default=None):
        return self.config.get(key, default)
    
    def set(self, key, value):
        self.config[key] = value
        self.save()