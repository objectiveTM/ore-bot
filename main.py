import random
from nextcord import *
from nextcord.ext import commands as cmds
from func import *
import typing
import time
import play2048 as p_2048

import json



INTENTS = Intents.all()
# INTENTS.all()
CLIENT = cmds.Bot(intents = INTENTS, command_prefix = "/")
CUSTOM = p_2048.customs.ORIGINAL.value

@CLIENT.event
async def on_ready():
    print("RUN")
    print("VERSION: 2.5")
    

@CLIENT.slash_command(description = "노동을 합니다")
async def 광질(inter:Interaction):
    await inter.response.defer()
    ore = Ore(inter.user)
    rank = ore.rank
    await inter.followup.send(embed = rank.embed, view = Comps([ore]))

@CLIENT.slash_command(description = "인벤토리를 확인합니다")
async def 인벤토리(inter:Interaction):
    await inter.response.defer()
    await inter.followup.send(view = Comps([Inv(inter.user)]))

@CLIENT.slash_command(description = "마법상점에 들립니다")
async def 마법상점(inter:Interaction):
    embed = Embed(title = "마법상점| 0", description = "마법과 관련된 아이템을 받을수있어요! 아직 공사중이여서 좋은 아이템을 없다네요...", color=color.PERPLE)
    embed.set_image(url="https://media.discordapp.net/attachments/1140727841303052458/1140727841466626190/spiritual-book-glow.gif")
        
    await inter.response.send_message(embed = embed, view = Comps([MagicStore(inter.user, i+1) for i in range(3)]))

@CLIENT.slash_command(description = "2048을 플레이합니다", name = "2048")
async def play2048(inter:Interaction, type:str = SlashOption(description = "플레이할것을 선텍하세요", choices={"이미지": "img", "이모지":"emj"}, required=False)):
    _2048 = p_2048.Game()
    views = [
        Play2048(disabled = True), Play2048(label = "w", style = ButtonStyle.blurple, user = inter.user, _2048 = _2048, custom_id="up", type=type), Play2048(disabled = True), Play2048(label = "end", style = ButtonStyle.red, user = inter.user, _2048 = _2048, custom_id="end", type=type),
        Play2048(label = "a", style = ButtonStyle.blurple, user = inter.user, _2048 = _2048, row = 2, custom_id="left", type=type), Play2048(label = "s", style = ButtonStyle.blurple, user = inter.user, _2048 = _2048, row = 2, custom_id="down", type=type), Play2048(label = "d", style = ButtonStyle.blurple, user = inter.user, _2048 = _2048, row = 2, custom_id="right", type=type), Play2048(disabled = True, row = 2)
    ]
    if type == "img" or type == None:
        await inter.response.send_message(f"점수: **0점**", file = File(_2048.encodingImage(CUSTOM).image_bytes, f"point_0.png"), view = Play2048s(views, _2048, inter))
    else:
        with open("json/2048Emoji.json", "r") as f: emoji2048:dict = json.load(f)
        _emj = _2048.arr
        emj = ""
        for i in _emj:
            for j in i:
                emj += emoji2048[str(j)]
            emj += "\n"
        
        embed = Embed(title = f"점수: **0점**", color = color.BLUE)
        await inter.response.send_message(emj, embed = embed, view = Play2048s(views, _2048, inter))
        
@CLIENT.slash_command(name = "2048랭크", description = "2048의 랭크를 확인합니다")
async def rank2048(inter:Interaction):
    try: await inter.response.defer()
    except: ...
    with open("json/2048Best.json", "r") as f: _j:dict = json.load(f)
    
    j = sorted(_j.items(), key=lambda x : x[1][0], reverse = True)
    i = 1
    description = ""
    isShow = False
    for rank in j[:10]:
        user = utils.get(CLIENT.get_all_members(), id = int(rank[0]))
        description += f"{i}등, `{user}`: **{rank[1][0]}점** <t:{rank[1][1]}:R>\n"
        i += 1
        
        if not isShow: isShow = inter.user == user
        
    
    if not isShow:
        i = 1
        description += f".\n"*3
        for rank in j:
            if inter.user.id == int(rank[0]):
                user = utils.get(CLIENT.get_all_members(), id = int(rank[0]))
                description += f"{i}등, `{user}`: **{rank[1][0]}점** <t:{rank[1][1]}:R>\n"
                break
            i += 1
    embed = Embed(title = "2048 rank!", description = description, color = color.BLUE)
    await inter.followup.send(embed = embed)



@CLIENT.command(name = "광질")
async def _광질(ctx: cmds.context.Context):
    ore = Ore(ctx.author)
    rank = ore.rank
    await ctx.send(embed = rank.embed, view = Comps([ore]))

@CLIENT.command(name = "인벤토리")
async def _인벤토리(ctx: cmds.context.Context):
    await ctx.send(view = Comps([Inv(ctx.author)]))

