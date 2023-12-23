import json
from .Emojis import *
from .Point import *
from nextcord import *
GUESS_CLIENT: Client = None
class GuessJson:
    def __init__(self) -> None:
        with open("json/guess.json", "r") as f: self.guess: dict = json.load(f)


    def make(self, id: int, option: dict[str, bool], title: list[str]):
        id = str(id)
        self.guess[id] = {
            "title": title,
            "point": [{}, {}],
            "option": option
        }
        with open("json/guess.json", "w") as f: json.dump(self.guess, f, indent=4)

    def vote(self, server: int, id: int, user: int, point: int, idx: int) -> str:
        p = Point(server)
        print(idx)
        old_idx = None
        add_point = 0
        if str(user) in self.guess[str(id)]["point"][idx]:
            add_point = self.guess[str(id)]["point"][idx][str(user)]
            p.add_point(user, add_point)
            del self.guess[str(id)]["point"][idx][str(user)]
            old_idx = idx
        if str(user) in self.guess[str(id)]["point"][int(not idx)]:
            add_point = self.guess[str(id)]["point"][int(not idx)][str(user)]
            p.add_point(user, add_point)
            del self.guess[str(id)]["point"][int(not idx)][str(user)]
            old_idx = int(not idx)
            
        if p.get_user(user) - point >= 0:
            self.guess[str(id)]["point"][idx][str(user)] = point
            p.add_point(user, -point)
            if self.guess[str(id)]["point"][idx][str(user)] == 0: del self.guess[str(id)]["point"][idx][str(user)]
        else:
            if old_idx != None:
                p.add_point(user, -add_point)
                self.guess[str(id)]["point"][old_idx][str(user)] = add_point
                if self.guess[str(id)]["point"][old_idx][str(user)] == 0: del self.guess[str(id)]["point"][old_idx][str(user)]



        with open("json/guess.json", "w") as f: json.dump(self.guess, f, indent=4)
        return "추측을 완료했어요"
    
    def make_str(self, id: int) -> str:
        res = f"{Emojis.blueStone} {self.guess[str(id)]['title'][0]}\n{Emojis.yellowStone} {self.guess[str(id)]['title'][1]}\n\n"
        print(sum_key(self.guess[str(id)]["point"][0].items(), lambda x: x[1]))

        if self.guess[str(id)]["option"]["user_count"]:
            print(len(self.guess[str(id)]['point'][0]), len(self.guess[str(id)]['point'][1]))
            percent = _percent(len(self.guess[str(id)]['point'][0]), len(self.guess[str(id)]['point'][1]))
            res += f"### 유저({len(self.guess[str(id)]['point'][0])}/{len(self.guess[str(id)]['point'][1])})\n"
            if percent == [0, 0]:
                res += f"**[0.0%]** {Emojis.grayStone*10} **[0.0%]**\n"
            else:
                res += f"**[{percent[0]:.1f}%]** {Emojis.yellowStone*round(percent[0]/10)}{Emojis.blueStone*round(percent[1]/10)} **[{percent[1]:.1f}%]**\n"

        if self.guess[str(id)]["option"]["point"]:
            sums = [sum_key(self.guess[str(id)]["point"][0].items(), lambda x: x[1]), sum_key(self.guess[str(id)]["point"][1].items(), lambda x: x[1])]
            percent = _percent(sums[0], sums[1])
            res += f"### 포인트({sums[0]}/{sums[1]})\n"
            if percent == [0, 0]:
                res += f"**[0.0%]** {Emojis.grayStone*10} **[0.0%]**\n"
            else:
                res += f"**[{percent[0]:.1f}%]** {Emojis.yellowStone*round(percent[0]/10)}{Emojis.blueStone*round(percent[1]/10)} **[{percent[1]:.1f}%]**\n"

        if not (self.guess[str(id)]["option"]["user_count"] | self.guess[str(id)]["option"]["point"]):
            res += "### 유저(???/???)\n"
            res += f"**[???]** {Emojis.grayStone*10} **[???]**\n"
            res += "### 포인트(???/???)\n"
            res += f"**[???]** {Emojis.grayStone*10} **[???]**\n"

        return res

    def is_empty(self, id: int):
        if self.guess.get(str(id), True) == True:
            return True
        return False
    
    def close(self, server: int, id: int, idx: int):
        p = Point(server)
        for user_point in self.guess[str(id)]["point"][idx].items():
            p.add_point(int(user_point[0]), user_point[1])

def _percent(a, b) -> list[float]:
    s = a + b
    if a+b:
        return [a/s*100, b/s*100]
    return [0, 0]

def sum_key(iter, key) -> int:
    res: int = 0
    for i in iter:
        try: 
            res += key(i)
        except: ...
    return res