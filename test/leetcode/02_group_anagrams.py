# 题目：
#     给你一个字符串数组 strs，请你将 字母异位词 组合在一起。
#     可以按任意顺序返回结果列表。
#
#     字母异位词 是由重新排列源单词的所有字母得到的一个新单词。
#     （即：字母构成相同、只是顺序不同的词）
#
# 示例：
#     输入: strs = ["eat", "tea", "tan", "ate", "nat", "bat"]
#     输出: [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]
#     （输出顺序不限，组内顺序也不限）
#
#     输入: strs = [""]
#     输出: [[""]]
#
#     输入: strs = ["a"]
#     输出: [["a"]]
#
# 提示：
#     1 <= strs.length <= 10^4
#     0 <= strs[i].length <= 100
#     strs[i] 仅包含小写英文字母
#
# 我的思路：
#     1. 用「排序后的字母」当身份证号 → 异位词的身份证号必然相同
#     2. sorted() 返回 list，list 可变、不能当 dict 的 key → 转成 tuple
#     3. 用字典分组：key = 身份证号，value = 该组的所有词
#     4. 返回 dict.values()
#
# 复杂度：
#     时间 O(n * k log k)   n = 词数，k = 平均词长（每个词要排序）
#     空间 O(n * k)         所有词都要存进字典
#
# 易错点：
#     - sorted(word) 返回 list，必须先转 tuple 才能当 key
#     - 输出顺序不确定 → 写测试时要「先规范化再比较」，不能直接 ==

class Solution(object):
    def groupAnagrams(self, strs):
        """
        :type strs: List[str]
        :rtype: List[List[str]]
        """
        anagrams = {}
        for word in strs:
            key = tuple(sorted(word))
            if key in anagrams:
                anagrams[key].append(word)
            else:
                anagrams[key] = [word]

        return list(anagrams.values())


if __name__ == "__main__":
    def check(words, expect):
        got = Solution().groupAnagrams(words)
        # 组内、组间顺序都不定 → 排序后比较
        norm = sorted(sorted(g) for g in got)
        exp = sorted(sorted(g) for g in expect)
        print(f"{'✅' if norm == exp else '❌'} {words} → {got}")

    check(["eat","tea","tan","ate","nat","bat"],
          [["bat"],["nat","tan"],["ate","eat","tea"]])
    check([""], [[""]])                    # 空字符串
    check(["a"], [["a"]])                  # 单个词
    check(["", ""], [["", ""]])            # 两个空串要分到一组