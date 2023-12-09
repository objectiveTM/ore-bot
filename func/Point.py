import json
from nextcord import Member
from .ServerOption import ServerOption

isize = int
class Point:
    def __init__(self, server: isize) -> None:
        with open("json/point.json", "r") as f: self.point: dict = json.load(f)
        self.server = str(server)

    def add_point(self, member: Member, n):
        if member.bot: return
        self.point[self.server] = self.point.get(self.server, {})
        self.point[self.server][str(member.id)] = self.point[self.server].get(str(member.id), 0)

        self.point[self.server][str(member.id)] += int(n)

        with open("json/point.json", "w") as f: json.dump(self.point, f, indent=4)

    def get_user(self, user: isize) -> isize:
        self.point[self.server] = self.point.get(self.server, {})
        self.point[self.server][str(user)] = self.point[self.server].get(str(user), 0)

        with open("json/point.json", "w") as f: json.dump(self.point, f, indent=4)
        
        return self.point[self.server][str(user)]


    def get_list(self) -> dict:
        with open("json/point.json", "r") as f: self.point: dict = json.load(f)
        return self.point[self.server]