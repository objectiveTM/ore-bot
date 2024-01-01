import random
from typing import List, Optional, Union
from nextcord import *
from nextcord.components import SelectOption
from nextcord.emoji import Emoji
from nextcord.enums import ButtonStyle
from nextcord.ext import commands as cmds, application_checks
from nextcord.interactions import Interaction
from nextcord.partial_emoji import PartialEmoji
from nextcord.utils import MISSING
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
    global GUESS_CLIENT
    await CLIENT.change_presence(activity=Game(name="정검(정밀검사)"))
    print("RUN")
    print("VERSION: 2.5")
    Vc.clear()
    CLIENT.add_view(Guess())
    GUESS_CLIENT = CLIENT


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
        dt = Vc.leave(member)//15
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

@play2048.subcommand(name = "랭킹", description = "2048의 랭킹를 확인합니다")
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

@CLIENT.slash_command(name = "포인트", description = "자신의 포인트를 가저옵니다")
async def point(inter: Interaction):
    await inter.reponse.send_message(Point(inter.guild).point)
    return
@point.subcommand(name = "랭킹", description = "포인트 랭킹을 표시합니다")
async def pointrank(inter: Interaction):
    if await is_blacklist(inter.user, inter): return
        
    try: await inter.response.defer()
    except: ...
    description = ""
    point_user = Point(inter.guild.id).get_list()
    point_user = sorted(point_user.items(), reverse=True, key=lambda x: x[1])
    for i in point_user[:10]:
        
        user = await CLIENT.fetch_user(i[0])
        description += f"- `{user}` {i[1]}\n"
    
    embed = Embed(title = "포인트 랭킹!", description = description, color = color.BLUE)
    await inter.followup.send(embed = embed)


@point.subcommand(name = "추측", description = "포인트로 추측을 할수있는 게임을 만듭니다")
@application_checks.has_permissions(administrator=True)
async def point_guess(
        inter: Interaction,
        guess1: str = SlashOption(name="첫번째값", description="추측의 첫번째값을 써주세요"),
        guess2: str = SlashOption(name="두번째값", description="추측의 두번째값을 써주세요"),

        point: str = SlashOption(name="포인트_설정", description="포인트값을 보이게할지 숨기게할지 정해주세요" , required=False, choices={"보이기", "숨기기"}),
        user_count: str = SlashOption(name="유저_설정", description="유저수를 보이게할지 숨기게할지 정해주세요" , required=False, choices={"보이기", "숨기기"})
    ):
    if await is_blacklist(inter.user, inter): return
    # embed = Embed(title = "보여줄 정보를 선택해주세요", description = MakeGuess().make_str(), color = color.BLUE)
    # await inter.response.send_message(embed = embed, view=MakeGuess())
    gj = GuessJson()
    message: Message = await inter.channel.send("wait...", view = Guess())
    viewable = {
        "point": point == "보이기",
        "user_count": user_count == "숨기기"
    }
    guess = [guess1, guess2]
    
    gj.make(message.id, viewable, guess)
    await message.edit(embed=Embed(description=gj.make_str(message.id), color=color.BLUE))



# @point_guess.subcommand(name = "감성있게", description = "포인트로 추측을 할수있는 게임을 만듭니다")
# @application_checks.has_permissions(administrator=True)
# async def point_guess_wtf(inter: Interaction):
#     if await is_blacklist(inter.user, inter): return

#     embed = Embed(title = "보여줄 정보를 선택해주세요", description = MakeGuess().make_str(), color = color.BLUE)
#     await inter.response.send_message(embed = embed, view=MakeGuess())







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


@CLIENT.command(name = "포인트랭킹")
async def _pointrank(ctx: cmds.context.Context):
    if await is_blacklist(ctx.message.author, ctx): return
        

    description = ""
    point_user = Point(ctx.guild.id).get_list()
    point_user = sorted(point_user.items(), reverse=True, key=lambda x: x[1])
    for i in point_user[:10]:
        
        user = await CLIENT.fetch_user(i[0])
        description += f"- `{user}` {i[1]}\n"
    
    embed = Embed(title = "포인트 랭킹!", description = description, color = color.BLUE)
    ctx.send(embed=embed)



class Comps(ui.View):
    def __init__(self, comps: list[ui.Select|ui.Button]):
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
    def __init__(self, option = { "point": True,  "user_count": True }, guess: list=["???", "???"]) -> None:
        super().__init__(timeout=600.)
        self.viewable = option
        self.guess = guess

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
        if not inter.user.guild_permissions.administrator: return
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
        if not inter.user.guild_permissions.administrator: return
        await inter.message.edit(embed=Embed(title = "주제를 설정해주세요", description=MakeGuess2(self).make_str()), view=MakeGuess2(self))


    def make_str(self):
        res = ""
        if self.viewable["user_count"]:
            res += "### 유저(30/70)\n"
            res += f"**[30%]** {Emojis.yellowStone*3}{Emojis.blueStone*7} **[50%]**\n"
        if self.viewable["point"]:
            res += "### 포인트(100000/100000)\n"
            res += f"**[50%]** {Emojis.yellowStone*5}{Emojis.blueStone*5} **[50%]**\n"

        if not (self.viewable["user_count"] | self.viewable["point"]):
            res += "### 유저(???/???)\n"
            res += f"**[???]** {Emojis.grayStone*10} **[???]**\n"
            res += "### 포인트(???/???)\n"
            res += f"**[???]** {Emojis.grayStone*10} **[???]**\n"


        return res

