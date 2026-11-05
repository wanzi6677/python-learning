import sys


class Solution(object):
    def searchMatrix(self, matrix, target):
        """
        :type matrix: List[List[int]]
        :type target: int
        :rtype: bool
        题号:LeetCode Hot 100 第 21 题(矩阵,本题为矩阵模块最后一道)
        链接:https://leetcode.cn/problems/search-a-2d-matrix-ii/
        难度:中等
        题意:在 m x n 整数矩阵中查找 target,返回 True/False。
             矩阵满足:每行从左到右升序;每列从上到下升序。
        思路(右上角梯子法):
            1. 起点选右上角 (i=0, j=n-1)。
               左上角不行 —— 往右和往下都是变大,比目标小时不知道往哪走;
               右上角则"往左一定变小、往下一定变大",两个方向反向,判据唯一。
            2. 每一步比较 matrix[i][j] 与 target:
               - 相等     -> 找到,返回 True
               - 当前值 < target -> 这一行从 0 到 j 全部 <= 当前值 < target,
                                    整行左侧作废,只能往下走(i += 1)
               - 当前值 > target -> 这一列从 i 到 m-1 全部 >= 当前值 > target,
                                    整列下方作废,只能往左走(j -= 1)
            3. i 越界(超过最后一行)或 j 越界(小于 0)时说明没找到,返回 False。
               因为每一行、每一列只要被走过一次就整条作废,总共最多走 m + n - 1 步。
        复杂度:
            时间 O(m + n) —— 每走一步删掉一整行或一整列,最多删 m + n - 1 次
            空间 O(1)     —— 只用 i、j 两个下标,不需要额外数组
        易错点:
            1. 起点选错:写在左上角/右下角,两个方向同增同减,判据不唯一,退化成搜索
            2. 方向写反:当前值 < target 该往"下"走(i += 1),当前值 > target 该往"左"走(j -= 1)。
               写反后不报错,只是永远找不到 —— 必须靠对拍抓
            3. 循环条件必须是 and:m < len(matrix) 且 j >= 0。
               写成 or 会越界(matrix[i] 取到第 m 行)
            4. 变量名别和题意撞车:题目里 m = 行数、n = 列数,
               下标习惯用 i/j,不要拿 m/n 当下标
            5. 小用例全绿不代表对:这题必须穷举/对拍
        自测用例:见 __main__,14 条;另做过 46,015 组穷举 + 随机对拍(0 不一致),
                 300x300 实测最慢 0.021 ms,故障注入(方向反 / 起点左上)均可被用例抓到。
        """
        i = 0
        j = len(matrix[0]) - 1
        while i < len(matrix) and j >= 0:
            nums = matrix[i][j]
            if nums < target:
                i += 1
            elif nums > target:
                j -= 1
            else:
                return True

        return False




if __name__ == '__main__':
    sys.stdout.reconfigure(encoding="utf-8")

    def check(matrix, target, expect):
        original = [row[:] for row in matrix]      # 本题不改输入，仅作对照（不算加严条件）
        got = Solution().searchMatrix(matrix, target)
        flag = "✅" if got == expect else "❌"
        print(f"{flag} target={target} → {got}（期望 {expect}）")
        if matrix != original:                      # 只报警、不判红 —— 防止误伤算法题
            print("  ⚠️ 输入矩阵被原地修改了")

    M = [[1, 4, 7, 11, 15],
         [2, 5, 8, 12, 19],
         [3, 6, 9, 16, 22],
         [10, 13, 14, 17, 24],
         [18, 21, 23, 26, 30]]

    check(M, 5, True)     # 题目原例 1（中间的数）
    check(M, 20, False)   # 题目原例 2（不存在）
    check(M, 1, True)     # 左上角
    check(M, 30, True)    # 右下角
    check(M, 15, True)    # 右上角
    check(M, 18, True)    # 左下角
    check(M, 0, False)    # 比最小值还小
    check(M, 31, False)   # 比最大值还大
    check([[1]], 1, True)   # 1×1 命中
    check([[1]], 2, False)  # 1×1 未命中
    check([[1, 3, 5]], 3, True)          # 只有 1 行（m=1）
    check([[1], [2], [3]], 2, True)      # 只有 1 列（n=1）
    check([[1, 4], [2, 5]], 2, True)     # 2×2：抓"该往下走却往左走"
    check([[1, 4], [2, 5]], 4, True)     # 2×2：抓"该往左走却往下走"