class Solution(object):
    def setZeroes(self, matrix):
        """
        :type matrix: List[List[int]]
        :rtype: None Do not return anything, modify matrix in-place instead.
        """
        m = len(matrix)
        n = len(matrix[0])
        first_row_has_zero = any(matrix[0][j] == 0 for j in range(n))
        first_col_has_zero = any(matrix[i][0] == 0 for i in range(m))

        for i in range(1, m):
            for j in range(1, n):
                if matrix[i][j] == 0:
                    matrix[i][0] = 0
                    matrix[0][j] = 0

        for i in range(1, m):
            for j in range(1, n):
                if matrix[i][0] == 0 or matrix[0][j] == 0:
                    matrix[i][j] = 0

        if first_row_has_zero:
            for j in range(n):
                matrix[0][j] = 0

        if first_col_has_zero:
            for i in range(m):
                matrix[i][0] = 0


if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding="utf-8")

    def check(matrix, expect):
        original = [row[:] for row in matrix]      # 二维必须逐行拷,list(matrix) 只拷外层
        Solution().setZeroes(matrix)
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
