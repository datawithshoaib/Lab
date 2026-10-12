class Node:
    def __init__(self, k):
        self.key = k
        self.left = None
        self.right = None

def calculateDepth(node):
    d = 0
    while node is not None:
        d += 1
        node = node.left
    return d

def is_perfect(root, d, level = 0):
    if root is None:
        return True
    
    if root.left is None and root.right is None:
        return (d == level + 1)
    
    if root.left is None or root.right is None:
        return False
    
    if root.left is not None and root.right is not None:
        return (is_perfect(root.left, d, level + 1) and is_perfect(root.right, d, level + 1))

root = None
root = Node(1)
root.left = Node(2)
root.right = Node(3)
root.left.left = Node(4)
root.left.right = Node(5)
root.right.left = Node(6)
root.right.right = Node(7)

if is_perfect(root, calculateDepth(root)):
    print("this is a perfect binary tree")
else: 
    print("this is not a perfect binary tree")








