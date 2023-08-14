import json
from typing import Union, overload
from nextcord import Member
from multipledispatch import dispatch

class EffectItem:
    def __init__(self , _effect:Union[str , list[str]]) -> None:
        with open("json/effects.json" , "r" , encoding = "UTF-8") as f: effect:dict[dict] = json.load(f)
        self.plus = 0
        self.luck = 0
        self.time = 0
        if type(_effect) == list:
            for e in _effect:
                self.plus = effect.get(e , {}).get("plus" , self.plus)
                self.luck = effect.get(e , {}).get("luck" , self.luck)
                self.time = effect.get(e , {}).get("time" , self.time)
        else:
            self.plus = effect.get(_effect , {}).get("plus" , self.plus)
            self.luck = effect.get(_effect , {}).get("luck" , self.luck)
            self.time = effect.get(_effect , {}).get("time" , self.time)
    
    @dispatch(str)
    def __add__(self , a: str):
        with open("json/effects.json" , "r" , encoding = "UTF-8") as f: effect:dict[dict] = json.load(f)
        self.plus = effect.get(a , {}).get("plus" , self.plus)
        self.luck = effect.get(a , {}).get("luck" , self.luck)
        return self
    
    @dispatch(list)
    def __add__(self , a: list[str]):
        with open("json/effects.json" , "r" , encoding = "UTF-8") as f: effect:dict[dict] = json.load(f)
        for e in a:
            self.plus = effect.get(e , {}).get("plus" , self.plus)
            self.luck = effect.get(e , {}).get("luck" , self.luck)
        return self
        
    def __radd__(self , a:str):
        return self.__add__(a)