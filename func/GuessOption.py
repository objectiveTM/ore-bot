class GuessOptionOption:
    def __init__(self, option):
            self.point: bool = option["point"]
            self.user_count: bool = option["user_count"]

class GuessOption:
    def __init__(self, guess: dict[str, list[str|dict]]):
        self.title: list[str] = guess["title"]
        self.point: list[dict] = guess["point"]
        self.option: GuessOptionOption = GuessOptionOption(guess["option"])
