# Definition for a binary tree node.
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def reach_end(root, s: list):
    if root.left is None and root.right is None:
        s.append(root.val)
    if root.left is not None:
        reach_end(root.left, s)
    if root.right is not None:
        reach_end(root.right, s)
    return s

root = TreeNode(3)
root.left = TreeNode(5)
root.right = TreeNode(1)
root.left.left = TreeNode(6)
root.left.right = TreeNode(2)
root.left.right.left = TreeNode(7)
root.left.right.right = TreeNode(4)
root.right.left = TreeNode(9)
root.right.right = TreeNode(8)

s = []
s1 = reach_end(root, s)
s = []
s2 = reach_end(root, s)

print(s1)
print(s2)
