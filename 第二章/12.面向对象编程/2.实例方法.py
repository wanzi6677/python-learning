class Car:
    def __init__(self, c_brand,c_color,c_price,c_name):
        self.brand = c_brand
        self.color = c_color
        self.price = c_price
        self.name = c_name

    def running(self):
        print(f"{self.brand}{self.name}正在高速行驶...")

    def total_cost(self,discount,rate):
        return round(self.price*discount+self.price*rate,1)

#创建对象
c1 = Car("BWM","red",999999,"X8")
c1.running()
print(f"{c1.brand}{c1.name}一共花费{c1.total_cost(0.9,0.1)}")