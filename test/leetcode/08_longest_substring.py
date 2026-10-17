# -*- coding: utf-8 -*-
import sys

class Solution(object):
    def lengthOfLongestSubstring(self, s):
        """
        :type s: str
        :rtype: int
        题号:LeetCode Hot 100 第 8 题(滑动窗口类第一道)
        链接:https://leetcode.cn/problems/longest-substring-without-repeating-characters/
        难度:中等
        题意:给一个字符串 s,找出不含重复字符的【最长连续子串】的长度。
             子串必须连续("pwwkew" 的答案是 "wke",不是 "pwke");s 可以是空串。

        我的思路(滑动窗口):
            暴力解是"固定起点 i,扫终点 j,每换一个起点就把子串从头重判一遍有没有重复"。
            滑动窗口只改一件事:不再重判,左右两端都往右走,只做局部调整。

            1. 窗口 = s[left..right],含义是"以 right 结尾、最长的那段无重复子串"。
            2. 右指针每次把 s[right] 加进窗口;用字典 loc 记"字符 -> 它上一次出现的下标"。
            3. 若 s[right] 出现过,说明窗口里有重复:
               左指针直接跳到"上一次出现位置 + 1"。
               —— 不能只挪一格("abba" 证明移一格后 "bba" 里 b 仍然重复)。
            4. 但 left 只能往右、绝不能回头:
               用 left = max(left, loc[s[right]] + 1) 保证不回退。
               ("abba" 走到最后的 a 时,上一次位置 0,而 left 已经是 2;
                若直接赋成 0+1=1,窗口会退回 "bba",重新变非法。)
            5. 先算长度 right - left + 1 去更新答案,再写 loc[s[right]] = right。

        复杂度:
            时间 O(n) —— right 走一遍 n 步;left 只增不减,最多也走 n 步,
                        每个字符最多进窗口一次、出窗口一次,不会反复重扫。
            空间 O(字符集大小) —— loc 里最多存"不同字符的个数"(
                        全 ASCII 时是 O(1),一般写成 O(min(n, 字符集大小)))。
            对照:暴力解 O(n^2) 时间 / O(字符集) 空间,滑动窗口用"不重扫"换来 O(n)。

        易错点(都是这题自己踩出来的):
            1. left 不能回头 —— 必须写 max(left, 上一次位置 + 1),而不是直接赋值。
               抓它的用例:"abba"(期望 2,不回退的正确;回退后会算错)。
            2. 遇到重复时 left 不能只挪一格 —— "bbbbb"、"abba" 会露馅。
            3. 更新顺序:先更新 max_length,再 loc[s[right]] = right。
               (长度是用 right - left + 1 算的,不依赖字典;
                但如果改成"先记 loc 再算长度",s[right] 会把自己当成重复。)
            4. 空串 "" 返回 0;" " 这种空格也是字符,返回 1 —— 别只想着字母。
            5. 这里 n == 0 的提前 return 其实不是必需的:
               空串时 for 不执行,直接返回 max_length = 0 同样正确。
               但留着更直观,所以保留。

        自测用例:见 __main__,7 条(含 abba 抓回退、tmmzuxt 抓 stale 下标)。
        """
        n = len(s)
        loc = {}
        if n == 0:
            return 0
        max_length = 0
        left = 0
        for right in range(n):

            if s[right] in loc:
                left = max(left, loc[s[right]] + 1)

            max_length = max(max_length, right - left + 1)
            loc[s[right]] = right



        return max_length




if __name__ == '__main__':
    sys.stdout.reconfigure(encoding="utf-8")

    def check(s, expect):
        max_length = Solution().lengthOfLongestSubstring(s)
        flag = "✅" if max_length == expect else "❌"
        print(f"{flag} {s} → {max_length}（期望 {expect}）")

    check("abcabcbb", 3)
    check("bbbbb", 1)
    check("pwwkew", 3)
    check("dvdf", 3)
    check(" ",1 )
    check("abba",2 )
    check("tmmzuxt",5 )
