# s = "hello Python"
# print(s[4])
# print(s[0:-3:2])
# print(s[ : :-1])

#字符串常用方法
#find() 查找子串，返回第一次出现的索引位置
#count() 统计子串在字符串中出现的次数
#upper() 将字符串里面所有的字母转换为大写
#lower() 将字符串里面所有的字母转换为小写
#split() 将字符串按照指定分隔符分隔为列表
#strip() 去除字符串两端的空白字符或指定字符
#replace() 将字符串里面的指定子串转换为新的子串
#startswith 检查字符串是否以指定子串开头，返回布尔值

# s = "hello-Python-hello-world "
#
# print(s.find("e"))
# print(s.count("o"))
# print(s.upper())
# print(s.lower())
# print(s.split("-"))
# print(s.strip(" "))
# print(s.replace("-", " "))
# print(s.startswith("he"))

# str = input("请输入你的邮箱:")
# if str.count("@")==1 and "." in str:
#     print("邮箱格式正确")
# else:
#     print("邮箱格式错误")

# str = input("请输入一个字符串:")
# str1 = str[::-1]
# if str == str1:
#     print(f"{str}是回文")
# else:
#     print(f"{str}不是回文")

# str = []
# for i in range(10):
#     str1 = input(f"请输入第{i+1}个字符串")
#     str2 = str1[::-1]
#     str3 = str2.upper()
#     str.append(str3)
# for i in str:
#     print(i)

