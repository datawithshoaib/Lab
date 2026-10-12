class Node:
    def __init__(self, item):
        self.left = None
        self.right = None
        self.val = item

# check if full binary tree
def isFullTree(root):
    # if tree empty, then it is full binary tree, so return true
    if root is None:
        return True
    
    # check if root node has both left and right children as none, if yes then return true 
    if root.left == None and root.right == None:
        return True
    
    if root.left is not None and root.right is not None:
        return (isFullTree(root.left) and isFullTree(root.right))
    
    return  False

root = Node(1)
root.left = Node(2)
root.right = Node(3)
root.left.right = Node(4)

if isFullTree(root):
    print("The tree is a full binary tree.")
else:
    print("The tree is not a full binary tree.")
