def two_sum(nums, target):
    """
    给定一个整数数组和一个目标值,返回和为目标值的两个数的【下标】。
    例: nums=[2,7,11,15], target=9 → [0,1]
    """
    #解法一（暴力）
    # for i in range(len(nums)):
    #     for j in range(i+1,len(nums)):
    #         if nums[i] + nums[j] == target:
    #             return [i, j]

    #解法二（哈希表）
    seen = {}
    for i in range(len(nums)):
        need = target - nums[i]
        if need in seen:
            return [seen[need], i]
        else:
            seen[nums[i]] = i

    return None

if __name__ == "__main__":
    case = [
        ([2,7,11,15],9,[0,1]),
        ([3,2,4],6,[1,2]),
        ([3,3],6,[0,1]),
        ([2,7,11,15],30,None),

    ]
    for nums, target, expect in case:
        got = two_sum(nums, target)
        flag = "✅" if got == expect else "❌"
        print(f"{flag} nums={nums}, target={target} → 得到 {got},期望 {expect}")
