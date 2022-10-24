import random
from nextcord import *
from func import *

import json

INTENTS = Intents.default()
# INTENTS.all()
CLIENT = Client(intents = INTENTS)

@CLIENT.event
async def on_ready():
    print("RUN")

@CLIENT.slash_command()
async def 광질(inter:Interaction):
    await inter.response.defer()
    ore = Ore(inter.user)
    rank = ore.rank
    await inter.followup.send(embed = rank.embed , view = Comps([ore]))

@CLIENT.slash_command()
async def 인벤토리(inter:Interaction):
    await inter.response.defer()
    await inter.followup.send(view = Comps([Inv(inter.user)]))

@CLIENT.slash_command()
async def 인첸트(inter:Interaction):
    await inter.response.send_message(view = Comps([EnchantButton(inter.user , i+1) for i in range(3)]))

class Comps(ui.View):
    def __init__(self , comps:list[ui.Select]):
        super().__init__()
        for comp in comps:
            self.add_item(comp)

class Inv(ui.Select):
    def __init__(self , _user):
        self._user = _user
        self.inventory = Inventory(_user)
        options = self.inventory.encoing()
        super().__init__(placeholder="눌러서 인벤토리를 확인하세요!" , options=options)
    async def callback(self, inter:Interaction):
        await inter.message.edit(embed = Mining(self._user).findRank(id = self.values[0]).embed)

class Ore(ui.Button):
    def __init__(self, _user:Member):
        self._user = _user
        self.mining = Mining(self._user)
        rank = random.randint(1 , 1000)
        if (rank == 1): rank = "전설"
        elif (rank < 11): rank = "에픽"
        elif (rank < 202): rank = "레어"
        else: rank = "일반"
        self.rank = self.mining.findRank(rank = rank)
            
        super().__init__(style=self.rank.color.button , emoji = self.rank.emoji)
        
    async def callback(self, inter:Interaction):
        await inter.response.defer()
        await self.mining.get(self.rank.id)
        rank = random.randint(1 , 1000)
        if (rank == 1): rank = "전설"
        elif (rank < 11): rank = "에픽"
        elif (rank < 202): rank = "레어"
        else: rank = "일반"
        
        self.rank = self.mining.findRank(rank = rank)
        self.style = self.rank.color.button
        self.emoji = self.rank.emoji
        await inter.message.edit(embed = self.rank.embed , view = Comps([self]))

class EnchantButton(ui.Button):
    def __init__(self, _user:Member , id:str , disabled = False):
        if (str(id).startswith("end")): super().__init__(emoji = Emojis.blueStone , label = f"구매" , custom_id=str(id) , disabled=disabled)
        else: super().__init__(emoji = Emojis.blueStone , label = f"{id}개 사용" , custom_id=str(id) , disabled=disabled)
        self.mining = func.Mining(_user)
        self._user = _user

    async def callback(self, inter:Interaction):
        if (self.custom_id.startswith("end")):
            id = int(self.custom_id.split("|")[1])
            try:
                await self.mining.use("blueStone:0" , id)
            except Exception as e:
                return await inter.response.send_message(e , ephemeral = True)
            item = self.mining.findRank(rank = "book")
            await self.mining.get(item.id)
            
            v = Comps([EnchantButton(inter.user , i+1) for i in range(3)])
            v.add_item(EnchantButton(inter.user , f"end|{id}" , not self.mining.isUse("blueStone:0" , id)))
            
            return await inter.message.edit(embed = item.embed , view = v)
            
        v = Comps([EnchantButton(inter.user , i+1) for i in range(3)])
        v.add_item(EnchantButton(inter.user , f"end|{self.custom_id}" , not self.mining.isUse("blueStone:0" , int(self.custom_id))))
        await inter.message.edit(view=v)
        

CLIENT.run('ODc4NDk0NTI0MzcxMDA5NTQ2.G3iTDq.SxiL4zcnqMxklcgX70JGR0jeOCL6Hez741UJd4')