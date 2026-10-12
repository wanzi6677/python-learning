# 题目：最长连续序列 Longest Consecutive Sequence
# 链接：https://leetcode.cn/problems/longest-consecutive-sequence/
# 难度：中等 · 分类：哈希
#
# 题意：
#     给一个「未排序」的整数数组 nums，找出其中「数字连续」的最长序列的长度。
#     - 「连续」指数值连续（1,2,3,4），不要求它们在原数组里挨着
#     - 要求时间复杂度 O(n)
#
# 示例：
#     输入: nums = [100,4,200,1,3,2]
#     输出: 4        （最长连续序列是 1,2,3,4）
#
#     输入: nums = [0,3,7,2,5,8,4,6,0,1]
#     输出: 9        （0,1,2,3,4,5,6,7,8；注意有重复的 0）
#
# 我的思路：
#     1. 先把 nums 丢进 set
#        —— 去重是顺带的，真正要的是 set 的「O(1) 查找」：
#           问「某个数在不在」一次就出答案，这是整题的关键能力
#     2. 不排序也能找到「下一个数」：下一个数就是 num + 1，直接算出来，
#        不需要像排序那样靠「挨在一起」才知道谁跟谁连续
#        （排序解 O(n log n)：set 去重 → sorted → 扫一遍比较相邻差是否为 1）
#     3. 关键优化：每个数字只当一次「起点」
#        - 如果 x-1 也在 set 里 → x 不是这一串的头 → continue 跳过
#        - 如果 x-1 不在 set 里 → x 是一串的头 → 从它往上数 x+1, x+2 ...
#
# 复杂度：
#     时间 O(n)     —— 看着有 while，但每个数字只会被 while 数到一次：
#                      只有「序列的头」会进 while，其余都被 continue 跳过了，
#                      所以 for 和 while 加起来总共 O(n)
#     空间 O(n)     ——set空间复杂度
#
# 易错点：
#     - longest_streak 的更新位置：必须在「一串数完」之后，不能写在 while 里面
#       （我一开始就写错了，缩进差一格 —— 那样「孤立的数」永远更新不到）
#     - 初始值用 0 而不是 1：
#         · 0 的意思是「我还没数过任何一串，目前最长是 0」——这是真话
#         · 1 的意思是「我已经见过长度 1 的一串了」——循环还没开始，这是假话
#         · 用 1 会「蒙对」某些输入，从而掩盖逻辑错误；用 0 不掩盖，写错立刻红
#     - continue 和 pass 不是一回事：
#         · continue = 跳过本轮剩下的代码，直接进入下一个 x
#         · pass     = 什么都不做，继续往下执行
#         如果把 continue 换成 pass，就会拿上一轮遗留的 current_streak 去 max
#     - 遍历的是 set 不是 nums：set 无序 → 但这题只求「长度」不求「是哪一串」，
#       所以无序不影响结果（对比第 2 题要求输出分组，就要先规范化再比较）


class Solution(object):
    def longestConsecutive(self, nums):

        #     1. 排序求解
        #        先排序。
        #        去掉重复数字，或者遇到重复时跳过。
        #        遍历排序后的数组。
        #        如果当前数字 = 上一个数字 + 1，说明连续，当前长度 + 1。
        #        否则连续断了，当前长度重置为1。
        #        每次更新最大值。
        # num_set = set(nums)
        # sorted_num_set = sorted(num_set)
        # longest_streak = 0
        # for i in range(len(sorted_num_set)):
        #     if i == 0 or sorted_num_set[i] != sorted_num_set[i-1] + 1:
        #         current_streak = 1
        #     else:
        #         current_streak += 1
        #     longest_streak = max(longest_streak, current_streak)

        # 02.哈希表
        # 把所有数字放进一个set，顺便去重。
        # 遍历这个set。
        # 对当前数字x，先判断x - 1是否在set里。
        # 如果x - 1在，说明x不是起点，直接跳过。
        # 如果x - 1不在，说明x是一个连续序列的起点。
        # 从x开始，不断检查x + 1、x + 2……是否在set里。
        # 统计这轮长度，更新最大值。
        if not nums:
            return 0
        set_nums = set(nums)
        longest_streak = 0
        for x in set_nums:
            if x-1 in set_nums:
                continue
            else:
                current_streak = 1
                while x+1 in set_nums:
                    current_streak+=1
                    x+=1
                longest_streak = max(longest_streak, current_streak)

        return longest_streak  # 记得返回结果


if __name__ == '__main__':
    def check(nums, expect):
        got = Solution().longestConsecutive(nums)
        print(f"{'✅' if got == expect else '❌'} {nums} → {got}（期望 {expect}）")

    check([100, 4, 200, 1, 3, 2], 4)
    check([], 0)
    check([10, 5], 1)          # ← 抓 bug 的用例
    check([0,3,7,2,5,8,4,6,0,1], 9)
    check([1, 2, 0, 1], 3)