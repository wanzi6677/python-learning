class Solution(object):
    def rotate(self, nums, k):
        """
        :type nums: List[int]
        :type k: int
        :rtype: None Do not return anything, modify nums in-place instead.
        """
        k %= len(nums)

        def reverse(start, end):
            while start < end:
                nums[start], nums[end] = nums[end], nums[start]
                start += 1
                end -= 1

        reverse(0,len(nums)-1)
        reverse(0,k-1)
        reverse(k,len(nums)-1)


if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding="utf-8")

    def check(nums, k, expect):
        original = list(nums)
        Solution().rotate(nums, k)
        flag = "✅" if nums == expect else "❌"
        print(f"{flag} {original} k={k} → {nums}（期望 {expect}）")


    check([1, 2, 3, 4, 5, 6, 7], 3, [5, 6, 7, 1, 2, 3, 4])
    check([-1, -100, 3, 99], 2, [3, 99, -1, -100])
    check([1, 2], 3, [2, 1])
    check([1], 0, [1])
    check([1, 2, 3, 4, 5, 6], 2, [5, 6, 1, 2, 3, 4])
    check([1, 2, 3, 4, 5, 6], 4, [3, 4, 5, 6, 1, 2])