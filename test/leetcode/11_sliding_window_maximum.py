import collections
class Solution(object):
    def maxSlidingWindow(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: List[int]
        题号:LeetCode Hot 100 第 11 题(LeetCode 原题号 239,分类:子串)
        链接:https://leetcode.cn/problems/sliding-window-maximum/
        难度:困难
        题意:给定数组 nums 和窗口大小 k,窗口从最左端开始每次右移一格,
             返回每个窗口内的最大值。结果长度 = len(nums) - k + 1。
             约束:1 <= len(nums) <= 10^5,1 <= k <= len(nums)。

        为什么暴力不行:
            (n-k+1) 个窗口,每个窗口扫 k 个取 max → O(n*k)。
            取 k ≈ n/2 = 5*10^4 → 约 2.5*10^9 次操作,Python 一秒量级 10^7,
            必然超时。且相邻窗口有 k-1 个元素重合,却被重复 max 了一遍 ——
            这正是"滑窗省的是重复计算"的用武之地。

        思路(单调队列,deque 存下标):
            核心判据:若 A 在 B 左边且 nums[A] <= nums[B],则 A 永远没机会 ——
            B 比它大,又比它晚过期(A 离开窗口时 B 还在)。
            → 每进一个数,把队尾所有 <= 它的都弹掉。
            队列里存"下标"不存"值",因为过期要比较位置。

            1. 队头过期:deque[0] < i-k+1 就 popleft
            2. 队尾挤压:while deque 非空且 nums[deque[-1]] <= nums[i],pop
            3. 追加 i
            4. i >= k-1 时,答案 = nums[deque[0]](队头永远最大)
            注意:队列从左到右是"从大到小",左端 = 最大且最老,右端 = 最小且最新。

        复杂度:
            时间 O(n) —— 每个下标最多进队一次、出队一次,while 总摊还 O(n)
            空间 O(k) —— 队列内最多存 k 个下标
            对照暴力 O(n*k):省掉的是"每个窗口重扫 k 个"的重复计算,
            换成了"每个元素一生只进出队列各一次"。

        易错点:
            1. 过期判断不能"找窗口左边那个值删掉" —— 它可能早被挤压走了。
               只能判断队头下标 deque[0] < i-k+1。队列存下标才做得到。
            2. 挤压用 <= 而不是 < —— 相等时也该弹掉旧的:
               保留旧的下标只会更早过期,新的存活更久,留新的严格更优。
               用例 [1,1,1], k=2 抓这里。
            3. 三步顺序:先过期、再挤压、最后追加。顺序反了会多弹或漏弹。
            4. 答案只能在 i >= k-1 之后才开始收集,len(res) 必须等于 n-k+1。

        自测用例:见 __main__,8 条。
        """
        if not nums or k == 0:
            return []

        deque = collections.deque()
        res = []

        for i in range(len(nums)):
            if deque and deque[0] < i - k + 1:
                deque.popleft()
            while deque and nums[deque[-1]] <= nums[i]:
                deque.pop()

            deque.append(i)

            if i >= k-1:
                res.append(nums[deque[0]])

        return res

if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding="utf-8")

    def check(nums, k, expect):
        got = Solution().maxSlidingWindow(nums, k)
        flag = "✅" if got == expect else "❌"
        print(f"{flag} {nums} k={k} → {got}（期望 {expect}）")

    check([1,3,-1,-3,5,3,6,7], 3, [3,3,5,5,6,7])  # 题目原例
    check([1], 1, [1])  # 最小规模
    check([1,-1], 1, [1,-1])  # k=1:结果等于原数组
    check([1,3,1,2,0,5], 3, [3,3,2,5])  # 窗口边界
    check([9,8,7,6], 3, [9,8])  # ← 照妖镜:单调递减,只走过期
    check([1,2,3,4], 3, [3,4])  # ← 照妖镜:单调递增,只走挤压
    check([1,1,1], 2, [1,1])  # ← 照妖镜:<= 还是 < 在这分胜负
    check([7,2,4], 2, [7,4])  # 队头 7 出去后 4 才上位