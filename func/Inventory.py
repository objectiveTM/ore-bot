import json , func
from nextcord import *

class Inventory:
    def __init__(self , _user:Member):
        self._user = _user
        try:
            with open("json/inv.json" , "r" , encoding="UTF-8") as f:inv = json.load(f)
        except:inv = {}
        
        self._items = inv.get(str(_user.id) , {})
        
        with open("json/items.json" , "r" , encoding="UTF-8") as f:self._itemJson = json.load(f)
    
    def encoing(self) -> list[SelectOption]:
        select = []
        for item in self._items:
            mining = func.Mining(self._user)
            info = mining.findRank(id = item)
            select.append(SelectOption(emoji = f"{info.emoji}" , label = f"{info.name} | {info.rank}" , description=f"{info.have}개" , value = info.id))
        if select == []:
            select.append(SelectOption(emoji = "🕸️" , label = f"인벤토리가 비어있어요! | 없음"))
        return select
    def embed(self , _id:str) -> Embed:
        mining = func.Mining(self._user)
        info = mining.findRank(id = _id)
        info.embed
        embed = Embed(title = info.name , description = info.description , color = info.color.embed)
        return embed