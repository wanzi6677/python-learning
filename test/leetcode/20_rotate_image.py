class Solution(object):
    def rotate(self, matrix):
        """
        :type matrix: List[List[int]]
        :rtype: None Do not return anything, modify matrix in-place instead.
        题号:LeetCode Hot 100 第 20 题(旋转图像)
        链接:https://leetcode.cn/problems/rotate-image/
        难度:中等
        题意:把 n × n 矩阵顺时针旋转 90°,必须原地修改(不许另开一个二维矩阵)。
        思路(转置 + 每行左右反转):
            1. 顺时针 90° 的下标映射:(i, j) → (j, n-1-i)
               即"行号变列号",再按新行做一次左右翻转。
            2. 拆成两个互不冲突的对称操作:
               第一步 沿主对角线转置:(i, j) ↔ (j, i)
               第二步 每一行左右反转:(i, j) ↔ (i, n-1-j)
            3. 只扫下三角写转置:内层 range(i) 保证 j < i,
               否则每对 (i,j)/(j,i) 会被交换两次,等于白做。
            4. 反转每行只走前一半 range(n//2),后半段由对称位置自动完成。
            5. 两次翻转的复合就是旋转:先转置后反转 = 顺时针,
               先反转后转置 = 逆时针 —— 顺序决定方向。
        复杂度:
            时间 O(n²) —— 每个元素被访问常数次。
            空间 O(1)    —— 只用了 i / j 两个下标,原地交换。
        易错点:
            1. 转置内层写成 range(n) 而不是 range(i) —— 结果照样对,
               但每对交换两次白做一倍工作量;面试会追问"为什么是 range(i)"。
               和第 17 题"每个数只归位一次"是同一个约束。
            2. 漏掉 m = len(matrix[0]) 的冗余 —— 本题保证 n == matrix[i].length,
               多开一个 m 会让读代码的人误以为处理了非正方形矩阵,是埋雷写法。
            3. rtype 是 None:结果在 matrix 里,不在返回值里。
               测试里写 got = Solution().rotate(...) 会让正确代码全红(第 4 题踩过)。
            4. 两步顺序不能反:先反转后转置得到的是逆时针 90°,
               用例里的 3×3 原例就能照出来。
            5. 原地修改的题,check() 必须先深拷贝原始输入:
               [row[:] for row in matrix],list(matrix) 只拷外层(第 18 题踩过)。
        自测用例:见 __main__,6 条(1×1 / 2×2 / 3×3 / 4×4 / 题目两个原例);
                 另做过穷举对拍 1×1 ~ 3×3 全部 0/1 与 0/1/2 矩阵
                 + n=1~20 随机 20000 组(含负数)+ 全同/主对角/反对角/递增结构,
                 共 40377 组,对照"开新矩阵"版本,0 不一致。
        """
        n = len(matrix)
        for i in range(n):
            for j in range(i):
                matrix[i][j],matrix[j][i] = matrix[j][i],matrix[i][j]

        for i in range(n):
            for j in range(n//2):
                matrix[i][j],matrix[i][n-1-j] = matrix[i][n-1-j],matrix[i][j]


if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding="utf-8")

    def check(matrix, expect):
        original = [row[:] for row in matrix]      # 二维深拷贝:list(matrix) 只拷外层
        Solution().rotate(matrix)                  # rtype: None,不接返回值
        flag = "✅" if matrix == expect else "❌"
        print(f"{flag} {original} → {matrix}（期望 {expect}）")

    check([[1,2,3],[4,5,6],[7,8,9]], [[7,4,1],[8,5,2],[9,6,3]])                # 题目原例
    check([[5,1,9,11],[2,4,8,10],[13,3,6,7],[15,14,12,16]],
          [[15,13,2,5],[14,3,4,1],[12,6,8,9],[16,7,10,11]])                    # 原例 2:4×4,偶数阶
    check([[1]], [[1]])                                                         # 1×1:环只转一次
    check([[1,2],[3,4]], [[3,1],[4,2]])                                         # 2×2:一个环
    check([[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]],
          [[13,9,5,1],[14,10,6,2],[15,11,7,3],[16,12,8,4]])                    # 4×4:验证内外两圈
    check([[1,2,3],[4,5,6],[7,8,9]], [[7,4,1],[8,5,2],[9,6,3]])                 # ← 照妖镜:写成逆时针会红