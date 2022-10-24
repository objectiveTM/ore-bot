import random
class ColorHax:
    def __init__(self) -> None:
        self.RED = 0xf74b20
        self.BLUE = 0x5833ff
        self.PERPLE = 0x9900ff
        self.PINK = 0xff0080
        self.GRAY = 0x2f3136

    def randomColor(self):
        return random.choice([self.RED , self.BLUE , self.PERPLE , self.PINK , self.GRAY])
    
color = ColorHax()