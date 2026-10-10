class ShoppingCar:
    def __init__(self,name,price,count):
        self.name = name
        self.price = price
        self.count = count

    def __str__(self):
        return f"商品名称： {self.name} ，商品价格：{self.price}，商品数量：{self.count}"



#教务管理系统类
class ShopManagement:
    system_version = "1.0"
    system_name = "购物车管理系统"
    def __init__(self):
        self.shoppingcar_list = []

    def add_shoppingcar(self):
        name = input("请输入商品名称: ")
        for goods in self.shoppingcar_list:
            if goods.name == name:
                print("该商品已经存在，添加失败!")
                return

        price = float(input("请输入商品价格: "))
        count = int(input("请输入商品数量: "))
        goods = ShoppingCar(name, price, count)
        self.shoppingcar_list.append(goods)
        print("添加商品成功~")




    def updata_shoppingcar(self):
        name = input("请输入要修改商品名称: ")

        for goods in self.shoppingcar_list:
            if goods.name == name:
                goods.price = float(input("请输入新的商品价格: "))
                goods.count = int(input("请输入新的商品数量: "))
                print("修改商品成功~")
                break
            else:
                print("没有该商品")



    def remove_shoppingcar(self):
        name = input("请输入要删除的商品名称: ")

        for goods in self.shoppingcar_list:
            if goods.name == name:
                self.shoppingcar_list.remove(goods)
                print("商品信息删除成功")
                break
            else:
                print("没有该商品!!")


    def show_shoppingcar(self):
        for goods in self.shoppingcar_list:
            print(goods)

    def run(self):
        print(f"欢迎使用购物车管理系统 v{ShopManagement.system_version}")


        while True:
            print("#########                                   【菜单】                                            #########")
            print("#                   1.添加购物车  2.修改购物车  3.删除购物车  4.查询购物车  5.退出系统                          #")
            print("########################################################################################################")

            oper = input("\n请输入你要进行的操作:")
            match oper:
                case "1":
                    self.add_shoppingcar()
                case "2":
                    self.updata_shoppingcar()
                case "3":
                    self.remove_shoppingcar()
                case "4":
                    self.show_shoppingcar()
                case "5":
                    print("已经成功退出系统")
                    break
                case _:
                    print("操作不支持，请重新输入！！")

if __name__ == "__main__":
    shopcar = ShopManagement()
    shopcar.run()