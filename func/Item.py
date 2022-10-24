import json , func
from nextcord import ButtonStyle , Embed , Member


class Item:
    def __init__(self , _id:str , _item:dict[str] , _user:Member):
        inventory = func.Inventory(_user)

        self.__ranks = ["전설" , "에픽" , "레어" , "일반"]
        
        self.id:str = _id
        item:str = _item[_id]
        if (_id.split(":")[1] == "book"): self.rank = "책"
        else: self.rank = self.__ranks[int(_id.split(":")[1])]  
        self.emoji:str = item["emoji"]
        self.name:str = item["name"]
        self.description:str = item["description"]
        self.have = inventory._items.get(self.id , 0)
        
        self.color:ButtonStyle = ButtonStyle.gray
        
        self.color:Color = Color(int(_id.split(":")[1]))
        
        self.embed = Embed(title = f"{self.emoji} **{self.name}** {self.emoji}" , description = self.description , color = self.color.embed)
        self.embed.add_field(name="갯수" , value=str(self.have))
        
class Color:
    def __init__(self , _id):
        if (_id == 0):
            self.button = ButtonStyle.red
            self.embed = func.color.RED
        if (_id == 1):
            self.button = ButtonStyle.blurple
            self.embed = func.color.BLUE
        if (_id == 2):
            self.button = ButtonStyle.blurple
            self.embed = func.color.PERPLE
        if (_id == 3):
            self.embed = func.color.GRAY
            self.button = ButtonStyle.gray