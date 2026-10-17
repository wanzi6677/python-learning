import sys


class Solution(object):
    def subarraySum(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: int
        题号:LeetCode Hot 100 第 10 题(前缀和 + 哈希)
        链接:https://leetcode.cn/problems/subarray-sum-equals-k/
        难度:中等
        题意:统计和恰好等于 k 的连续子数组个数。
             注意"子数组"= 连续;"子序列"才可以不连续 —— 这题要连续。

        为什么不能用滑动窗口:
            nums 里有负数(-1000 <= nums[i] <= 1000),窗口的"和"不单调 ——
            右扩一格和可能变小,左缩一次和可能变大。
            左指针没有安全位置可去,往右缩就可能漏解
            (反例:[1,-1,0], k=0 用滑窗会漏掉 [1,-1])。

        思路(前缀和 + 哈希):
            1. prefix[t] = nums[0] + ... + nums[t-1],prefix[0] = 0
            2. 区间和 nums[i..j] = prefix[j+1] - prefix[i]
            3. 求和 == k → prefix[i] == prefix[j+1] - k
            4. 边走边记:走到当前位置 curr_sum 时,
               查字典里"curr_sum - k 出现过几次",就累加几次;
               再把 curr_sum 记进字典(次数 +1)。
            5. 字典初始 {(0, 1)} —— 空前缀。
               没有它,[1], k=1 这种"从下标 0 开始"的答案就数不到。

        复杂度:
            时间 O(n) —— 每个元素查一次、记一次,字典 O(1)
            空间 O(n) —— 字典最坏存 n+1 个不同前缀和
            对照暴力 O(n^2):省掉的内层循环就是"找哪个 i 使得 prefix[i]==curr_sum-k",
            这个动作交给哈希表 O(1) 完成。

        易错点:
            1. 字典初始必须 {0: 1},不能是 {} (漏掉从下标 0 开始的区间)
            2. 必须"先查后记":若先记 curr_sum 再查,当 k == 0 时会把自己算进去
            3. 字典的值存"次数"不是 True/False —— [0,0,0,0], k=0 答案 10,
               只存存在性会数成 1
            4. 区间和公式是 prefix[右+1] - prefix[左],漏了 +1 则单元素区间全丢

        自测用例:见 __main__,5 条;另做过 3000 组随机对拍(暴力 O(n^2) 对照)全一致。
        """

        prefix_count = {0:1}
        curr_sum = 0
        ans = 0
        for num in nums:
            curr_sum += num
            target = curr_sum - k

            ans += prefix_count.get(target, 0)

            prefix_count[curr_sum] = prefix_count.get(curr_sum, 0) + 1

        return ans

if __name__ == '__main__':
    sys.stdout.reconfigure(encoding="utf-8")

    def check(nums, k, expect):
        got = Solution().subarraySum(nums, k)
        flag = "✅" if got == expect else "❌"
        print(f"{flag} nums={nums} k={k} → {got}（期望 {expect}）")

    check([1, 1, 1], 2, 2)
    check([1, 2, 3], 3, 2)
    check([1, -1, 0], 0, 3)
    check([1], 0, 0)
    check([0, 0, 0, 0], 0, 10)
