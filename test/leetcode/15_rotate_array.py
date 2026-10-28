class Solution(object):
    def rotate(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: None Do not return anything, modify nums in-place instead.
        题号:LeetCode Hot 100 第 15 题(轮转数组 / 原题号 189)
        链接:https://leetcode.cn/problems/rotate-array/
        难度:中等
        题意:把 nums 向右轮转 k 个位置。原地修改,不返回任何东西。
        思路(反转三步,O(1) 空间):
            1. 轮转不改变元素的相对顺序,只是把数组切成"前 k 个"和"后 n-k 个"两截,再对调位置。
            2. 先反转整段 → 两截位置换对了,但每截内部顺序是反的。
            3. 再反转前 k 个、反转后 n-k 个 → 各自顺序恢复。
            4. 三个原地交换,只用两个下标变量,不需要额外数组。
        复杂度:
            时间 O(n) —— 三次反转合起来每个元素恰被访问 2 次(2n),仍是 O(n)。
            空间 O(1) —— 只在 nums 上交换,额外只用 left/right 两个下标变量。
        易错点:
            1. nums = nums[-k:] + nums[:-k] 只重新绑定了局部变量,调用方传入的原列表不受影响,
               必须写 nums[:] = ... 才是原地修改。本题 rtype 是 None,调用方只看 nums 本身。
            2. 切片越界会静默截断、不报错:k>n 时 nums[-k:] 会取成整个数组,nums[:-k] 取成空,
               结果是"看起来跑通了其实全错"。所以必须先 k %= len(nums)。
            3. 切片法(nums[:] = nums[-k:] + nums[:-k])虽然能过,但会新建一个长度 n 的列表,
               空间是 O(n),不满足进阶要求的 O(1)。
            4. while 用 < 不用 <= :left == right 时是同一个元素,再交换一次没有意义。
        自测用例:见 __main__,6 条;含 k>n、k=0、单元素三个照妖镜。
        """
        k %= len(nums)
        def reverse(left, right):
            while left < right:
                nums[left], nums[right] = nums[right], nums[left]
                left += 1
                right -= 1

        reverse(0, len(nums) - 1)
        reverse(0, k-1)
        reverse(k, len(nums) - 1)





if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding="utf-8")      # PowerShell 是 GBK,不设会 UnicodeEncodeError

    def check(nums, k, expect):
        original = list(nums)              # ← 本题是原地修改(rtype: None)，必须先留证据
        Solution().rotate(nums, k)         # ← 不接返回值，结果在 nums 里
        flag = "✅" if nums == expect else "❌"
        print(f"{flag} {original} k={k} → {nums}（期望 {expect}）")

    check([1,2,3,4,5,6,7], 3, [5,6,7,1,2,3,4])   # 题目原例
    check([-1,-100,3,99], 2, [3,99,-1,-100])      # 题目原例（负数）
    check([1,2], 3, [2,1])                        # ← 照妖镜:k > n,没做 k % n 会搬错
    check([1], 0, [1])                            # ← 照妖镜:k = 0,单元素
    check([1,2,3,4,5,6], 2, [5,6,1,2,3,4])        # n=6,k=2
    check([1,2,3,4,5,6], 4, [3,4,5,6,1,2])        # n=6,k=4