@CLIENT.command(name="마법상점")
async def _마법상점(ctx: cmds.context.Context):
    embed = Embed(title = "마법상점| 0", description = "마법과 관련된 아이템을 받을수있어요! 아직 공사중이여서 좋은 아이템을 없다네요...", color=color.PERPLE)
    embed.set_image(url="https://media.discordapp.net/attachments/1140727841303052458/1140727841466626190/spiritual-book-glow.gif")
      
    await ctx.send(embed = embed, view = Comps([MagicStore(ctx.author, i+1) for i in range(3)]))
    

@CLIENT.command(name = "2048")
async def _play2048(ctx: cmds.context.Context, type:str = None):
    _2048 = p_2048.Game()
    views = [
        Play2048(disabled = True), Play2048(label = "w", style = ButtonStyle.blurple, user = ctx.author, _2048 = _2048, custom_id="up", type=type), Play2048(disabled = True), Play2048(label = "end", style = ButtonStyle.red, user = ctx.author, _2048 = _2048, custom_id="end", type=type),
        Play2048(label = "a", style = ButtonStyle.blurple, user = ctx.author, _2048 = _2048, row = 2, custom_id="left", type=type), Play2048(label = "s", style = ButtonStyle.blurple, user = ctx.author, _2048 = _2048, row = 2, custom_id="down", type=type), Play2048(label = "d", style = ButtonStyle.blurple, user = ctx.author, _2048 = _2048, row = 2, custom_id="right", type=type), Play2048(disabled = True, row = 2)
    ]
    if type == "emj" or type == "emoji" or type == "이모지":
        with open("json/2048Emoji.json", "r") as f: emoji2048:dict = json.load(f)
        _emj = _2048.arr
        emj = ""
        for i in _emj:
            for j in i:
                emj += emoji2048[str(j)]
            emj += "\n"
        
        embed = Embed(title = f"점수: **0점**", color = color.BLUE)
        await ctx.send(emj, embed = embed, view = Play2048s(views, _2048, ctx))
        
    else:
        await ctx.send(f"점수: **0점**", file = File(_2048.encodingImage(CUSTOM).image_bytes, f"point_0.png"), view = Play2048s(views, _2048, ctx))

@CLIENT.command(name = "2048랭크")
async def _rank2048(ctx: cmds.context.Context):
    with open("json/2048Best.json", "r") as f: _j:dict = json.load(f)
    
    j = sorted(_j.items(), key=lambda x : x[1][0], reverse = True)
    i = 1
    description = ""
    isShow = False
    for rank in j[:10]:
        user = utils.get(CLIENT.get_all_members(), id = int(rank[0]))
        description += f"{i}등, `{user}`: **{rank[1][0]}점** <t:{rank[1][1]}:R>\n"
        i += 1
        
        if not isShow: isShow = ctx.author == user
        
    
    if not isShow:
        i = 1
        description += f".\n"*3
        for rank in j:
            if ctx.author.id == int(rank[0]):
                user = utils.get(CLIENT.get_all_members(), id = int(rank[0]))
                description += f"{i}등, `{user}`: **{rank[1][0]}점** <t:{rank[1][1]}:R>\n"
                break
            i += 1
    embed = Embed(title = "2048 rank!", description = description, color = color.BLUE)
    await ctx.send(embed = embed)




class Comps(ui.View):
    def __init__(self, comps: list[ui.Select]):
        super().__init__()
        for comp in comps:
            self.add_item(comp)
            
class Play2048s(ui.View):
    def __init__(self, comps: list[ui.Button], _2048: p_2048.Game, inter: Union[Interaction, cmds.context.Context]):
        super().__init__(timeout = 300)
        for comp in comps:
            self.add_item(comp)
        self.inter = inter
        self._2048 = _2048
            
    async def on_timeout(self) -> None:
        with open("json/2048Best.json", "r") as f: j:dict = json.load(f)
        if type(self.inter) == Interaction:
            if self._2048.point > j.get(str(self.inter.user.id), [0])[0]:
                j[str(self.inter.user.id)] = [self._2048.point, int(time.time())]
            
            await self.inter.edit_original_message(view = None)
        else:
            if self._2048.point > j.get(str(self.inter.author.id), [0])[0]:
                j[str(self.inter.author.id)] = [self._2048.point, int(time.time())]
            
            await self.inter.edit_original_message(view = None)
        with open("json/2048Best.json", "w") as f: json.dump(j, f, indent = 4)

