import json
from .Emojis import *
class GuessJson:
    def __init__(self) -> None:
        with open("json/guess.json", "r") as f: self.guess: dict = json.load(f)


    def make(self, id: int, option: dict[str, bool], title: list[str]):
        id = str(id)
        self.guess[id] = {
            "title": title,
            "point": [0, 0],
            "user": [[], []],
            "option": option
        }
        with open("json/guess.json", "w") as f: json.dump(self.guess, f, indent=4)

    def vote(self, id: int, user: int, idx: int) -> str:
        if user in self.guess[str(id)]["user"][idx]:
            return "이미 추측하신곳이에요, 다른걸 눌러야해요"
        if user in self.guess[str(id)]["user"][int(not idx)]:
            self.guess[str(id)]["user"][int(not idx)].remove(user)
        self.guess[str(id)]["user"][idx].append(user)

        with open("json/guess.json", "w") as f: json.dump(self.guess, f, indent=4)
        return "추측을 완료했어요"
    
    def make_str(self, id: int) -> str:
        res = f"{Emojis.blueStone} {self.guess[str(id)]['title'][0]}\n{Emojis.yellowStone} {self.guess[str(id)]['title'][1]}\n\n"
        
        if self.guess[str(id)]["option"]["user_count"]:
            percent = _percent(len(self.guess[str(id)]['user'][0]), len(self.guess[str(id)]['user'][1]))
            res += f"### 유저({len(self.guess[str(id)]['user'][0])}/{len(self.guess[str(id)]['user'][1])})\n"
            res += f"**[{percent[0]:.1f}%]** {Emojis.yellowStone*percent[0]}{Emojis.blueStone*percent[1]} **[{percent[1]:.1f}%]**\n"

        if self.guess[str(id)]["option"]["point"]:
            percent = _percent(self.guess["point"][0], self.guess["point"][1])
            res += f"### 포인트({self.guess['point'][0]}/{self.guess['point'][1]})\n"
            res += f"**[{percent[0]:.1f}%]** {Emojis.yellowStone*percent[0]}{Emojis.blueStone*percent[1]} **[{percent[1]:.1f}%]**\n"

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
    
def _percent(a, b) -> list[float]:
    s = a + b
    return [a/s*100, b/s*100]