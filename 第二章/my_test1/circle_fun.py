#计算圆的面积
import math

__all__ = ['circle_len','circle_area','PI']
PI = 3.14
NAME = "原神牛逼"
def circle_area(r):
    return round(math.pi * r**2,1)

def circle_len(r):
    return round(2*math.pi*r,1)

def log_apt():
    print("apt"*30)

if __name__ == '__main__':
    log_apt()