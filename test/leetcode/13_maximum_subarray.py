import sys


class Solution(object):
    def maxSubArray(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        题号:LeetCode Hot 100 第 13 题(普通数组 / 动态规划)
        链接:https://leetcode.cn/problems/maximum-subarray/
        难度:中等
        题意:找出和最大的非空连续子数组,返回这个和。
        思路(以 i 结尾的最优段):
            1. 不枚举所有段,改成问"以 nums[i] 结尾的子数组,最大和是多少",记作 f(i)
            2. f(i) 只有两个候选:接在 f(i-1) 后面(left + x),或者自己重开(x)
               —— 两者加的是同一个 x,所以前面那段越大,接上越划算
            3. 所以判据是 left <= 0 就重开,否则接上,即 left = max(x, left + x)
            4. best 记录所有出现过的 f(i) 的最大值,先更新 left 再更新 best
        复杂度:
            时间 O(n) —— 只扫一遍
            空间 O(1) —— 只用两个变量
        易错点:
            1. best 必须开成 nums[0] 而不是 0 —— 题目要求"非空子数组",全负数组的答案是 -1 之类,
               不是 0。开成 0 会让 [-3,-1,-2] 输出 0。
            2. left = 0 和 best = nums[0] 含义不同:left 是"还没开始",best 是"先假设第一段就是答案"。
               两者能立刻对上,是因为第一轮 left = max(nums[0], 0 + nums[0]) = nums[0]。
            3. 必须先更新 left、再更新 best —— 顺序反了比较的是 f(i-1),
               最后一个位置的 f 永远没机会被比到,只有 n == 1 的用例能暴露。
            4. 只考虑"接到最优那一段"是够的:两个候选加的是同一个 x,
               前一项越大后一项越大,不存在"接到次优段更优"的情况。
            5. 进阶要求是分治 O(n log n):左半边 / 右半边 / 跨中点三类讨论(本题未实现)。
        自测用例:见 __main__,7 条。
        """
        left = 0  # 以 nums[i-1] 结尾的最优段和;0 表示"还没开始",第一轮自然被 x 覆盖
        best = nums[0]  # 目前见过的最大答案 —— 初值必须是 nums[0],不能是 0

        for x in nums:
            left = max(x, left + x)
            best = max(best, left)
        return best


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding="utf-8")

    def check(nums, expect):
        got = Solution().maxSubArray(nums)
        flag = "✅" if got == expect else "❌"
        print(f"{flag} {nums} → {got}（期望 {expect}）")

    check([-2,1,-3,4,-1,2,1,-5,4], 6)   # 题目原例
    check([1], 1)                        # 原例:只有一个元素
    check([5,4,-1,7,8], 23)              # 原例:整段最优
    check([-3,-1,-2], -1)                # ← 照妖镜:全负,答案不是 0,必须真的选一个元素
    check([-2,1], 1)                     # ← 照妖镜:抓"初值开成 0"
    check([1,-1,1], 1)                   # 正负交替,别把两段正数拼起来
    check([8,-19,5,-4,20], 21)           # 中间那段负数要不要跨过去
