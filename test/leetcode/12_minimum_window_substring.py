class Solution(object):
    def minWindow(self, s, t):
        """
        :type s: str
        :type t: str
        :rtype: str
        题号:LeetCode Hot 100 第 12 题(LeetCode 原题号 76,分类:子串)
        链接:https://leetcode.cn/problems/minimum-window-substring/
        难度:困难
        题意:在 s 里找最短的连续子串,使 t 中每个字符(含重复次数)都在其中出现。
             找不到返回 ""。答案唯一。
             约束:1 <= m, n <= 10^5,大小写英文字母。
             本题要求 O(m+n)(follow up)。

        和第 9 题的区别:
            第 9 题窗口长度固定(= len(p)),left 跟着 right 同步走;
            这题窗口长度可变,left 独立走,内层 while 控制"收缩到不覆盖为止"。

        思路(可变滑动窗口 + 哈希计数):
            1. need = Counter(t) 记每个字符要几个;window 记窗口里现有几个。
            2. 只维护一个数 formed = 已凑够数量的字符种数;
               formed == len(need) 即窗口覆盖 t,不必每次比整张字典。
            3. right 扩张进窗口;凑够 formed 后进入 while,left 收缩。
            4. 内层 while:先记录答案(此刻一定覆盖),再把 s[left] 移出。
               循环退出时窗口一定已不覆盖 —— 所以记录必须在收缩之前。

        复杂度:
            时间 O(m+n) —— right 走 m 步;left 总共也只走 m 步(每字符最多进一次窗口、出一次)
            空间 O(k) —— k 为 t 中不同字符数,至多 52
            对照暴力 O(n^2 * k):省掉的是"每个窗口重新数一遍字符",
            换成"每进出一个字符改两个计数 + 一个 formed"。

        易错点:
            1. 必须用 Counter(t),不能用 set(t) —— t = "aa" 要 2 个 a,
               set 只留 1 种,会把 "a" 判成合格(用例 "aa"/"aa" 抓)
            2. formed 判断用 ==,不能用 >= —— 超量的字符会重复计数,
               使 formed 虚增到 required(例:窗口 "aa" 会被误判成覆盖了 "ab")
            3. 内层用 while,不能用 if —— 缩一格可能仍覆盖,要缩到不覆盖为止
            4. 记录答案必须在收缩之前 —— while 退出时窗口已不覆盖(用例 cabwefgewcwaefgcf 抓)
            5. 答案记 (起点, 长度),不记子串本身 —— 每步切片会退化

        自测用例:见 __main__,9 条;另做过 500 组随机对拍(暴力 O(n^2) 对照)长度全一致。
        """
        from collections import Counter

        need = Counter(t)

        window = {}  #窗口里每个字符有几个
        formed = 0   #已经凑够数量的字符种数
        required = len(need) #需要凑够的字符种数

        left = 0
        best = (0, float('inf'))  # 答案记 (起点, 长度), 无穷大表示还没找到

        for right in range(len(s)):
            c = s[right]

            # 1. 把 s[right] 加进 window
            if c in need:
                window[c] = window.get(c, 0) + 1
                # 若 window[c] == need[c] → formed += 1 (== 不是 >=)
                if window[c] == need[c]:
                    formed += 1

            # 2. while formed == required: 窗口覆盖 t
            while formed == required:
                # 先记录（更新 best，若更短）
                if right - left + 1 < best[1]:
                    best = (left, right - left + 1)

                # 再破坏（把 s[left] 移出 window）
                d = s[left]
                if d in need:
                    # 移出前判
                    if window[d] == need[d]:
                        formed -= 1
                    window[d] -= 1

                left += 1  # 窗口左边界右移

        # 最后截取返回
        # 如果 best[1] 还是无穷大，说明没找到，返回 ""
        return "" if best[1] == float('inf') else s[best[0]: best[0] + best[1]]

if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding="utf-8")

    def check(s, t, expect):
        got = Solution().minWindow(s, t)
        flag = "✅" if got == expect else "❌"
        print(f"{flag} s={s!r} t={t!r} → {got!r}（期望 {expect!r}）")

    check("ADOBECODEBANC", "ABC", "BANC")  # 题目原例
    check("a", "a", "a")  # 最小规模
    check("a", "aa", "")  # s 不够,不存在
    check("aa", "aa", "aa")  # ← 照妖镜:重复字符,用 set 会错判成 "a"
    check("ab", "b", "b")  # 只需 1 种字符
    check("abc", "cba", "abc")  # 顺序无关,整个 s 是答案
    check("bba", "ab", "ba")  # ← 照妖镜:更短的窗口在后面
    check("cabwefgewcwaefgcf", "cae", "cwae")  # ← 照妖镜:收缩过头或不足都会错
    check("ADOBECODEBANC", "XYZ", "")  # t 里的字符 s 没有
