import json

def load_config(filepath="config.json"):
    print("*** Loading config...")
    try:
        with open(filepath, "r") as f:
            config = json.load(f)
        return config
    except:
         return {}
    
def save_config(config, filepath="config.json"):
    print("*** Saving config...")
    with open(filepath, "w") as f:
        json.dump(config, f)

config = load_config()