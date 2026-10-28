class Solution(object):
    def moveZeroes(self, nums):
        """
        :type nums: List[int]
        :rtype: None Do not return anything, modify nums in-place instead.
        题意:把数组里所有 0 移到末尾,同时保持非零元素的相对顺序。必须原地修改,不能新建数组。

        思路：用快慢指针，两个索引都从数组开头出发。

        1. 定义快慢指针：slow 和 fast 都从数组开头 0 开始；fast 负责遍历整个数组，slow 负责记录“下一个非零元素应该放的位置”。
        2. 明确 slow 的含义：slow 左边始终是已经按原顺序排好的非零元素，slow 指向的位置就是下一个非零元素要放进去的位置。
        3. fast 从左到右扫描数组，每次只判断当前元素 nums[fast] 是不是 0。
        4. 如果 nums[fast] == 0：说明当前元素是 0，不需要保留在前面，直接跳过，fast 继续向右移动。
        5. 如果 nums[fast] != 0：说明当前元素是非零元素，需要把它放到前面 slow 指向的位置。
        6. 执行交换：交换 nums[slow] 和 nums[fast]。这样非零元素被换到前面，原来的 0 被换到后面。
        7. 交换后执行 slow += 1：表示前面的非零区扩大了一个位置，下一个非零元素应该放到新的 slow 位置。
        8. 为什么能保持非零元素相对顺序：因为 fast 是从左往右扫描的，先遇到的非零元素会先被交换到前面，后遇到的非零元素会后被放到后面，所以非零元素之间的顺序不会改变。
        9. 为什么一次遍历就够了：这种写法不是“先覆盖非零，再补零”，而是直接用交换处理。非零元素往前放的同时，0 也被换到了后面，因此不需要最后再遍历一次补 0。
        10. 遍历结束后的结果：所有非零元素都按原相对顺序集中在数组前面，所有 0 都被交换到了数组末尾。
        11. 时间复杂度：O(n)，因为 fast 只从左到右遍历一次数组。
        12. 空间复杂度：O(1)，只使用了 slow 和 fast 两个变量，原地修改数组，没有新建数组。
        13. 注意事项：题目要求原地修改，所以不需要返回新数组；return nums 可以省略，LeetCode 会直接检查 nums 的最终状态。

        示例
        输入: nums = [0,1,0,3,12]
        输出: [1,3,12,0,0]
        """
        slow = 0
        for fast in range(len(nums)):
            if nums[fast] == 0:
                continue
            nums[fast], nums[slow] = nums[slow], nums[fast]
            slow += 1




if __name__ == '__main__':
    def check(nums, expect):
        original = list(nums)
        Solution().moveZeroes(nums)
        flag = "✅" if nums == expect else "❌"
        print(f"{flag} {original} → {nums}（期望 {expect}）")

    check([0,1,0,3,12], [1,3,12,0,0])
    check([0], [0])
    check([1], [1])
    check([0,0,1], [1,0,0])
    check([], [])
    check([0,0,0], [0,0,0])