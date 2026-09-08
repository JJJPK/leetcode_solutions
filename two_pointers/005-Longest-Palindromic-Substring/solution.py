class Solution:
    def longestPalindrome(self, s: str) -> str:
        str_len = len(s)

        def expandFromCentre(s, left, right):
            # Keep expanding outward as long as we're within bounds
            # and the characters on both sides match.
            if left >= 0 and right < len(s) and s[left] == s[right]:
                return expandFromCentre(s, left - 1, right + 1)
            else:
                # Base case: either we've gone out of bounds, or the
                # characters no longer match. Step back one position
                # (left+1, right-1) to get the last valid palindrome
                # boundaries, and compute its length.
                return [left + 1, right - 1, right - left - 1]

        # Track the best (longest) palindrome found so far.
        p_left, p_right = 0, 0
        max_p = 0

        # Case 1: odd-length palindromes (single character center)
        # e.g. "aba" is centered on 'b' at index i.
        for i in range(str_len):
            left, right, temp = expandFromCentre(s, i, i)
            if temp > max_p:
                max_p = temp
                p_left, p_right = left, right

        # Case 2: even-length palindromes (center is between two characters)
        # e.g. "abba" is centered between the two 'b's at indices i, i+1.
        for i in range(str_len - 1):
            left, right, temp = expandFromCentre(s, i, i + 1)
            if temp > max_p:
                max_p = temp
                p_left, p_right = left, right

        # Slice is inclusive of p_right, so add 1 since Python slicing
        # excludes the end index.
        return s[p_left:p_right + 1]
