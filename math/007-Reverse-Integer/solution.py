class Solution:
    def reverse(self, x: int) -> int:
        isNegative = False
        if x < 0:
            x*=-1
            isNegative = True
        rev = ''

        for ch in str(x):
            rev = ch + rev
        
        reverse = int(rev)        
        if isNegative == True:
            reverse*=-1

        if reverse >= -exp2(31) and reverse <= exp2(31) -1:
            return reverse
        else:
            return 0