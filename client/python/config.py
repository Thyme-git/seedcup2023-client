import json

class Config(object):
    def __init__(self, path="../../config.json") -> None:
        with open(path, "r") as f:
            self.config = json.load(f)

    def get(self, query):
        return self.config.get(query)

config = Config()