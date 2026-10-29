class Solution(object):
    def productExceptSelf(self, nums):
        """
        :type nums: List[int]
        :rtype: List[int]
        题号:LeetCode Hot 100 第 16 题(普通数组 · 前缀积 + 后缀积)
        链接:https://leetcode.cn/problems/product-of-array-except-self/
        难度:中等
        题意:返回数组 answer,answer[i] 等于 nums 中除 nums[i] 之外其余各元素的乘积。
             要求 O(n) 时间且不使用除法。
        思路(两趟扫描,输出数组当容器):
            1. answer[i] = 左边所有数的积 × 右边所有数的积。
               "自己"从始至终不在乘积里 —— 不是"除掉了自己",是"从来没乘进来"。
               所以这题根本不需要除法,含 0 也不会崩。
            2. 第一趟从左往右:left 维护 nums[0..i-1] 的积,直接写进 answer[i],
               再把 nums[i] 并入 left。跑完 answer 就是左半列。
            3. 第二趟从右往左:right 维护 nums[i+1..] 的积,乘进 answer[i](用 *=,
               不是 =,否则覆盖掉左半),再把 nums[i] 并入 right。
        复杂度:
            时间 O(n) —— 两趟各走 n 次,共 2n 次乘法
            空间 O(1) —— 除输出数组外只用了 left / right 两个变量(题目不计输出)
        易错点:
            1. left / right 必须定义在 for 外面 —— 写在循环体内每轮重置,
               就退回"每个 i 都重算"的 O(n²),n=10^5 时约 10^10 次运算,必超时。
            2. 先记后乘 —— 每个循环里先写 answer[i],再更新 left/right。
               顺序反了会把 nums[i] 自己乘进去(判据:answer[0] 必须还是 1)。
            3. 第二趟用 answer[i] *= right,不能用 = —— 会覆盖第一趟填好的左半。
            4. 外层 range(n - 1, -1, -1) 的终点写 -1 —— range 不含终点,才跑得到下标 0。
            5. 用例全绿不等于复杂度对 —— 小数组上 O(n²) 也能全过,要代入 n=10^5 算。
        自测用例:见 __main__,6 条(含两条含 0 的用例)。
        """
        n = len(nums)
        answer = [1] * n

        left = 1
        for i in range(n):
            answer[i] = left
            left *= nums[i]

        right = 1
        for i in range(n - 1, -1, -1):
            answer[i] *= right
            right *= nums[i]

        return answer


if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding="utf-8")

    def check(nums, expect):
        got = Solution().productExceptSelf(nums)
        flag = "✅" if got == expect else "❌"
        print(f"{flag} {nums} → {got}（期望 {expect}）")

    check([1,2,3,4], [24,12,8,6])        # 题目原例
    check([-1,1,0,-3,3], [0,0,9,0,0])    # 原例:含 0,用除法必崩
    check([2,3], [3,2])                  # 最短长度 2
    check([0,0], [0,0])                  # ← 两个 0:抓"除以零"
    check([-1,-1], [-1,-1])              # 全负数,偶个数
    check([1,0], [0,1])                  # ← 抓"0 的位置":除自身后另一个是 0 还是 1