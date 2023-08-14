import json, datetime
from nextcord import Member
from .EffectItem import EffectItem
class Effect:
    def __init__(self, _user: Member):
        self.user = _user

    def setEffect(self, name: str):
        with open("json/effect.json", "r", encoding="UTF-8") as f: j = json.load(f)
        user = j.get(str(self.user.id), {})
        j[str(self.user.id)] = user
        j[str(self.user.id)][name] = int(datetime.datetime.now().timestamp()) + EffectItem(name).time
        with open("json/effect.json", "w", encoding="UTF-8") as f: json.dump(j, f, indent=4, ensure_ascii=False)
