class Solution(object):
    def setZeroes(self, matrix):
        """
        :type matrix: List[List[int]]
        :rtype: None Do not return anything, modify matrix in-place instead.
        题号:LeetCode Hot 100 第 18 题(矩阵 · 先记录后修改)
        链接:https://leetcode.cn/problems/set-matrix-zeroes/
        难度:中等
        题意:若某元素为 0,把它所在的整行、整列都置 0,必须原地修改。
        思路(O(m+n) 空间的及格版:先记录,后修改):
            1. 不能"找到一个 0 就立刻刷整行整列" —— 刷出来的新 0 会被后续扫描
               当成"原生的 0"继续向外扩散(边遍历边修改自己正在读的输入)。
            2. 所以分两趟:第一趟只记录哪些行、哪些列要清;第二趟按记录执行。
            3. 记录用 set 而不是 list,避免同一行/列有多个 0 时重复追加。
        复杂度:
            时间 O(m*n) —— 扫描一遍 + 按记录清零
            空间 O(m+n) —— 两个 set,不满足题目的进阶要求
        易错点:
            1. 一边遍历一边就地清零 -> 假 0 扩散(本题的原始坑)。
            2. 用 list 记录不判重 -> 全 0 矩阵会记下 m*n 条,
               清理阶段工作量放大到 O(m*n*m),白白多算几百倍。
            3. 这是"及格版",题目明确说 O(m+n) space still not the best,
               最优解见 setZeroes2。
        自测用例:见 __main__,9 条(调用 setZeroes2)。
        """
        zero_rows = set()
        zero_cols = set()
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                if matrix[i][j] == 0:
                    zero_rows.add(i)
                    zero_cols.add(j)

        for i in zero_rows:
            for j in range(len(matrix[i])):
                matrix[i][j] = 0

        for i in zero_cols:
            for j in range(len(matrix)):
                matrix[j][i] = 0

    def setZeroes2(self, matrix):
        """
        :type matrix: List[List[int]]
        :rtype: None Do not return anything, modify matrix in-place instead.
        题号:LeetCode Hot 100 第 18 题(矩阵 · 借第一行第一列当标志,最优解 O(1) 空间)
        链接:https://leetcode.cn/problems/set-matrix-zeroes/
        难度:中等
        题意:若某元素为 0,把它所在的整行、整列都置 0,必须原地修改。
        思路(把"两套记录"塞进矩阵自己):
            1. O(m+n) 版用两个 set 记"哪行哪列要清",信息量一共 m+n 个是/否。
               这题的考点是:能不能借矩阵自己的第 0 行和第 0 列来存这 m+n 个标志。
            2. 位置天然对齐:matrix[i][0] 天生位于第 i 行 -> 记"第 i 行要清";
               matrix[0][j] 天生位于第 j 列 -> 记"第 j 列要清"。用 0 表示"要清"。
               借的东西本来就要被改写成 0(只要该行/列有 0,这些位置最终也必然是 0),
               所以不丢信息 —— 这和第 17 题"借下标"同样是借本来就会被改写的地方。
            3. 但 matrix[0][0] 同时属于第 0 行和第 0 列,一个格子背不下两件事。
               -> 第 0 行、第 0 列"原本是否含 0"必须提前存进两个布尔变量,
                  在写标志之前就算出来(之后再查就查不到了)。
            4. 顺序(本题全部难点):
               (a) 先扫 i>=1,j>=1,用 matrix[i][0] / matrix[0][j] 当标志;
               (b) 再清内部区域 i>=1,j>=1(此时只读第 0 行第 0 列的标志);
               (c) 最后用两个布尔变量清第 0 列、第 0 行。
               顺序绝不能反:先清第 0 行,标志全变 0 -> 所有列被误清。
        复杂度:
            时间 O(m*n) —— 扫矩阵常数趟
            空间 O(1) —— 只借矩阵自己的格子 + 两个布尔变量
        易错点:
            1. 第一步(写标志)若从 i=0 或 j=0 开始扫 -> 把第 0 行第 0 列的原始数据
               覆盖成标志,之后就用布尔变量之外的东西去判断"第 0 行/列要不要清",
               必然出错。实测反例:[[1,0],[1,1]] 曾被多清成 [[0,0],[0,0]]。
            2. 两个布尔变量必须写在写标志之前,顺序反了就是读到已被污染的值。
            3. matrix[0][0] 一个格子不许替两件事做决定(初版两个 if 用了同一个条件,
               穷举 3x3 时失败 42/512)。
            4. 清第 0 行/列的步骤必须放在最后,否则会抹掉自己正在用的标志。
            5. 会原地修改 matrix(虽然 rtype 是 None)。测试里 check() 必须用
               [row[:] for row in matrix] 深拷贝,list(matrix) 只拷外层。
        自测用例:见 __main__,9 条。另做过:穷举 1x1~4x4 全部 0/1 矩阵 74000+ 种,
            加上 1..6 维随机 20000 组(含非 0/1 取值),均 0 不一致;
            200x200 实测 3.69 ms。
        """
        m = len(matrix)
        n = len(matrix[0])
        first_row_has_zero = any(matrix[0][j] == 0 for j in range(n))
        first_col_has_zero = any(matrix[i][0] == 0 for i in range(m))

        # 步骤 1:借第 0 行/第 0 列当标志(从 1 开始,不碰第 0 行第 0 列的原始数据)
        for i in range(1, m):
            for j in range(1, n):
                if matrix[i][j] == 0:
                    matrix[i][0] = 0
                    matrix[0][j] = 0

        # 步骤 2:按标志清内部区域
        for i in range(1, m):
            for j in range(1, n):
                if matrix[i][0] == 0 or matrix[0][j] == 0:
                    matrix[i][j] = 0

        # 步骤 3:最后处理第 0 行/第 0 列(用提前存好的布尔变量,不看 matrix[0][0])
        if first_col_has_zero:
            for i in range(m):
                matrix[i][0] = 0

        if first_row_has_zero:
            for j in range(n):
                matrix[0][j] = 0


if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding="utf-8")

    def check(matrix, expect):
        original = [row[:] for row in matrix]      # 二维必须逐行拷,list(matrix) 只拷外层
        Solution().setZeroes2(matrix)
        flag = "✅" if matrix == expect else "❌"
        print(f"{flag} {original} → {matrix}（期望 {expect}）")

    check([[1,1,1],[1,0,1],[1,1,1]], [[1,0,1],[0,0,0],[1,0,1]])   # 题目原例 1
    check([[0,1,2,0],[3,4,5,2],[1,3,1,5]], [[0,0,0,0],[0,4,5,0],[0,3,1,0]])  # 原例 2:0 在角上
    check([[1,0]], [[0,0]])          # ← 只有一行:行与标志重合
    check([[1],[0]], [[0],[0]])      # ← 只有一列
    check([[1]], [[1]])              # 单格、非 0:不能被清
    check([[0]], [[0]])              # 单格、是 0
    check([[1,2,3]], [[1,2,3]])      # 一行且无 0,整行不能被误清
    check([[1,2],[3,4]], [[1,2],[3,4]])   # 没有 0:一个都不能动
    check([[1,0],[1,1]], [[0,0],[1,0]])