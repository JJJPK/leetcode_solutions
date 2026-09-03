# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        def addNode(n1, n2, carry):
            if not n1 and not n2 and carry == 0:
                return None

            v1 = n1.val if n1 else 0
            v2 = n2.val if n2 else 0
            total = v1 + v2 + carry

            next1 = n1.next if n1 else None
            next2 = n2.next if n2 else None

            node = ListNode(total % 10)
            node.next = addNode(next1, next2, total // 10)
            return node

        return addNode(l1, l2, 0)
