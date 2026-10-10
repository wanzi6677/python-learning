# def out_line():
#     print("___________________")
#
# out_line()
# import math
#
#
#计算圆的面积和周长
# import math
#
#
# def mcircle_area(r):
#     """
#     根据圆的半径得到面积和周长
#     :param r: 圆的半径
#     :return: 圆的面积和周长
#     """
#     return round(math.pi * r * r,2),round(math.pi*2*r,2)
#
# area,len = mcircle_area(5)#解包
# print(area)
# print(len)

#函数的嵌套调用是使用的栈结构，先进后出
# def func_c():
#     print("  进入 func_c")
#     # 做一些操作
#     print("  离开 func_c")
#
# def func_b():
#     print(" 进入 func_b")
#     func_c()
#     print(" 离开 func_b")
#
# def func_a():
#     print("进入 func_a")
#     func_b()
#     print("离开 func_a")
#
# func_a()

# def tri(d,h):
#     return round(0.5*d*h,2)
#
# print(tri(5.4,1.44))

# def count_yy(str):
#     count = 0
#     for x in str:
#         if x in "aeiouAEIOU":
#             count += 1
#     return count
#
# print(count_yy("shauisgdushdqy2tudhaskd"))

# def grades(list):
#     return max(list),min(list),round(sum(list)/len(list),1)
#
# grades_list = [589,609,643,677,455,503,487]
#
# max_grades,min_grades,avg_grades = grades(grades_list)
# print(f"最高分：{max_grades},最低分：{min_grades},平均分：{avg_grades}")
# def huiwen(str):
#     str1 = str[::-1]
#     if str1 == str:
#         return True
#     else:
#         return False
#
# test = input("请输入一个字符串")
# print(f"{test}是否为回文串:{huiwen(test)}")

# def time_change(seconds):
#     hour, minute, second = seconds // 3600, seconds % 3600 // 60, seconds % 60
#     return hour, minute, second
#
# seconds = int(input("请输入一个秒数:"))
# hour, minute, second = time_change(seconds)
# print(f"{seconds}秒一共是：{hour}:{minute}:{second}")

