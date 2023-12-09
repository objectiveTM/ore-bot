from nextcord import Member
import json, time

class Vc:
    def clear():
        with open("json/vc.json", "r") as f: vc: dict = json.load(f)
        vc = {}
        with open("json/vc.json", "w") as f: json.dump(vc, f, indent=4)

    def join(member: Member):
        with open("json/vc.json", "r") as f: vc: dict = json.load(f)
        vc[str(member.id)] = vc.get(str(member.id), time.time())
        with open("json/vc.json", "w") as f: json.dump(vc, f, indent=4)

    def leave(member: Member) -> int:
        with open("json/vc.json", "r") as f: vc: dict = json.load(f)
        try:
            old_t = vc[str(member.id)]
        except:
            return 0
        del vc[str(member.id)]
        with open("json/vc.json", "w") as f: json.dump(vc, f, indent=4)
        return (time.time() - old_t)//1
