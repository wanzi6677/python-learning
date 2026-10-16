class Solution(object):
    def trap(self, height):
        """
        LeetCode Hot 100 第 7 题:接雨水 (Trapping Rain Water)
        链接:https://leetcode.cn/problems/trapping-rain-water/
        难度:困难
        分类:双指针

        题意:
            给定 n 个非负整数表示宽度为 1 的柱子高度图,
            下雨后计算这些柱子一共能接多少雨水。

        核心直觉(三个解法共用):
            某一根柱子上方能接的水 = min(左边最高, 右边最高) - 自己。
            减去自己后若 <= 0,说明这根柱子太高接不到水,记 0。

        解法 ①:暴力 —— 时间 O(n^2),空间 O(1)
            对每一根柱子 i,分别往左、往右各扫一遍找最高,再套公式。
            这是最直觉的版本,也是 ②③ 的对照组(用慢的验快的)。

        max 的口径:含自己(range(0, i+1) / range(i, n))
            把 i 自己算进"左边最高/右边最高"里,
            保证 min(max_left, max_right) >= height[i],水位结构性 >= 0。
            即便不加 max(0, ...) 也不会算出虚高的水。

        易错点:
            1. 左右扫的边界必须包含自己。
               不含自己时,min 可能取到比 height[i] 还小的值 -> 水位为负,
               靠 max(0, ...) 兜住结果虽对,但那是"掩盖",不是"正确"。
            2. 位置 0(或 n-1)没有外侧柱子,max 保持初值 0 是安全的 ——
               因为题目保证 height[i] >= 0,min(0, ...) - height[i] 必为负,被 max(0,...) 吃掉。
               若题目允许负高度,初值必须改成 -inf。
        """

        #01.暴力求解,对每一个柱子找左右最高的柱子,暴力解法的时间复杂度是 O(N2)

        total = 0
        for i in range(len(height)):
            max_left, max_right = 0, 0
            for j in range(0,i+1):
                max_left = max(max_left,height[j])
            for j in range(i,len(height)):
                max_right = max(max_right,height[j])
            total += max(0,min(max_left,max_right) - height[i])
        return total

        #02.预处理两个数组


    def trap2(self, height):
        """
                   解法 ②:预处理 —— 时间 O(n),空间 O(n)

                   思路:
                       ① 每次都要重扫左右两边,而 left_max[i] 和 left_max[i-1] 只差一个数字
                       -> 大量计算被重复做了。
                       把 left_max / right_max 预先算好存成两个数组,
                       最后再扫一遍套公式。这就是"空间换时间"。

                   递推式(注意用的是 i-1 / i+1,不是 i):
                       left_max[0]  = 0
                       left_max[i]  = max(left_max[i-1], height[i-1])    从左往右扫
                       right_max[n-1] = 0
                       right_max[i]  = max(right_max[i+1], height[i+1])  从右往左扫

                   max 的口径:不含自己
                       定义是"位置 i 左侧(不含 i)的最高柱子"。
                       这才是"左边最高"的字面含义 —— 自己不算自己的左边。
                       因此 min(left_max[i], right_max[i]) - height[i] 可能是负数,
                       必须用 max(0, ...) 归零。

                   ⚠️ 三个解法的口径注定不统一(这不是缺陷):
                       ② 的 max 是"整条边的最高",可以预先算完;
                       ①③ 的 max 是"已扫过的最高",边扫边涨。
                       含义不同 -> 写法不同。但每个解法内部必须自洽。

                   易错点:
                       1. 递推一定要用 height[i-1] / height[i+1](不含自己),
                          写成 height[i] 就变成含自己,和另一侧口径不一致时会静默算错。
                       2. n == 0 必须提前 return,否则 [0]*0 之后的循环和下标访问都是空转/越界。
                       3. right_max 必须倒着扫(range(n-2, -1, -1)),步长 -1 别漏。
                       4. 初值 0 的理由同 ①:题目保证非负高度。
                   """
        n = len(height)
        if n == 0:
            return 0
        left_max = [0] * n
        right_max = [0] * n

        # 正向扫一遍 → 填 left_max
        left_max[0] = 0
        for i in range(1,n):
            left_max[i] = max(left_max[i-1], height[i-1])
        # 反向扫一遍 → 填 right_max
        right_max[n-1] = 0
        for i in range(n-2, -1, -1):
            right_max[i] = max(right_max[i+1], height[i+1])

        # 再扫一遍,用公式累加
        total = 0
        for i in range(len(height)):
            total += max(0, min(left_max[i], right_max[i]) - height[i])
        return total

    # 03.双指针
    def trap3(self, height):
        """
                解法 ③:双指针 —— 时间 O(n),空间 O(1)  <- 面试要的最优解

                做法:
                    left / right 从两端往中间收,只维护 left_max / right_max 两个变量。
                    每轮比较 left_max 和 right_max,谁小就处理谁那一侧。

                ⚠️ 判据是"谁的 max 小",不是"哪根柱子矮"
                    第 5 题(盛水)比的是 height[left] vs height[right](当前柱);
                    本题比的是 left_max vs right_max(两侧已扫过的历史最高)。
                    长得像,判据完全不同,别混。

                为什么可以放心只挪一边(完整论证必须两半):
                    算过的:    每格水量算完立刻累加进 total,指针扔掉不会丢。
                    没算过的:  当 left_max < right_max 时:
                                - left 这格的水 = min(left_max, right_max) - height[left]
                                  = left_max - height[left]   (left_max 更小,min 取它)
                                  -> 现在就能算准,不需要知道 right_max 的确切值。
                                - left 右边那些还没算的格子,左边最高只会 >= left_max,
                                  水位上界被 left_max 压住,不可能更好。
                    结论:这条 left_max 已经"到极限了",可以放心把 left 往里挪。

                max 的口径:不含自己(靠事后补更新)
                    先算水位、再挪指针、最后用刚处理过的那格补更新:
                        left_max = max(left_max, height[left-1])
                    含义是"left 指针已经扫过的最高",天然不含当前格。
                    因此水位必须先 max(0, ...) 归零。

                ⚠️ 循环边界必须是 while left <= right(左闭右闭)
                    若改成 while left < right,两指针相遇的那一格永远不会被处理
                    -> [5, 0, 5] 会输出 0(正确答案是 5)。
                    这是"改了边界就静默出错"的地方,自测必须覆盖"中间一个孤立深坑"的形状。

                易错点:
                    1. left_max / right_max 的初始化是 0(还没扫过任何柱子),
                       第一轮水位必然是 max(0, 0 - height[...]) = 0,正常,不是 bug。
                    2. left += 1 必须在算完水位之后;
                       补更新用 height[left-1](刚处理过的那格),不是 height[left](还没处理)。
                       写反了要么越界,要么漏掉当前格。
                    3. 循环退出时 left > right,所有格子恰好被处理一次。
                """
        n = len(height)
        if n == 0:
            return 0
        left_max = 0
        right_max = 0
        left = 0
        right = n - 1
        total = 0
        while left<=right:
            if left_max <= right_max:
                total += max(0, left_max - height[left])
                left += 1
                left_max = max(left_max, height[left-1])
            else:
                total += max(0, right_max - height[right])
                right -= 1
                right_max = max(right_max, height[right+1])
        return total



if __name__ == '__main__':
    def check(height, expect):
        total = Solution().trap3(height)
        flag = "✅" if total == expect else "❌"
        print(f"{flag} {height} → {total}（期望 {expect}）")

    check([0,1,0,2,1,0,1,3,2,1,2,1], 6)
    check([], 0)
    check([3,3,3], 0)
    check([4,2,3], 1)
    check([5,0,5], 5)
