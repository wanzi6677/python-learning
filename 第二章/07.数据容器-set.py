#存储不重复的元素,set可以自动去重，无序，不能重复，可以修改
# s1 = {"cat", "dog", "mouse","cat", "dog", "mouse"}
# 不能定义空集合{}，{}是字典
# s2 = set()
# print(s1)

# s1 = {100,200,300,400,500,600,700,800}
# s2 = {100,200,300,700,900,1000,1100,1200,1300}
# #add():添加元素到集合中
# #remove():移除集合中的随机元素
# #pop():随机删除集合中的元素并返回
# #clear():清空集合
# #操作两个集合
# #difference():求取两个集合差值（在第一个集合里面但是不在第二个集合里面）
# #union():求并集
# #intersection():求交集
#
#
#
#
# print(s1.intersection(s2))

# 选修足球学生名单
football_set = {"王林", "曾牛", "徐立国", "通天", "天运子", "韩立", "厉飞雨", "乌丑", "紫灵"}

# 选修篮球学生名单
basketball_set = {"张铁", "墨居仁", "王林", "姜老道", "曾牛", "王蝉", "韩立", "天运子", "李化元", "厉飞雨", "云露"}

# 选修法语学生名单
french_set = {"许木", "王卓", "十三", "虎跑", "姜老道", "天运子", "红蝶", "厉飞雨", "韩立", "曾牛"}

# 选修艺术学生名单
art_set = {"通天", "天运子", "韩立", "虎跑", "姜老道", "紫灵"}

print(f"同时修了法语和艺术的学生有：{french_set.intersection(art_set)}")
print(f"同时修了四门课的学生有：{(french_set.intersection(art_set)).intersection(football_set.intersection(basketball_set))}")
print(f"修了足球但是没有修篮球的学生有：{football_set.difference(basketball_set)}")

all_stu = football_set | basketball_set | french_set | art_set
all_set = football_set & basketball_set & french_set & art_set

#集合推导式{i for in set if 条件}
all_stulist = [*football_set, *basketball_set, *french_set, *art_set]
print(all_stulist)
for stu in all_stu:
    print(f"{stu}选修的课程数为{all_stulist.count(stu)}")