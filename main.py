import random
from typing import Optional
from nextcord import *
from nextcord.ext import commands as cmds
from func import *
import typing
import time
import play2048 as p_2048

import json

async def is_blacklist(member: Member, channel: ChannelType):
    blacklist: list[int] = eval(open("blacklist").read())
    if member.id in blacklist:
        try: 
            await channel.response.send_message("LMAO")
        except:...
        await channel.send("LMAO")
        return True
    return False



INTENTS = Intents.all()
CLIENT = cmds.Bot(intents = INTENTS, command_prefix = "/")
CUSTOM = p_2048.customs.ORIGINAL.value

@CLIENT.event
async def on_ready():
    await CLIENT.change_presence(activity=Game(name="정검(정밀검사)"))
    print("RUN")
    print("VERSION: 2.5")
    Vc.clear()


@CLIENT.event
async def on_message(message: Message):
    server = message.guild.id
    member = message.author

    try: 
        point = Point(server)
        point.add_point(member, 1)
    except: pass

    await CLIENT.process_commands(message)  

@CLIENT.event
async def on_voice_state_update(member: Member, before: VoiceState, after: VoiceState):
    if before.channel == None and after.channel != None: # vc join
        Vc.join(member)
        return
    
    if before.channel != None and after.channel == None: # vc leave
        dt = Vc.leave(member)//3
        point = Point(CLIENT.get_channel(before.channel.id).guild.id)
        point.add_point(member, dt)
        return

      


@CLIENT.slash_command(description = "2048을 플레이합니다", name = "2048")
async def play2048(inter:Interaction, type:str = SlashOption(description = "플레이할것을 선텍하세요", choices={"이미지": "img", "이모지":"emj"}, required=False)):
    if await is_blacklist(inter.user, inter): return
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
    if await is_blacklist(inter.user, inter): return
        
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


@CLIENT.slash_command(name = "포인트랭킹", description = "포인트 랭킹을 표시합니다")
async def pointrank(inter: Interaction):
    if await is_blacklist(inter.user, inter): return
        
    try: await inter.response.defer()
    except: ...
    description = ""
    point_user = Point(inter.guild.id).get_list()
    point_user = sorted(point_user.items(), reverse=True, key=lambda x: x[1])
    for i in point_user[:10]:
        
        user = await CLIENT.fetch_user(i[0])
        print(i)
        description += f"- `{user}` {i[1]}\n"
    
    embed = Embed(title = "포인트 랭킹!", description = description, color = color.BLUE)
    await inter.followup.send(embed = embed)






    

@CLIENT.command(name = "2048")
async def _play2048(ctx: cmds.context.Context, type: str = None):
    if await is_blacklist(ctx.message.author, ctx): return
        
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
    if await is_blacklist(ctx.message.author, ctx): return
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

@CLIENT.command(name = "aaa")
async def aaa(ctx: cmds.context.Context):
    if await is_blacklist(ctx.message.author, ctx): return
    embed = Embed(title = "2048 rank!", description = f"{Emojis.blueStone} 100(10명)\n{Emojis.yellowStone} 500(5명)", color = color.BLUE)
    await ctx.send(embed = embed, view=MakeGuess("sus"))


@CLIENT.command(name = "포인트랭킹")
async def _pointrank(ctx: cmds.context.Context):
    if await is_blacklist(ctx.message.author, ctx): return
        

    description = ""
    point_user = Point(ctx.guild.id).get_list()
    point_user = sorted(point_user.items(), reverse=True, key=lambda x: x[1])
    for i in point_user[:10]:
        
        user = await CLIENT.fetch_user(i[0])
        print(i)
        description += f"- `{user}` {i[1]}\n"
    
    embed = Embed(title = "포인트 랭킹!", description = description, color = color.BLUE)
    ctx.send(embed=embed)



class Comps(ui.View):
    def __init__(self, comps: list[ui.Select]):
        super().__init__()
        for comp in comps:
            self.add_item(comp)
            
class Play2048s(ui.View):
    def __init__(self, comps: list[ui.Button], _2048: p_2048.Game, inter: Interaction | cmds.context.Context):
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
    def __init__(self, *, type: str = "img", user: Member = None, _2048: p_2048.Game = None, style:ButtonStyle = ButtonStyle.secondary, label:typing.Optional[str] = "ㅤ", disabled:bool = False, custom_id:typing.Optional[str] = None, url:typing.Optional[str] = None, emoji: typing.Optional[str | Emoji | PartialEmoji] = None, row: typing.Optional[int] = None):
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
            
            if self._type == "emj" or self._type == "emoji" or self._type == "이모지":
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


class MakeGuess(ui.View):
    def __init__(self, description: str, option = { "point": True,  "user_count": True, "percent": True }) -> None:
        super().__init__(timeout=600.)
        self.description = description
        self.viewable = option

    @ui.button(emoji="<:back:1032996444963090553>", style=ButtonStyle.green, disabled=True)
    async def back_btn(self, button: ui.Button, inter: Interaction):
        ...

    @ui.button(label="포인트", style=ButtonStyle.blurple)
    async def point_btn(self, button: ui.Button, inter: Interaction):
        if self.viewable["point"]:
            button.style = ButtonStyle.gray
        else:
            button.style = ButtonStyle.blurple

        self.viewable["point"] = not self.viewable["point"]
        embed = inter.message.embeds[0]
        embed.description = self.make_str()
        await inter.message.edit(embed = embed, view = self)

    @ui.button(label="유저수", style=ButtonStyle.blurple)
    async def user_count_btn(self, button: ui.Button, inter: Interaction):
        if self.viewable["user_count"]:
            button.style = ButtonStyle.gray
        else:
            button.style = ButtonStyle.blurple

        self.viewable["user_count"] = not self.viewable["user_count"]
        embed = inter.message.embeds[0]
        embed.description = self.make_str()

        await inter.message.edit(embed = embed, view = self)

    @ui.button(emoji="<:front:1032996551229976636>", style=ButtonStyle.green)
    async def next_btn(self, button: ui.Button, inter: Interaction):
        await inter.message.edit(embed=Embed("주제"), view=MakeGuess2(self))
        ...


    # @ui.button(label="퍼센트", style=ButtonStyle.blurple)
    # async def percent_btn(self, button: ui.Button, inter: Interaction):
    #     if self.viewable["percent"]:
    #         button.style = ButtonStyle.gray
    #     else:
    #         button.style = ButtonStyle.blurple

    #     self.viewable["percent"] = not self.viewable["percent"]
    #     embed = inter.message.embeds[0]
    #     await inter.message.edit(embed = embed, view = self)

    def make_str(self):
        res = ""
        if self.viewable["user_count"] & self.viewable["point"]:
            res += f"{Emojis.blueStone} 100(10명)\n" 
            res += f"{Emojis.yellowStone} 500(5명)"

        elif self.viewable["user_count"]:
            res += f"{Emojis.blueStone} 10명\n" 
            res += f"{Emojis.yellowStone} 5명"
        
        elif self.viewable["point"]:
            res += f"{Emojis.blueStone} 100\n" 
            res += f"{Emojis.yellowStone} 500"
        else:
            res += f"{Emojis.blueStone} ???\n" 
            res += f"{Emojis.yellowStone} ???"

        return res

class MakeGuess2(ui.View):
    def __init__(self, option) -> None:
        super().__init__(timeout=None)
        self.option = option




if __name__ == "__main__":
    CLIENT.run(open("TOKEN.secret").read())
