class Student:
    def __init__(self,name,chinese,math,english):
        self.name = name
        self.chinese = chinese
        self.math = math
        self.english = english

    def __str__(self):
        return f"姓名： {self.name} | 语文：{self.chinese} | 数学：{self.math} | 英语：{self.english}"

    def update_score(self,chinese = None,math = None,english = None):
        if chinese is not None:
            self.chinese = chinese
        if math is not None:
            self.math = math
        if english is not None:
            self.english = english

#教务管理系统类
class EduManagement:
    system_version = "1.0"
    system_name = "教务管理系统"
    def __init__(self):
        self.student_list = []

    def add_student(self):
        name = input("请输入学生姓名: ")
        if name in self.student_list:
            print("该学生已经存在，添加失败!")
            return

        chinese = int(input("请输入学生语文成绩: "))
        math = int(input("请输入学生数学成绩: "))
        english = int(input("请输入学生英语成绩: "))
        if 0<=chinese<=100 and 0<=math<=100 and 0<=english<=100:
            stu = Student(name,chinese,math,english)
            self.student_list.append(stu)
            print("添加学生成功~")
        else:
            print("分数不合理！！！")


    def updata_student(self):
        name = input("请输入要修改学生姓名: ")

        for stu in self.student_list:
            if stu.name == name:
                print(f"当前成绩:{stu}")
                chinese = int(input("请输入学生新的语文成绩: "))
                math = int(input("请输入学生新的数学成绩: "))
                english = int(input("请输入学生新的英语成绩: "))
                if 0 <= chinese <= 100 and 0 <= math <= 100 and 0 <= english <= 100:
                    stu = Student(name, chinese, math, english)
                    self.student_list.append(stu)
                    print("修改学生成绩成功~")
                else:
                    print("分数不合理！！！")


        print("没有该学生!!")


    def remove_student(self):
        name = input("请输入要删除学生姓名: ")

        for stu in self.student_list:
            if stu.name == name:
                self.student_list.remove(stu)
                print("学生信息删除成功")

        print("没有该学生!!")

    def query_student(self):
        name = input("请输入要查询的学生姓名: ")

        for stu in self.student_list:
            if stu.name == name:
                print(f"当前成绩:{stu}")

        print("没有该学生!!")

    def show_student(self):
        for stu in self.student_list:
            print(stu)

    def run(self):
        print(f"欢迎使用教务管理系统 v{EduManagement.system_version}")


        while True:
            print(
                "#########                                   【菜单】                                            #########")
            print(
                "#       1.添加学生信息  2.修改学生成绩  3.删除学生成绩  4.查询指定学生成绩  5.列出所有学生成绩  6.退出系统            #")
            print(
                "########################################################################################################")

            oper = input("\n请输入你要进行的操作:")

            try:
                match oper:
                    case "1":
                        self.add_student()
                    case "2":
                        self.updata_student()
                    case "3":
                        self.remove_student()
                    case "4":
                        self.query_student()
                    case "5":
                        self.show_student()
                    case "6":
                        print("已经成功退出系统")
                        break
                    case _:
                        print("操作不支持，请重新输入！！")

            except Exception as e:
                print("出现错误，联系管理员解决,或者检查输入",e)

if __name__ == "__main__":
    edu_management = EduManagement()
    edu_management.run()