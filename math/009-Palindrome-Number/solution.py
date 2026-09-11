class Solution:
    def isPalindrome(self, x: int) -> bool:
        xx = x
        y = 0
        if x < 0:
            return False
        while xx > 0:
            y *= 10
            y += (xx % 10)
            xx = xx // 10
            print(xx)
        if x == y:
            return True
        else:
            return False