class MakeGuess2(ui.View):
    def __init__(self, option: MakeGuess) -> None:
        super().__init__(timeout=None)
        self.option = option

    @ui.button(emoji="<:back:1032996444963090553>", style=ButtonStyle.green)
    async def back_btn(self, button: ui.Button, inter: Interaction):
        if not inter.user.guild_permissions.administrator: return
        await inter.message.edit(embed=Embed(title="보여줄 정보를 선택해주세요", description=self.option.make_str(), color=color.BLUE), view = self.option)

    @ui.button(emoji=Emojis.blueStone, style=ButtonStyle.gray)
    async def one_btn(self, button: ui.Button, inter: Interaction):
        if not inter.user.guild_permissions.administrator: return
        await inter.response.send_modal(GuessModal(self, 0))

    @ui.button(emoji=Emojis.yellowStone, style=ButtonStyle.gray)
    async def two_btn(self, button: ui.Button, inter: Interaction):
        if not inter.user.guild_permissions.administrator: return
        await inter.response.send_modal(GuessModal(self, 1))


    @ui.button(emoji="<:speaker:1043817834003832863>", style=ButtonStyle.green)
    async def make_btn(self, button: ui.Button, inter: Interaction):
        if not inter.user.guild_permissions.administrator: return
        gj = GuessJson()
        message: Message = await inter.channel.send("wait...", view = Guess())
        gj.make(message.id, self.option.viewable, self.option.guess)
        await message.edit(embed=Embed(description=gj.make_str(message.id), color=color.BLUE))

    
    def make_str(self):
        res = f"{Emojis.blueStone} {self.option.guess[0]}\n{Emojis.yellowStone} {self.option.guess[1]}\n\n"
        res += self.option.make_str()
        return res

class GuessModal(ui.Modal):
    def __init__(self, guess: MakeGuess2, idx: int) -> None:
        super().__init__("추가하기")
        df_value = guess.option.guess[idx]
        if df_value == "???": df_value = None
        self.option = ui.TextInput(
            "여기에 입력해주세요",
            placeholder = "뭐하지",
            required=True,
            default_value=df_value,
            style = TextInputStyle.short
        )
        self.idx = idx
        self.guess = guess
        self.add_item(self.option)

    async def callback(self, inter: Interaction) -> None:
        self.guess.option.guess[self.idx] = self.option.value
        embed = Embed(title= "주제를 설정해주세요")
        embed.description = self.guess.make_str()
        await inter.message.edit(embed = embed, view = MakeGuess2(self.guess.option))

class GuessBtn(ui.Button):
    def __init__(self, idx: int) -> None:
        self.id = id
        self.idx = idx
        if idx != -1: return super().__init__(style=ButtonStyle.blurple, custom_id=f"guessbtn-{self.idx}",  emoji=Emojis.blueStone if not idx else Emojis.yellowStone)
        super().__init__(style=ButtonStyle.red, custom_id=f"guessbtn-{self.idx}",  emoji=Emojis.grayStone)

    async def callback(self, inter: Interaction) -> None:
        if self.idx != -1:
            return await inter.response.send_modal(GuessBetModal(self.idx))
        if not inter.permissions.administrator: return
        await inter.response.send_message(view = Comps([GuessEnd(inter.message.id)]), ephemeral=True)

# class GuessEndOption(SelectOption):
#     def __init__():
#         ...

class GuessEnd(ui.Select):
    def __init__(self, msg_id: int) -> None:
        title = GuessJson().get(msg_id).title;
        super().__init__(
            placeholder="정답을 선택해주세요",
            options=[
                SelectOption(label=title[0], emoji=Emojis.blueStone, value=0),
                SelectOption(label=title[1], emoji=Emojis.yellowStone, value=1),
            ]
        )
        self.msg_id = msg_id
    async def callback(self, inter: Interaction) -> None:
        gj = GuessJson()
        msg = inter.channel.get_partial_message(self.msg_id)
        embed = Embed(title=f"정답은 {gj.get(self.msg_id).title[int(self.values[0])]} 였습니다!", description=gj.make_str(self.msg_id), color=ColorHax.BLUE)
        gj.close(inter.guild_id, self.msg_id, int(self.values[0]))
        await msg.edit(embed = embed, view=None)
        # await inter.user.send(file=File(fp="html/point.html", filename="test.html"))

class Guess(ui.View):
    def __init__(self) -> None:
        super().__init__(timeout=None)
        self.add_item(GuessBtn(0))
        self.add_item(GuessBtn(1))
        self.add_item(GuessBtn(-1))


class GuessBetModal(ui.Modal):
    def __init__(self, idx: int) -> None:
        super().__init__("추측!", timeout=None)
        self.point = ui.TextInput(
            label = "몇 포인트를 배팅하실껀가요?",
            style = TextInputStyle.short,
            default_value = "0",
            placeholder="1121"
        )
        self.add_item(self.point)
        self.idx = idx;
    
    async def callback(self, inter: Interaction) -> None:
        point = 0
        try:
            point = int(self.point.value)
        except:
            return await inter.response.send_message("숫자를 입력해주세요 :)", ephemeral=True)
        gj = GuessJson()
        msg = gj.vote(inter.guild.id, inter.message.id, inter.user.id, point, self.idx)
        await inter.response.send_message(msg, ephemeral=True)
        await inter.message.edit(content="", embed=Embed(description=gj.make_str(inter.message.id), color=color.BLUE))

if __name__ == "__main__":
    CLIENT.run(open("TOKEN.secret").read())
