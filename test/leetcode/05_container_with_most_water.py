class Solution(object):
    def maxArea(self, height):
        """
        :type height: List[int]
        :rtype: int
        01.暴力求解,O(n^2)
        02.双指针
        计算两条垂线与 x 轴围成的容器最多能装多少水。



        思路：
            使用左右对撞双指针。初始时 left 在 0，right 在 len(height) - 1。
            当前水量 = min(height[left], height[right]) * (right - left)。
            计算后，移动高度较小的一侧：
                - 若 height[left] < height[right]，则 left += 1；
                - 否则 right -= 1。
            因为宽度只会缩小，保留较矮的一侧没有意义，
            移动较矮的一侧是安全的,两个理由:
               1. 已经算过的最大值都存进了 max_water,扔掉指针不会丢。
               2. 以这条矮边为边界的容器,已经到上限了:
                  宽度不可能更大(右边界最远就到这),
                  高度被这条矮边卡死(高度 = min(两边))。
                  所以没算过的那些也不可能超过当前值。
            移动它才可能找到更高的线来增大水量。

        复杂度：
            时间复杂度：O(n)，每个元素最多被访问一次。
            空间复杂度：O(1)，只使用常数个变量。
        """
        #01
        # max_water = 0
        # for i in range(len(height)):
        #     for j in range(i+1, len(height)):
        #         water = min(height[i], height[j]) * (j - i)
        #         max_water = max(max_water, water)
        #
        # return max_water

        #02
        max_water = 0
        left = 0
        right = len(height) - 1
        while left < right:
            current_water = min(height[left], height[right]) * (right - left)
            max_water = max(max_water, current_water)
            if height[left] < height[right]:
                left += 1
            else:
                right -= 1

        return max_water

if __name__ == '__main__':
    def check(height, expect):
        max_water = Solution().maxArea(height)
        flag = "✅" if max_water == expect else "❌"
        print(f"{flag} {height} → {max_water}（期望 {expect}）")

    check([1,8,6,2,5,4,8,3,7], 49)
    check([1,1], 1)
    check([4,3,2,1,4], 16)