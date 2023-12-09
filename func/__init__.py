import random
if __name__ == "__main__":
    rank = random.randint(1 , 1000)
    t = 1
    n = 10000
    tArr = []
    while (len(tArr) < n):
        while (rank != 1):
            t += 1
            rank = random.randint(1 , 1000)
        tArr.append(t)
        rank = 0
    t = 0
    for i in tArr:
        t += i
    print(tArr)
    print(int(t/(n+1)))
        
        

else:
    from .ColorHax import *
    from .Emojis import *
    from .Vc import *
    from .Point import *

    ERROR_404_ITEM = Exception("404 Not Found: 아이템을 찾을수 없습니다.")
    ERROR_505_ENOUGHT = Exception("505 Not Enought: 아이템을 이 충분하지 않습니다.")