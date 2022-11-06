import random
from nextcord import *
from func import *
import typing
import time
import play2048 as p_2048

import json

INTENTS = Intents.all()
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

CUSTOM = p_2048.customs.ORIGINAL.value

@CLIENT.slash_command()
async def play2048(inter:Interaction):
    _2048 = p_2048.Game()
    
    view = [
        Play2048(disabled = True), Play2048(label = "w", style = ButtonStyle.blurple, user = inter.user, _2048 = _2048, custom_id="up"), Play2048(disabled = True), Play2048(label = "end", style = ButtonStyle.red, user = inter.user, _2048 = _2048, custom_id="end"),
        Play2048(label = "a", style = ButtonStyle.blurple, user = inter.user, _2048 = _2048, row = 2, custom_id="left"), Play2048(label = "s", style = ButtonStyle.blurple, user = inter.user, _2048 = _2048, row = 2, custom_id="down"), Play2048(label = "d", style = ButtonStyle.blurple, user = inter.user, _2048 = _2048, row = 2, custom_id="right"), Play2048(disabled = True, row = 2)
    ]
    
    await inter.response.send_message(f"점수: **0점**", file = File(_2048.encodingImage(CUSTOM).image_bytes, f"point_0.png"), view = Comps(view))
    
@CLIENT.slash_command()
async def rank2048(inter:Interaction):
    with open("json/2048Best.json", "r") as f: _j:dict = json.load(f)
    
    j = sorted(_j.items() , key=lambda x : x[0] , reverse = True)
    description = ""
    for rank in j[:10]:
        user = utils.get(CLIENT.get_all_members() , id = int(rank[0]))
        description += f"{user}: **{rank[1][0]}점** <t:{rank[1][1]}:R>\n"
        
    await inter.response.send_message(embed = Embed(title = "2048 rank!", description = description, color = color.BLUE))

class Comps(ui.View):
    def __init__(self , comps:list[ui.Select]):
        super().__init__()
        for comp in comps:
            self.add_item(comp)

class Play2048(ui.Button):
    def __init__(self, *, user:Member = None, _2048:p_2048.Game = None, style:ButtonStyle = ButtonStyle.secondary, label:typing.Optional[str] = "ㅤ", disabled:bool = False, custom_id:typing.Optional[str] = None, url:typing.Optional[str] = None, emoji:typing.Optional[Union[str, Emoji, PartialEmoji]] = None, row:typing.Optional[int] = None):
        super().__init__(style = style, label = label, disabled = disabled, custom_id = custom_id, url = url, emoji = emoji, row = row)
        self.user = user
        self._2048 = _2048
        
    async def callback(self, inter:Interaction):
        if self.user != inter.user:return await inter.response.send_message("자신의것을 사용하세요!", ephemeral = True)
        m = 0
        if self.custom_id == "up":    m  = p_2048.move.UP
        if self.custom_id == "down":  m  = p_2048.move.DOWN
        if self.custom_id == "left":  m  = p_2048.move.LEFT
        if self.custom_id == "right": m  = p_2048.move.RIGHT
        
        if m != 0:
            self._2048.move(m)
            img = File(self._2048.encodingImage(CUSTOM).image_bytes, f"point_{self._2048.point}.png")
            with open("json/2048Best.json", "r") as f: j:dict = json.load(f)
            msg = ""
            if self._2048.point > j.get(inter.user.id, 0):
                msg = " | **BEST SCORE!**"
            
            await inter.message.edit(f"점수: **{self._2048.point}점**{msg}", file = img)

        if self.custom_id == "end":
            with open("json/2048Best.json", "r") as f: j:dict = json.load(f)
            j[str(inter.user.id)] = [self._2048.point, int(time.time())]
            
            with open("json/2048Best.json", "w") as f: json.dump(j, f, indent = 4)
            await inter.message.edit(view = None)
            

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
        

CLIENT.run("MTAyNzAxMDY3MDQ1MDk3ODg5MA.GNEqCf.xDfHg_nf38o6J43wk8ysYqd8gQlqMzQIRa407Q")