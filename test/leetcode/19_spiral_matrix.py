class Solution(object):
    def spiralOrder(self, matrix):
        """
        :type matrix: List[List[int]]
        :rtype: List[int]
        题号:LeetCode Hot 100 第 19 题(螺旋矩阵)
        链接:https://leetcode.cn/problems/spiral-matrix/
        难度:中等
        题意:按"右 → 下 → 左 → 上"由外向内一圈圈走,返回访问顺序。
             矩阵不一定正方形(m 与 n 可以不等)。
        思路(四边界收缩):
            1. top / bottom / left / right 定义成"还没走过的矩形"的四条边,
               初始是整个矩阵。
            2. 一圈 = 沿剩余矩形的四条边各走一条:
               上边(top 行,左→右)→ 右边(right 列,上→下)
               → 下边(bottom 行,右→左)→ 左边(left 列,下→上)
            3. 每段都必须避开上一段已经收过的那个角:
               第 2 段从 top+1 起(避开 (top,right));
               第 3 段从 right-1 起(避开 (bottom,right));
               第 4 段从 bottom-1 起(避开 (bottom,left))。
            4. 第 3、4 段前用 if 挡住"重复走同一条边":
               if top < bottom 才走下边 —— 否则只剩 1 行,第 1 段已收完;
               if left < right 才走左边 —— 否则只剩 1 列,第 2 段已收完。
            5. 四段走完后统一收缩四条边,进入内圈。
        复杂度:
            时间 O(m*n) —— 每个格子恰好被收进 result 一次。
            空间 O(1)    —— 除输出数组外只用了 4 个整数边界。
        易错点:
            1. range(a, b, -1) 要求 a > b。写成 range(left, right, -1)(a < b)
               不会报错,而是静默空转 → 整整少走一段,结果是"缺一段"而不是崩溃。
            2. 单行或单列时,第 3、4 段会重复收取第 1、2 段刚收过的同一行/列,
               必须用 if top < bottom / if left < right 挡住。
               (m == 1 时第 3 段自己的 range 是非空的,挡不住自己)
            3. 第 3 段起点必须是 right-1,直接从 right 起会把 (bottom, right)
               收第二遍(那一格已被第 2 段收走)。
            4. while 用 top <= bottom and left <= right,不能用 < ,
               否则 1×1 的矩阵一格都收不到。
            5. 边界的更新放在这一圈四段都走完之后,让四个 if 看到的是本圈的值;
               要么每段之后立即收缩,两种写法不能混。
        自测用例:见 __main__,8 条;另做过穷举对拍 1×1 ~ 5×5 全部 0/1 矩阵
                 共 35794186 组(对照方向游走暴力解),0 不一致。
        """
        if not matrix:
            return []

        result = []
        top = 0
        bottom = len(matrix) - 1
        left = 0
        right = len(matrix[0]) - 1
        while top <= bottom and left <= right:
            for i in range(left, right + 1):
                result.append(matrix[top][i])

            for i in range(top + 1, bottom + 1):
                result.append(matrix[i][right])

            if top < bottom:
                for i in range(right-1, left-1, -1):
                    result.append(matrix[bottom][i])

            if left < right:
                for i in range(bottom-1, top, -1):
                    result.append(matrix[i][left])

            top += 1
            bottom -= 1
            left += 1
            right -= 1

        return result


if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding="utf-8")

    def check(matrix, expect):
        original = [row[:] for row in matrix]      # 二维深拷贝:list(matrix) 只拷外层
        got = Solution().spiralOrder(matrix)
        flag = "✅" if got == expect else "❌"
        print(f"{flag} {original} → {got}（期望 {expect}）")

    check([[1,2,3],[4,5,6],[7,8,9]], [1,2,3,6,9,8,7,4,5])          # 题目原例
    check([[1,2,3,4],[5,6,7,8],[9,10,11,12]], [1,2,3,4,8,12,11,10,9,5,6,7])  # 非正方形:最后一行倒走
    check([[1]], [1])                                               # 1×1
    check([[1,2,3]], [1,2,3])                                       # ← 照妖镜:单行,左段会重复收割
    check([[1],[2],[3]], [1,2,3])                                   # ← 照妖镜:单列,上段会重复收割
    check([[1,2],[3,4]], [1,2,4,3])                                 # 2×2:一圈正好走完
    check([[1,2],[3,4],[5,6]], [1,2,4,6,5,3])                       # 3×2:高度大于宽度
    check([[1,2,3],[4,5,6]], [1,2,3,6,5,4])                         # 2×3:宽度大于高度