class Play2048(ui.Button):
    def __init__(self, *, type: str = "img", user: Member = None, _2048: p_2048.Game = None, style:ButtonStyle = ButtonStyle.secondary, label:typing.Optional[str] = "ㅤ", disabled:bool = False, custom_id:typing.Optional[str] = None, url:typing.Optional[str] = None, emoji: typing.Optional[Union[str, Emoji, PartialEmoji]] = None, row: typing.Optional[int] = None):
        if user != None:
            super().__init__(style = style, label = label, disabled = disabled, custom_id = f"{custom_id}|{user.id}", url = url, emoji = emoji, row = row)
        else:
            super().__init__(style = style, label = label, disabled = disabled, custom_id = custom_id, url = url, emoji = emoji, row = row)
        self._2048 = _2048
        self._type = type
        
    async def callback(self, inter: Interaction):
        if self.custom_id.split("|")[1] != str(inter.user.id): return await inter.response.send_message("자신의것을 사용하세요!", ephemeral = True)
        await inter.response.defer()
        m = 0
        if self.custom_id.startswith("up"):    m  = p_2048.move.UP
        if self.custom_id.startswith("down"):  m  = p_2048.move.DOWN
        if self.custom_id.startswith("left"):  m  = p_2048.move.LEFT
        if self.custom_id.startswith("right"): m  = p_2048.move.RIGHT
        
        if m != 0:
            self._2048.move(m)
            with open("json/2048Best.json", "r") as f: j:dict = json.load(f)
            msg = " | **BEST SCORE!**" if self._2048.point > j.get(str(inter.user.id), [0])[0] else ""
            
            if type == "emj" or type == "emoji" or type == "이모지":
                with open("json/2048Emoji.json", "r") as f: emoji2048:dict = json.load(f)
                _emj = self._2048.arr
                emj = ""
                for i in _emj:
                    for j in i:
                        emj += emoji2048[str(j)]
                    emj += "\n"
                    
                
                embed = Embed(title = f"점수: **{self._2048.point}점**", color = color.BLUE)
                await inter.message.edit(emj, embed = embed)
                
            else:
                img = File(self._2048.encodingImage(CUSTOM).image_bytes, f"point_{self._2048.point}.png")
            
                await inter.message.edit(f"점수: **{self._2048.point}점**{msg}", file = img)
                
                

        if self.custom_id.startswith("end"):
            with open("json/2048Best.json", "r") as f: j:dict = json.load(f)
            if self._2048.point > j.get(str(inter.user.id), [0])[0]:
                j[str(inter.user.id)] = [self._2048.point, int(time.time())]
            
                with open("json/2048Best.json", "w") as f: json.dump(j, f, indent = 4)
            await inter.message.edit(view = None)
            await rank2048(inter)
    
class Inv(ui.Select):
    def __init__(self, _user):
        self._user = _user
        self.inventory = Inventory(_user)
        options = self.inventory.encoing()
        super().__init__(placeholder="눌러서 인벤토리를 확인하세요!", options=options)
    async def callback(self, inter:Interaction):
        await inter.message.edit(embed = Mining(self._user).findRank(id = self.values[0]).embed)

class Ore(ui.Button):
    def __init__(self, _user:Member):
        self._user = _user
        self.mining = Mining(self._user)
        rank = random.randint(1, 2000)
        if (rank == 1): rank = "전설"
        elif (rank < 202): rank = "에픽"
        elif (rank < 404): rank = "레어" # Not Found
        else: rank = "일반"
        self.rank = self.mining.findRank(rank = rank)
            
        super().__init__(style=self.rank.color.button, emoji = self.rank.emoji)
        
    async def callback(self, inter:Interaction):
        await inter.response.defer()
        await self.mining.get(self.rank.id)
        rank = random.randint(1, 2000)
        if (rank == 1): rank = "전설"
        elif (rank < 202): rank = "에픽"
        elif (rank < 404): rank = "레어"
        else: rank = "일반"
        
        self.rank = self.mining.findRank(rank = rank)
        self.style = self.rank.color.button
        self.emoji = self.rank.emoji
        await inter.message.edit(embed = self.rank.embed, view = Comps([self]))

class MagicStore(ui.Button):
    def __init__(self, _user: Member, id: str, disabled: bool = False):
        if (str(id).startswith("end")): super().__init__(emoji = Emojis.blueStone, label = f"구매", custom_id=str(id), disabled=disabled)
        else: super().__init__(emoji = Emojis.blueStone, label = f"{id}개 사용", custom_id=str(id), disabled=disabled)
        self.mining = func.Mining(_user)
        self._user = _user

    async def callback(self, inter:Interaction):
        try: id = int(self.custom_id.split("|")[1])
        except: id = int(self.custom_id)
        if (self.custom_id.startswith("end")):
            try:
                await self.mining.use("blueStone:0", id)
            except Exception as e:
                return await inter.response.send_message(e, ephemeral = True)
            item = self.mining.findRank(rank = "book")
            await self.mining.get(item.id)
            
            v = Comps([MagicStore(inter.user, i+1) for i in range(3)])
            v.add_item(MagicStore(inter.user, f"end|{id}", not self.mining.isUse("blueStone:0", id)))
            
            return await inter.message.edit(embed = item.embed, view = v)
            
        v = Comps([MagicStore(inter.user, i+1) for i in range(3)])
        v.add_item(MagicStore(inter.user, f"end|{self.custom_id}", not self.mining.isUse("blueStone:0", int(self.custom_id))))
        embed = Embed(title = f"마법상점| {id}", description = "마법과 관련된 아이템을 받을수있어요! 아직 공사중이여서 좋은 아이템을 없다네요...", color=color.PERPLE)
        embed.set_image(url="https://media.discordapp.net/attachments/1140727841303052458/1140727841466626190/spiritual-book-glow.gif")
        await inter.message.edit(embed = embed, view=v)


if __name__ == "__main__":
    CLIENT.run(open("TOKEN.secret").read())
