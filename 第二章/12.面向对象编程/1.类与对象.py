# #定义类-->不推荐
# class Car:
#     pass
#
# #创建对象
# c1 = Car()
# #动态给对象添加属性
# c1.brand = "BMW"
# c1.color = "red"
# c1.price = 99999
# c1.name = "X5"
#
# print(c1.__dict__)#以字典形式输出


class Car:
    def __init__(self, c_brand,c_color,c_price,c_name):
        self.brand = c_brand
        self.color = c_color
        self.price = c_price
        self.name = c_name

#创建对象
c1 = Car("BWM","red",999999,"X8")
print(c1.__dict__)
