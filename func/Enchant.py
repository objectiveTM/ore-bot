import json
from typing import Union, overload
from nextcord import Member
from multipledispatch import dispatch

class Enchant:
    def __init__(self , _enchant:Union[str , list]) -> None:
        with open("json/enchants.json" , "r" , encoding = "UTF-8") as f: enchant:dict[dict] = json.load(f)
        self.plus = 0
        self.luck = 0
        if type(_enchant) == list:
            for e in _enchant:
                self.plus = enchant.get(e , {}).get("plus" , self.plus)
                self.luck = enchant.get(e , {}).get("luck" , self.luck)
        else:
            self.plus = enchant.get(_enchant , {}).get("plus" , self.plus)
            self.luck = enchant.get(_enchant , {}).get("luck" , self.luck)
    
    @dispatch(str)
    def __add__(self , a):
        with open("json/enchants.json" , "r" , encoding = "UTF-8") as f: enchant:dict[dict] = json.load(f)
        self.plus = enchant.get(a , {}).get("plus" , self.plus)
        self.luck = enchant.get(a , {}).get("luck" , self.luck)
        return self
    
    @dispatch(list)
    def __add__(self , a):
        with open("json/enchants.json" , "r" , encoding = "UTF-8") as f: enchant:dict[dict] = json.load(f)
        for e in a:
            self.plus = enchant.get(e , {}).get("plus" , self.plus)
            self.luck = enchant.get(e , {}).get("luck" , self.luck)
        return self
        
    def __radd__(self , a:str):
        return self.__add__(a)