#数据容器（数组）

#1.列表list
# s = [54,23,45,67,12,"apt","okun",True]
# print(s[0])
# print(s[-1])
# print(s[-2])
# print(s[7])
#
# #修改
# s[-2] = "欧坤"
# print(s[-2])
#
# del s[-2]
# print(s)
#
# for item in s:
#     print(item,end=" ")

#列表的切片
# s = ["a","b","c","d","e","f","A","B","C","D","E","F"]
# a = s[0:11:2]
# print(a)
# print(s)

#列表的方法
# append()  在列表尾部加元素
# insert()  在指定索引前插入一个元素
# remove()  移除第一个匹配到的值
# pop()  删除列表指定位置的元素
# sort()  对列表排序（列表元素数据类型一致）
# reverse()  反转列表元素

# s = [3,4,5,12,42,56,0,6,241]
# s.append(26)
# print(s)
# s.insert(1,32)
# print(s)
# s.remove(241)
# print(s)
# s.pop(-2)
# print(s)
# s.sort()
# print(s)
# s.reverse()
# print(s)


# s = [0]*10
# for i in range(10):
#     s[i] = int(input(f"请输入第{i+1}个数字:"))
#
# s.sort()
# print("该数组元素排序为",s,"\n最大值为",s[9],",最小值为",s[0])

# s = []
# for i in range(10):
#     num = int(input(f"请输入第{i+1}个数字:"))
#     s.append(num)
#
# s.sort()
# print("该数组元素排序为",s,"\n最大值为",s[9],",最小值为",s[0])
# print(f"平均值为{sum(s)/len(s)}")

# 直接合并后去重（用集合）
# num_list1 = [19,23,54,64,875,20,109,232,123,54]
# num_list2 = [55,80,72,35,60,123,54,29,91]
# merged = [*num_list1 , *num_list2]#解包操作
# new_list = []
# for i in merged:
#     if i not in new_list:
#         new_list.append(i)
# print(new_list)

# num_list = []
# for i in range(1,21):
#     num_list.append(i**2)
#
# print(num_list)
#
# new_list = []
# for i in num_list:
#     if i%2==0:
#         new_list.append(i**2)
#
# print(new_list)

#列表推导式 [要插入的值 for i in 序列/列表]
# num_list2 = [j**2 for j in range(1,21)]
# print(num_list2)

# num_list = [12,32,45,34,12,34,32,56,76,55,343]
# new_list = [i**2 for i in num_list if i%2==0]
# print(new_list)

#列表表达式：[你要的东西 for i in 序列/列表 if 条件]
# list1 = ['M', 'A', 'C', 'E', 'F', 'G', 'H', 'L', 'N', 'I', 'J', 'K', 'O']
# list2 = ['X', 'Z', 'T', 'Y', 'D', 'E', 'F', 'G']
# list3 = ['W', 'A', 'S', 'D']
#
# list = list1 +list2 +list3
# new_list = []
# for i in list:
#     if i not in new_list:
#         new_list.append(i)
# new_list.sort()
# print(new_list)

# list1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]
# new_list = [i**2 for i in list1 if (i%3 == 0 or i%5 == 0)]
# print(new_list)

# list1 = [11, 2, 31, 4, -5, 15, 17, 28, 49, 10, -11, 16, 54, -14, 36, -16, 87, -39]
# list = [i for i in list1 if i > 0]
# print(list)


