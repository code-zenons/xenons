import json
import os

CONFIG_FILE = "config.json"

DEFAULT_CONFIG = {
    "scan": {
        "timeout": 2.0,
        "concurrency": 100
    },
    "ui": {
        "theme": "monokai"
    }
}

class Config:
    def __init__(self):
        self.config = DEFAULT_CONFIG
        self.load()

    def load(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    self.config.update(json.load(f))
            except:
                pass

    def get(self, key, default=None):
        keys = key.split('.')
        val = self.config
        for k in keys:
            val = val.get(k, default)
            if val is None:
                return default
        return val

cfg = Config()
