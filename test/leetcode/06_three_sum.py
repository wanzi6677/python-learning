class Solution(object):
    def threeSum(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]

        找出所有和为 0 且不重复的三元组。

        核心：排序 + 固定一个数 + 对撞双指针。

        步骤：
            1. nums.sort()，让数组有序，才能用双指针。
            2. 枚举 i 作为三元组中最小的数，在 nums[i+1:] 中找两数之和为 -nums[i]。
            3. 双指针 left = i + 1，right = len(nums) - 1：
               - 和 > 0：right -= 1
               - 和 < 0：left += 1
               - 和 == 0：记录答案，并跳过重复的 left / right(这一点很重要,最后一个测试用例是这个问题）

        去重：
            - 外层：nums[i] == nums[i-1] 时跳过。
            - 内层：命中一组后，left 跳过重复值，right 跳过重复值。

        剪枝：
            - nums[i] > 0 时直接 break，因为后面不可能再凑成 0。

        复杂度：
            时间 O(n²)，空间 O(1)（不含结果数组）。


        """

        nums.sort()
        result = []
        for i in range(len(nums)):
            if i>0 and nums[i] == nums[i-1]:
                continue
            if nums[i] > 0:
                break

            left = i+1
            right = len(nums)-1
            while left < right:
                total = nums[i] + nums[left] + nums[right]
                if total > 0:
                    right -= 1
                elif total < 0:
                    left += 1
                else:
                    result.append([nums[i], nums[left], nums[right]])
                    left += 1
                    while left < right and nums[left] == nums[left - 1]:
                        left += 1
                    right -= 1
                    while left < right and nums[right] == nums[right+1]:
                        right -= 1

        return result

if __name__ == '__main__':
    def normalize(triples):
        """把结果规范成可比的标准形状:组内排序 + 组间排序。"""
        return sorted([sorted(t) for t in triples])

    def check(nums, expect):
        got = Solution().threeSum(nums)
        flag = "✅" if normalize(got) == normalize(expect) else "❌"
        print(f"{flag} {nums} → {got}（期望 {expect}）")

    check([-1, 0, 1, 2, -1, -4], [[-1, -1, 2], [-1, 0, 1]])  # 题目原例
    check([], [])  # 空数组
    check([0, 1, 1], [])  # 无解
    check([0, 0, 0], [[0, 0, 0]])  # 三个 0:合法答案别被去重吃掉
    check([0, 0, 0, 0], [[0, 0, 0]])  # ← 照妖镜:去重写错这里就现形
    check([-2, 0, 1, 1, 2], [[-2, 0, 2], [-2, 1, 1]])  # 有两组答案
    check([-2, 0, 0, 2, 2], [[-2, 0, 2]])