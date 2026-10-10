# ==========================================================
# 最基础的学生管理系统（第一章：基础语法版）
# 功能：1.添加学生  2.删除学生  3.修改学生
#       4.查询学生  5.显示全部学生  6.退出系统
# 数据存储：列表 students，列表里每个元素是一个字典
#           {"姓名": 姓名, "年龄": 年龄, "成绩": 成绩}
# ==========================================================

print("欢迎使用学生管理系统！")

# 用一个列表保存所有学生信息，一开始没有任何学生
students = []

while True:
    # 1.打印菜单
    print("##########              【菜单】              ##########")
    print("#   1.添加学生   2.删除学生   3.修改学生                #")
    print("#   4.查询学生   5.显示全部学生   6.退出系统            #")
    print("########################################################")

    # 2.接收用户的输入
    num = input("请选择要执行的操作(1-6): ")

    # 3.根据输入执行对应的操作
    if num == "1":
        # ---------- 添加学生 ----------
        name = input("请输入学生姓名：")

        # 判断该学生是否已经存在
        is_exist = False
        for stu in students:
            if stu["姓名"] == name:
                is_exist = True
                break

        if is_exist:
            print(f"{name} 已经存在，添加失败！")
        else:
            age = int(input("请输入学生年龄："))
            score = float(input("请输入学生成绩："))
            students.append({"姓名": name, "年龄": age, "成绩": score})
            print(f"添加学生 {name} 成功~")

    elif num == "2":
        # ---------- 删除学生 ----------
        name = input("请输入要删除的学生姓名：")

        index = -1
        for i in range(len(students)):
            if students[i]["姓名"] == name:
                index = i
                break

        if index == -1:
            print("该学生不存在，删除失败！")
        else:
            students.pop(index)
            print(f"删除学生 {name} 成功~")

    elif num == "3":
        # ---------- 修改学生 ----------
        name = input("请输入要修改的学生姓名：")

        for stu in students:
            if stu["姓名"] == name:
                print(f"该学生原来的信息是：{stu}")
                stu["年龄"] = int(input("请输入新的年龄："))
                stu["成绩"] = float(input("请输入新的成绩："))
                print(f"修改学生 {name} 的信息成功~")
                break
        else:
            print("该学生不存在，修改失败！")

    elif num == "4":
        # ---------- 查询学生 ----------
        name = input("请输入要查询的学生姓名：")

        for stu in students:
            if stu["姓名"] == name:
                print(f"姓名：{stu['姓名']} | 年龄：{stu['年龄']} | 成绩：{stu['成绩']}")
                break
        else:
            print("该学生不存在，查询失败！")

    elif num == "5":
        # ---------- 显示全部学生 ----------
        if len(students) == 0:
            print("暂无学生信息，请先添加学生！")
        else:
            print(f"当前共有 {len(students)} 名学生：")
            for stu in students:
                print(f"姓名：{stu['姓名']} | 年龄：{stu['年龄']} | 成绩：{stu['成绩']}")

    elif num == "6":
        # ---------- 退出系统 ----------
        print("已经退出学生管理系统，欢迎下次使用！")
        break

    else:
        # ---------- 其他非法输入 ----------
        print("操作不支持，请重新输入(1-6)！")
