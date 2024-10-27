DFS (Depth-First Search) is a popular algorithm for traversing or searching through tree or graph structures. In a binary tree, DFS explores as far down a branch as possible before backtracking.

### Key Points:
1. **Binary Tree Structure**:
   - Each node in a binary tree can have up to two children: a left child and a right child.
   - In DFS, you start at the root node and explore each branch completely before moving on to the next branch.

### DFS Traversal Methods:
DFS can be implemented in three main ways when applied to binary trees:
1. **In-order (Left, Root, Right)**: 
   - Traverse the left subtree, visit the root, and then traverse the right subtree.
   
2. **Pre-order (Root, Left, Right)**: 
   - Visit the root first, then traverse the left subtree, and finally the right subtree.
   
3. **Post-order (Left, Right, Root)**: 
   - Traverse the left subtree, then the right subtree, and visit the root last.

### Example Code:
Here’s how you can implement DFS in Python for a binary tree:

```python
# Define a class for a Node in the binary tree
class TreeNode:
    def __init__(self, value):
        self.value = value  # Store the value of the node
        self.left = None    # Left child
        self.right = None   # Right child

# Depth First Search: In-order Traversal (Left, Root, Right)
def dfs_inorder(node):
    if node:  # If the current node exists
        dfs_inorder(node.left)  # Traverse left subtree
        print(node.value)  # Visit the root
        dfs_inorder(node.right)  # Traverse right subtree

# Depth First Search: Pre-order Traversal (Root, Left, Right)
def dfs_preorder(node):
    if node:
        print(node.value)  # Visit the root
        dfs_preorder(node.left)  # Traverse left subtree
        dfs_preorder(node.right)  # Traverse right subtree

# Depth First Search: Post-order Traversal (Left, Right, Root)
def dfs_postorder(node):
    if node:
        dfs_postorder(node.left)  # Traverse left subtree
        dfs_postorder(node.right)  # Traverse right subtree
        print(node.value)  # Visit the root

# Example of creating a binary tree
root = TreeNode(1)   # Root node
root.left = TreeNode(2)  # Left child of root
root.right = TreeNode(3)  # Right child of root
root.left.left = TreeNode(4)  # Left child of node 2
root.left.right = TreeNode(5)  # Right child of node 2

# Testing In-order Traversal
print("In-order Traversal:")
dfs_inorder(root)

# Testing Pre-order Traversal
print("Pre-order Traversal:")
dfs_preorder(root)

# Testing Post-order Traversal
print("Post-order Traversal:")
dfs_postorder(root)
```

### Explanation:
- We define a `TreeNode` class to represent each node in the binary tree.
- The `dfs_inorder`, `dfs_preorder`, and `dfs_postorder` functions perform the three different types of DFS traversals.
- In the example, we create a simple binary tree with 5 nodes and demonstrate all three types of DFS.

### Sample Output:
Given the binary tree:
```
      1
     / \
    2   3
   / \
  4   5
```
- **In-order Traversal**: `4 2 5 1 3`
- **Pre-order Traversal**: `1 2 4 5 3`
- **Post-order Traversal**: `4 5 2 3 1`

### How DFS Works:
- **In-order** goes to the leftmost node first, processes it, then moves up to the parent, and finally to the right subtree.
- **Pre-order** starts from the root, processes it, then explores the left and right subtrees.
- **Post-order** traverses both subtrees first and only processes the root after both left and right children are explored. 

This is a simple way to understand DFS in a binary tree, which is commonly used for tasks like tree traversal, searching, and pathfinding.