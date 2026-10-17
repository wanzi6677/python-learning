class Solution(object):
    def singleNumber(self, nums):
        """
        LeetCode Hot 100 第 136 题:只出现一次的数字 (Single Number)
        链接:https://leetcode.cn/problems/single-number/
        难度:简单
        分类:技巧(位运算)

        题意:
            非空整数数组,除某个元素只出现一次外,其余每个元素均出现两次。
            找出那个只出现一次的元素。

        核心直觉:
            成对出现的数字在异或时自己抵消(a ^ a = 0),
            只有那个落单的没得抵消 -> 它留下来了。

        为什么能"无视顺序"配成对(这题的关键,容易被忽略):
            异或满足【交换律和结合律】。
            [4,1,2,1,2] 里两个 1 中间隔着 2,本来抵不到一起,
            但靠交换律可以重排成 4 ^ (1^1) ^ (2^2) = 4 ^ 0 ^ 0 = 4。

        三条性质(缺一不可):
            a ^ a = 0     成对的自己抵消
            a ^ 0 = a     抵消后剩下的原样留下
            交换律/结合律  允许重新排列,把相同的配到一起

        我的思路(两版对照):
            ① 异或版   :一遍循环,时间 O(n),空间 O(1)  <- 满足进阶要求
            ② dict计数 :时间 O(n),空间 O(n)           <- 能过但不满足进阶

        复杂度:
            时间 O(n)  —— 只扫一遍
            空间 O(1)  —— 只用了一个 result 变量

        易错点:
            1. 初值必须是 0。因为 a ^ 0 = a,0 是异或的单位元;
               换成别的初值第一轮就会污染结果。
            2. 答案是 0 时([0,1,1] -> 0),0 是假值!
               不能用 if result: 判断,要写 if result is not None:
               (这和第 1 题 if seen.get(need) is not None 是同一个坑)
            3. 负数不影响:异或的性质对任何整数成立,不用特殊处理。
            4. 这题是"技巧"分类,考的是知不知道这一招,不是推出来的。
        """
        only = 0
        for num in nums:
            only ^= num
        return only

if __name__ == '__main__':
    def check(nums, expect):
        only = Solution().singleNumber(nums)
        flag = "✅" if only == expect else "❌"
        print(f"{flag} {nums} → {only}（期望 {expect}）")

    check([2,2,1], 1)
    check([4,1,2,1,2], 4)
    check([1], 1)
    check([-1,-1,-2], -2)
    check([5,0,5], 0)
