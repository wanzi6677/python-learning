import sys


class Solution(object):
    def merge(self, intervals):
        """
        :type intervals: List[List[int]]
        :rtype: List[List[int]]
        题号:LeetCode Hot 100 第 14 题(普通数组 / 排序 + 扫描)
        链接:https://leetcode.cn/problems/merge-intervals/
        难度:中等
        题意:合并所有重叠的区间,返回互不重叠且覆盖全部输入的结果。
        思路(先排序,再一次扫描):
            1. 先排序,让左端点单调不减 —— 不排序就判不出重叠([[4,7],[1,4]] 的反例)
            2. 已知 a[0] <= b[0] 时,两区间重叠的充要条件是 b[0] <= a[1]
               (端点相接也算重叠,所以是 <= 不是 <)
            3. 从左往右扫,手上维护"当前正在合并的区间":
               和它重叠 → 右端点取 max 后并入
               不重叠 → 它已经合并完,收进结果,手上换成当前区间
            4. 扫完别忘了把手上的最后一个也收进结果
        复杂度:
            时间 O(n log n) —— 排序主导,扫描是 O(n)
            空间 O(n) —— 结果数组(排序原地,不计入)
        易错点:
            1. 重叠判据用 <= 不用 < —— [[1,4],[4,5]] 这条专门抓它
            2. 合并时右端点要取 max,不能直接赋当前区间的右端点 ——
               [[1,4],[0,4]] 或 [[1,10],[2,3]] 会把区间缩回去
            3. 注意本函数原地修改了输入(用了 sort),题目不要求保护输入
            4. 排序后结果天然有序,测试可直接 == 比较,不需要 normalize
        自测用例:见 __main__,7 条。
        """
        intervals.sort(key=lambda x: x[0])
        merged = []
        for x in intervals:
            if not merged or merged[-1][1]<x[0]:
                merged.append(x)
            else:
                merged[-1][1] = max(merged[-1][1], x[1])

        return merged


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding="utf-8")

    def check(intervals, expect):
        got = Solution().merge(intervals)
        flag = "✅" if got == expect else "❌"
        print(f"{flag} {intervals} → {got}（期望 {expect}）")

    check([[1,3],[2,6],[8,10],[15,18]], [[1,6],[8,10],[15,18]])  # 题目原例
    check([[1,4],[4,5]], [[1,5]])                                # ← 照妖镜:端点相接算重叠(用 < 就红)
    check([[4,7],[1,4]], [[1,7]])                                # 原例:输入无序
    check([[1,4],[0,4]], [[0,4]])                                # ← 照妖镜:后面的右端点比前面小,合并时别把右端点缩回去
    check([[1,4],[2,3]], [[1,4]])                                # ← 内含:小区间被大区间包住
    check([[1,10]], [[1,10]])                                    # 单个区间
    check([[1,2],[3,4]], [[1,2],[3,4]])                           # 完全不重叠,一个都不许合并