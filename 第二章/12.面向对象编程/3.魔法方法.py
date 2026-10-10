#以__开头和结尾的方法
class Car:
    def __init__(self, c_brand,c_color,c_price,c_name):
        self.brand = c_brand
        self.color = c_color
        self.price = c_price
        self.name = c_name

    def running(self):
        print(f"{self.brand}{self.name}正在高速行驶...")
    def __eq__(self, other):
        return self.brand == other.brand and self.color == other.color and self.price == other.price and self.name == other.name
    def __ge__(self, other):
        return self.price >= other.price
    def __str__(self):
        return f"{self.brand}{self.name}"

c1 = Car("BWM","red",999999,"X8")
c2 = Car("BWM","red",999999,"X8")

print(c1==c2)
print(c1>=c2)
print(c1)