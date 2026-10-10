#元组：不能修改，只能查询的序列,元组使用（）定义
#方法：count():统计某元素在元组中出现的次数
#     index():查找某个元素在索引中的索引位置
# t1 = (5,4,23,523,67,74,23,4,66,32,26)
#
# print(t1[0])
# print(t1[::2])
# print(t1.count(4))
# print(t1.index(67))

#组包和解包
# t1 = (5,7,9,1)
# t2 = 5,7,9,1
#
# #基础解包
# a,b,c,d = t1
# #扩展解包
# x,*y,z = t2
# s,*o = t2
# *o,e = t2
# print(a,b,c,d)
# print(x,y,z,s,o)

#元组
# a = 10
# b = 20
# b,a = a,b
# print(a,b)
#
# x,y,z = 100,200,300
# z,x,y = x,y,z
# print(x,y,z)

name = ["王林","利姆湾","十三","增牛","周易","王卓","红蝶","虚李过","序幕","巡天"]
yw = [85,92,78,88,95,76,89,75,86,66]
sx = [92,88,85,79,96,82,91,69,89,59]
yy = [78,95,82,91,89,77,94,82,98,72]

for x in range(10):
    print(f"{name[x]}的各科总分是{yw[x] + sx[x] + yy[x]}，各科平均分是{(yw[x]+sx[x]+yy[x])/3:.1f}")

print(f"语文最高分是{max(yw)},最低分是{min(yw)},平均分是{sum(yw)/len(yw)}")
print(f"数学最高分是{max(sx)},最低分是{min(sx)},平均分是{sum(sx)/len(sx)}")
print(f"英语最高分是{max(yy)},最低分是{min(yy)},平均分是{sum(yy)/len(yy)}")

print("成绩优秀的学生有：",end="")
for x in range(10):
    if (yw[x] + sx[x] + yy[x])/3>90:
        print(f"{name[x]}",end=" ")

