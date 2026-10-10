# a = int(input("输入一个a的值:"))
# if a>0:
#     a=1
# else:
#     a=-1
#
#     print(f"a的值为{a}")
from unittest import case

# zhang_hao = "18888888888"
# password = "666888"
# hao = input("请输入账号")
# ma = input("请输入密码")
# if hao == zhang_hao and password == ma:
#     print("恭喜登录成功")
# else:
#     print("请重新登录")

# year = int(input("请输入一个年份:"))
# if (year%100!=0 and year%4==0) or (year%400==0):
#     print(f"{year}是闰年")
# else:
#     print(f"{year


# name = input("请输入用户名:")
# password = input("请输入密码:")
# if (name == "admin" and password == "666888") or (name == "root" and password == "547527") or (name == "zhangsan" and password == "123456") :
#     print("登陆成功")
# else:
#     print("用户名或密码错误")

# a = int(input("输入三角形第一条边长："))
# b = int(input("输入三角形第二条边长："))
# c = int(input("输入三角形第三条边长："))
#
# if a+b>c and a+c>b and b+c>a:
#     if a ==b and b==c:
#         print("等边三角形")
#     elif a==b or b==c or a==c:
#         print("等腰三角形")
#     else:
#         print("普通三角形")
# else:
#     print("不是三角形")

# day = input("今天星期几")
#
# match day:
#         case "1":
#             print("周一")
#         case "2":
#             print("周二")
#         case "3":
#             print("周三")
#         case "4":
#             print("周四")
#         case "5":
#             print("周五")
#         case "6":
#             print("周六")
#         case "7":
#             print("周日")
#         case _:
#             print("瞎说呀")


# fu = input("请输入操作输入")
#
# match fu:
#     case "上" | "w" | "W":
#         print("角色向上移动")
#     case "下" | "s" | "S":
#         print("角色向上移动")
#     case "左"|"a" | "A":
#         print("角色向左移动")
#     case "右"|"d" | "D":
#         print("角色向右移动")
#     case "跳"|" ":
#         print("角色跳跃")
#     case "攻击"|"j"|"J":
#         print("角色发动攻击")
#     case "退出" | "esc"|"ESC":
#         print("角色退出游戏")
#     case _:
#         print("不合理的操作")

# a = 0;
# while a < 10:
#     print("python,啦啦啦啦啦")
#     a += 1

# sum = 0
# a = 1
# while a<=100:
#     if a%2==0:
#         sum+=a
#     a+=1
# print(sum)
#

# msg = input("输入你要遍历的字符串：")
#
# for c in msg:
#     print(c)
# else:
#     print("ok")

# sum = 0;
# for i in range(1,100,2):
#     sum += i
# else:
#     print(f"加和为{sum}")

# sum = 0
# for i in range(102,500,3):
#     sum += i
# else:
#     print(f"加和为{sum}")

# m = int(input("请输入长方形的长"))
# n = int(input("请输入长方形的宽"))
#
# for i in range(0,n):
#     for j in range(0,m):
#         print("*",end=" ")
#     print()

# for i in range(1,7):
#     for j in range(1,i+1):
#         print(f"{j}",end = "\t")
#     print()

# for i in range(1,9):
#      for j in range(1,9):
#          if i%2!=0:
#              if (j % 2 == 0):
#                  print("⬜", end="\t")
#              else:
#                  print("⬛", end="\t")
#          elif i%2==0:
#              if (j % 2 == 0):
#                  print("⬛", end="\t")
#              else:
#                  print("⬜", end="\t")
#      print()

# for i in range(1,9):
#      for j in range(1,9):
#              if ((j+i)% 2 == 0):
#                  print("⬛", end="\t")
#              else:
#                  print("⬜", end="\t")
#      print()



# while True:
#     hao = input("请输入你的用户名")
#     password = input("请输入你的密码")
#     if hao =="" or password == "":
#         print("用户名或密码不能为空")
#         continue
#     elif hao =="admin" and password =="666888":
#         break
#     elif hao =="zhangsan" and password =="123456":
#         break
#     elif hao =="taoge" and password =="888666":
#         break
#     else:
#         print("用户名或密码错误，请重新输入！")
# print("登录成功，欢迎进入b站首页")


# import random
# num = random.randint(1, 100)
# while True:
#     a = int(input("输入你猜测的数字："))
#     if a == num:
#         break
#     elif a > num:
#         print("猜大了")
#         continue
#     elif a < num:
#         print("猜小了")
#         continue
# print("猜测正确，游戏结束")