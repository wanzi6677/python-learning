# def reg_stu(name,age,gender="男",city="北京"):

#不定长参数
#1.位置传参,传给一个元组
# def calc_data(*args):
#     max_num = max(args)
#     min_num = min(args)
#     avg_num = sum(args)/len(args)
#     return max_num, min_num, round(avg_num,1)
#
# data = calc_data(1,2,3,4,5,6,7,8,9,10)
# print(data)
# 2.关键字传参,关键字参数传给字典
# def calc_data(*args,**kwargs):
#     """
#
#     :param args: 不定长位置参数
#     :param kwargs: 不定长关键字参数
#         round 保留的小数位个数
#         print 是否打印输出
#     :return:
#     """
#     max_num = max(args)
#     min_num = min(args)
#     avg_num = sum(args)/len(args)
#     if kwargs.get("round") is not None:
#         avg_num = round(avg_num,kwargs.get("round"))
#     if kwargs.get("print"):
#         print(f"最大值：{max_num},最小值：{min_num},平均值：{avg_num}")
#     return max_num, min_num, avg_num
#
# data = calc_data(1,2,5,4,5,6,7,7,9,3,11,round=4,print=True)
# print(data)

#匿名函数 lambda表达式
# add = lambda x,y: x+y
# outline = lambda :print("-----------------------------")
# outline()
# print(add(1,2))

# 需求3：完成如下列表的排序操作，按照每一个元素的字符个数， 从小到大排序 ；
# data_list = ["C++", "C", "Python", "Jack", "PHP", "Java", "Go", "JavaScript", "Rust"]
# print(data_list)
#
# data_list.sort(key=lambda item : len(item), reverse=True)#默认从小到大
# print(data_list)
#

# def factorial(n):
#     if n == 0:
#         return 1
#     else:
#         return n * factorial(n-1)
#
# print(factorial(5))

# def money(*args：tuple[str,float,int],coupon,score,express):
#     """
#
#     :param args: 商品信息
#     :param coupon: 优惠倦
#     :param score: 积分
#     :param express: 运费
#     :return: 最终价格
#     """
#     total_price = [goods[1]*goods[2] for goods in args]
#     total_cost = sum(total_price)
#
#     if total_cost>=5000 and total_cost>=coupon:
#         total_cost = total_cost-coupon
#
#     if total_cost>=5000 and total_cost>=score//100:
#         total_cost = total_cost-score//100
#
#     total_cost = total_cost+express
#     return total_cost


# a2: int = 596
# score: float = 98.5
# hobby2: str = "Python"
# flag: bool = True
# pics:None = None
#
# names2: list[str] = ["A","B","C","D","E","F"]
# phones2:set[str] = {"13789964595","17760453948","1889076534"}
# options:dict[str,int] = {"count":10,"total":2}
# goods:tuple[str,int,int]=("手机",6999,1)
#
# names2.append("1002")



