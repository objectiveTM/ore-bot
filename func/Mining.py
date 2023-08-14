import json , random , func
from typing import overload
from nextcord import *

from func.Item import Item

class Mining:
    def __init__(self, _user:Member) -> None:
        self.user = _user
        self.__fileName = "json/inv.json"
        
        try:
            with open(self.__fileName , "r" , encoding="UTF-8") as f:self.inv = json.load(f)
        except:
            self.inv = {}
            with open(self.__fileName , "w" , encoding="UTF-8") as f:json.dump(self.inv , f , indent=4 , ensure_ascii=False)
        
        with open("json/items.json" , "r" , encoding="UTF-8") as f: self._itemJson = json.load(f)

    
    async def get(self , id:str = "stone:1"):
        """
        id아이템의 대한 정보를 가져온다
        """
        if (self.inv.get(str(self.user.id) , "null") == "null"):
            self.inv[str(self.user.id)] = {}
        if (self.inv[str(self.user.id)].get(id , "null") == "null"):
            self.inv[str(self.user.id)][id] = 1
        else:
            self.inv[str(self.user.id)][id] += 1
            
        self.inv[str(self.user.id)]
        await self.__save__()
    
    async def use(self , id:str , n:int = 0):
        """
        id: 사용할 아이템의 id\n
        n: 사용할 아이템의 개수
        """
        if (self.inv.get(str(self.user.id) , "null") == "null"):
            raise func.ERROR_404_ITEM
        if (self.inv[str(self.user.id)].get(id , "null") == "null"):
            raise func.ERROR_404_ITEM
        else:
            if (self.inv[str(self.user.id)][id] < n):raise func.ERROR_505_ENOUGHT
            self.inv[str(self.user.id)][id] -= n
            if (not self.inv[str(self.user.id)][id]):del self.inv[str(self.user.id)][id]

        self.inv[str(self.user.id)]
        await self.__save__()
        
    def isUse(self , id:str , n:int = 0) -> bool:
        """
        id이름의 아이템 n개를 사용할수있는지 확인하는 함수
        """
        # print(self.inv[str(self.user.id)][id] < n)
        return all([
            (self.inv[str(self.user.id)].get(id , 0) >= n),
            (self.inv.get(str(self.user.id) , "null") != "null")
        ])
    
    @overload
    def findRank(self , id:str) -> Item: 
        """
        id의 아이템을 반환한다
        """
        ...
    @overload
    def findRank(self , ranks:str) -> list[Item]:
        """
        ranks리스트에있는 랭크에 맞는 아이템을 반환한데
        """
        ...
    @overload
    def findRank(self , rank:str) -> Item:
        """
        rank에 맞는 아이템을 반환한다
        """
        ...

    def findRank(self , **params) -> Item:
        _id = params.get("id" , None)
        _ranks = params.get("ranks" , None)
        _rank = params.get("rank" , _ranks)
        if _id:
            return Item(_id , self._itemJson , self.user)
        
        elif _rank:
            if not _ranks:
                rank = 0
                ranks = ["전설" , "에픽" , "레어" , "일반"]
                for r in ranks:
                    if _rank != r: rank += 1
                    else: break
            else: rank = _rank
            rankArr = [Item(item , self._itemJson , self.user) for item in self._itemJson if (str(item).endswith(str(rank)))]
            if (rankArr == []):rankArr = [Item(item , self._itemJson , self.user) for item in self._itemJson if (str(item).endswith(str(_rank)))]
            
            if _ranks != None:return rankArr
            return random.choice(rankArr)
        return None
        
    
    
    async def __save__(self) -> bool:
        try:
            with open(self.__fileName , "w" , encoding="UTF-8") as f:json.dump(self.inv , f , indent=4 , ensure_ascii=False)
            return True
        except:return False