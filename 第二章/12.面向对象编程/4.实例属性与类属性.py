#实例属性：每个具体对象的属性，各个对象独立
#类属性：这个类本身的属性，所有实例共享

class Car:
    #类属性
    wheel = 4
    tax_rate = 0.1
    def __init__(self, c_brand,c_color,c_price,c_name):
        #实例属性
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


