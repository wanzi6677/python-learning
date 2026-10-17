class Solution(object):
    def findAnagrams(self, s, p):
        """
        :type s: str
        :type p: str
        :rtype: List[int]
        题号:LeetCode Hot 100 第 9 题(滑动窗口 + 哈希)
        链接:https://leetcode.cn/problems/find-all-anagrams-in-a-string/
        难度:中等
        题意:给定 s 和 p,找出 s 中所有是 p 的字母异位词的子串,返回它们的起始下标。
             例:s = "cbaebabacd", p = "abc" → [0, 6]

        【第一版:排序滑窗(对照用,LeetCode 提交的是第二版)】

        思路:
            1. 窗口长度固定 = len(p),因为异位词要求字母个数完全一致。
            2. 枚举每个起点 left,把窗口 s[left:left+k] 排序,和排序后的 p 比较。
            3. 相等就记录 left。

            这是"暴力枚举 + 每个窗口重新算一遍",和第 2 题(字母异位词分组)
            的 tuple(sorted(word)) 是同一个身份证思路。

        复杂度:
            时间 O(n · k log k) —— n 个窗口,每个窗口排序 O(k log k)
            空间 O(k) —— 每个窗口的排序结果

        为什么它不是最终版:
            窗口 [0,k-1] 和 [1,k] 只差 2 个字符,其余 k-2 个一模一样,
            但这里每次都把整串重新排序了一遍 —— 重复劳动。
        """
        tuple_p = tuple(sorted(p))
        n = len(p)
        list_s = []
        for left in range(len(s) - n + 1):
            if tuple(sorted(s[left:left+n])) == tuple_p:
                list_s.append(left)

        return list_s

    def findAnagrams2(self, s, p):
        """
        :type s: str
        :type p: str
        :rtype: List[int]
        【第二版:计数滑窗(最终版,LeetCode 提交逻辑与此相同)】

        思路:
            1. 判断依据从"排序后的元组"换成"字符计数表"(Counter)。
               Counter('abc') == Counter('cba') 为 True,与顺序无关。
            2. 先算第一个窗口 s[:k] 的计数,单独判一次。
            3. 窗口整体右移:左边出去的字符计数 -1,右边进来的字符 +1。
               —— 窗口滑一格只有 2 个字母的计数变了,不用重算整窗。
            4. 每次滑动后比较两个 Counter,相等就记录新起点 left + 1。

        复杂度:
            时间 O(n · 26) = O(n) —— 每次比较整张表是 O(26),26 是常数
            空间 O(k) —— 两个 Counter

        易错点(这题自己踩出来的):
            1. range(len(s) - k) 比第一版少 1 —— 第一个窗口在循环外单独判过了,
               漏了这格会漏掉 s 末尾正好是异位词的情况。
               抓它的用例:"baa" / "aa" → [1]
            2. 滑动时"进一个、出一个"必须同时做,窗口长度恒为 k。
            3. Counter 的 == 会忽略计数为 0 的键,所以窗口里某字母减到 0
               不会误判。
            4. 新窗口起点是 left + 1,不是 left。

        已知更优解(今天没有写,原因记录在此):
            用 diff[26] + not_zero 计数,把每次"比较整张计数表 O(26)"降到 O(1)。
            大 O 上第二版已经是 O(n),第三版赢的只是常数因子。
            → 判断:不值得为常数因子增加代码复杂度。
        """
        k = len(p)
        if len(s) < k:
            return []

        from collections import Counter
        count_p = Counter(p)
        count_w = Counter(s[:k])#第一个窗口的计数，window
        res = []

        if count_w == count_p:
            res.append(0)

        for left in range(len(s)-k):
            count_w[s[left]] -= 1
            count_w[s[left+k]] += 1
            if count_w == count_p:
                res.append(left+1)

        return res

if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding="utf-8")

    def check(s, p, expect):
        got = Solution().findAnagrams2(s, p)
        flag = "✅" if got == expect else "❌"
        print(f"{flag} s={s!r} p={p!r} → {got}（期望 {expect}）")

    check("cbaebabacd", "abc", [0, 6])
    check("abab", "ab", [0, 1, 2])
    check("aa", "aa", [0])
    check("a", "ab", [])
    check("abcabbcabacba", "abca", [0,6,7,9])
    check("cbaebabacd", "abc", [0,6])