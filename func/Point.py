import json
isize = int
from .ServerOption import ServerOption
class Point:
    def __init__(self, server: isize) -> None:
        with open("json/point.json", "r") as f: self.json: dict = json.load(f)
        self.server = str(server)

    def add_point(self, user: isize, n: isize):
        self.json[self.server] = self.json.get(self.server, {})
        self.json[self.server][str(user)] = self.json[self.server].get(str(user), 0)

        self.json[self.server][str(user)] += n

        with open("json/point.json", "w") as f: json.dump(json, f, indent=4)

    def get_user(self, user: isize) -> isize:
        self.json[self.server] = self.json.get(self.server, {})
        self.json[self.server][str(user)] = self.json[self.server].get(str(user), 0)

        with open("json/point.json", "w") as f: json.dump(json, f, indent=4)
        
        return self.json[self.server][str(user)]
    
    def get_n(self, option: ServerOption): ...
