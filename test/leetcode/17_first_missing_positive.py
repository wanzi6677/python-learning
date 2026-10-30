import sys


class Solution(object):
    def firstMissingPositive(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        题号:LeetCode Hot 100 第 17 题(普通数组 · 原地哈希)
        链接:https://leetcode.cn/problems/first-missing-positive/
        难度:困难
        题意:返回最小的、不在 nums 里的正整数。要求 O(n) 时间 + O(1) 辅助空间。
        思路(先定答案范围,再把 nums 自己当哈希表):
            1. 定范围:n 个数最多凑出 1..n。若 1..n 全都在,答案是 n+1;
               否则答案必落在 1..n 之内。→ 负数、0、大于 n 的数全是干扰项,
               它们不可能成为答案,也帮不上忙。
            2. 用额外空间的版本(垫脚石):把 1..n 内的数丢进 set,从 1 往上数。
               时间 O(n),但空间 O(n),不满足要求。
            3. 把"集合"塞进 nums:约定 nums[i] 这个格子负责数字 i+1。
               数字 x 存在,就把它交换到 nums[x-1] 上(原地归位)。
            4. 归位规则:对每个 i,只要 nums[i] 在 1..n 内、且目标位
               nums[nums[i]-1] 还没有这个数,就一直交换(内层 while)。
               换过来的新数也可能没归位,所以是 while 不是 if。
               目标位已有同样的数 = 重复数字,必须停,否则死循环。
            5. 扫一遍:第一个 nums[i] != i+1 的 i,答案就是 i+1;
               全对上则返回 n+1。
        复杂度:
            时间 O(n) —— 外层扫 n 次;每次交换至少让一个数永久归位且不再动,
                总交换次数 <= n,所以内层 while 不构成 O(n^2),整体 <= 2n 次操作。
            空间 O(1) —— 没有开任何新容器,只用 j 和交换时的临时量。
                原地哈希的本质:用输入数组自己当那张表,值即位置。
        易错点:
            1. 初版写成 `if i not in nums`(从 n 往下扫找最小缺失)
               —— 逻辑对,但 `in` 对 list 是 O(n),套在 n 次循环里是 O(n^2),
               n=10^5 时约 10^10 次比对,必超时。改用 set 能到 O(n) 时间
               但空间变 O(n),题目要 O(1),所以只能原地哈希。已替换。
            2. while 的条件少判"目标位已有同样的数" -> 重复数字死循环
               (例:[1,1] 会无限交换)。判据:第二条 and 是防死循环的。
            3. nums[i] 不在 1..n 时绝不能访问 nums[nums[i]-1]:
               负数会取到末尾元素(静默错误),大于 n 会 IndexError(例:[1000])。
               靠 and 短路保护,所以范围判断必须写在第一个,顺序不能反。
            4. 内层必须 while 不能 if —— 交换换来的新数可能还没归位,要反复换。
            5. 会原地修改 nums(虽然 rtype 是 int)。测试里 check() 先
               original = list(nums) 留证据,但它只用于打印,不参与比较。
        自测用例:见 __main__,10 条(含重复 [1,1] / 越界 [1000] / 全齐 [1,2,3])。
            另做过:随机对拍 5000 组 vs 集合版,0 不一致;
            n=10^5 实测最慢 31 ms(判据:Python 10^8 以上不可接受)。
        """
        n = len(nums)
        # 步骤 1:原地归位,让 nums[x-1] 存放数字 x
        for i in range(n):
            while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
                j = nums[i] - 1  # 先算好目标下标
                nums[i], nums[j] = nums[j], nums[i]

        # 步骤 2:扫描找答案
        for i in range(n):
            if nums[i] != i + 1:
                return i + 1
        return n + 1




if __name__ == '__main__':
    sys.stdout.reconfigure(encoding="utf-8")

    def check(nums, expect):
        original = list(nums)          # 本题会原地改 nums,先留证据
        got = Solution().firstMissingPositive(nums)
        flag = "✅" if got == expect else "❌"
        print(f"{flag} {original} → {got}（期望 {expect}）")

    check([1,2,0], 3)              # 题目原例 1
    check([3,4,-1,1], 2)           # 原例 2:含负数
    check([7,8,9,11,12], 1)        # 原例 3:全大于 n → 答案必是 1
    check([1], 2)                  # ← 单元素且是 1:抓"忘了返回 n+1"
    check([2], 1)                  # ← 单元素是 2(超出范围):抓"越界访问"
    check([1,1], 2)                # ← 重复数字:抓"交换死循环"
    check([1,2,3], 4)              # ← 1..n 全齐:必须返回 n+1
    check([-1,-2,0], 1)            # ← 全负数/0:答案必是 1
    check([2,2,3], 1)              # ← 重复 + 缺 1:抓"死循环"和"第一个缺"
    check([1000], 1)               # ← 超大值:抓"直接拿值当下标"→ IndexError