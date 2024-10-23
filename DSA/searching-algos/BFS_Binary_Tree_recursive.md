This code implements a *Level Order Traversal* of a binary tree, which is commonly known as **Breadth-First Search (BFS)** in tree traversal.

```python
# Recursive Python program for level
# order traversal of Binary Tree

class Node:
    def __init__(self, key):
        self.data = key
        self.left = None
        self.right = None

# Function to  print level order traversal of tree
def printLevelOrder(root):
    h = height(root)
    for i in range(1, h+1):
        printCurrentLevel(root, i)

# Print nodes at a current level
def printCurrentLevel(root, level):
    if root is None:
        return
    if level == 1:
        print(root.data, end=" ")
    elif level > 1:
        printCurrentLevel(root.left, level-1)
        printCurrentLevel(root.right, level-1)

# Compute the height of a tree-
def height(node):
    if node is None:
        return 0
    else:
        lheight = height(node.left)
        rheight = height(node.right)
        if lheight > rheight:
            return lheight+1
        else:
            return rheight+1

if __name__ == '__main__':
    root = Node(1)
    root.left = Node(2)
    root.right = Node(3)
    root.left.left = Node(4)
    root.left.right = Node(5)
    printLevelOrder(root)

```

### Let's break it down step by step:

1. **Node Class**:
   ```python
   class Node:
       def __init__(self, key):
           self.data = key
           self.left = None
           self.right = None
   ```
   - This class represents a node in the binary tree.
   - Each node has a `data` field (which stores the value of the node), and two pointers (`left` and `right`) which point to the left and right children of the node, respectively. These pointers are initialized to `None`.

2. **printLevelOrder Function**:
   ```python
   def printLevelOrder(root):
       h = height(root)
       for i in range(1, h+1):
           printCurrentLevel(root, i)
   ```
   - This function performs a level order traversal of the tree.
   - It first calculates the **height** of the tree by calling the `height()` function.
   - Then, for each level (from 1 to the height of the tree), it prints all the nodes at that level by calling the `printCurrentLevel()` function.

3. **printCurrentLevel Function**:
   ```python
   def printCurrentLevel(root, level):
       if root is None:
           return
       if level == 1:
           print(root.data, end=" ")
       elif level > 1:
           printCurrentLevel(root.left, level-1)
           printCurrentLevel(root.right, level-1)
   ```
   - This function prints the nodes at the current level.
   - It works recursively:
     - If the `level` is 1, it means we are at the current level, so it prints the node's data.
     - If the `level` is greater than 1, it recursively calls itself for both the left and right children, but with the level decreased by 1. This way, it moves deeper into the tree, level by level.

4. **height Function**:
   ```python
   def height(node):
       if node is None:
           return 0
       else:
           lheight = height(node.left)
           rheight = height(node.right)
           if lheight > rheight:
               return lheight+1
           else:
               return rheight+1
   ```
   - This function calculates the height (or depth) of the binary tree.
   - If the node is `None`, the height is 0 (this is the base case).
   - Otherwise, it calculates the height of the left and right subtrees and returns the maximum of the two plus 1 (to account for the current node).

### Example:

In the `__main__` part of the code:
```python
if __name__ == '__main__':
    root = Node(1)
    root.left = Node(2)
    root.right = Node(3)
    root.left.left = Node(4)
    root.left.right = Node(5)
    printLevelOrder(root)
```
- We are creating the following binary tree:

      ```
          1
         / \
        2   3
       / \
      4   5
      ```

- Then, we call `printLevelOrder(root)` to print the tree level by level:
   - First level: `1`
   - Second level: `2 3`
   - Third level: `4 5`

The output will be:
```
1 2 3 4 5
```

### Key Concept: **Breadth-First Search (BFS)**
- BFS explores nodes level by level (i.e., it visits all nodes at a particular depth before moving to the next depth). This is exactly what the `printLevelOrder()` function is doing: it prints all nodes at each level of the tree in sequence.

### Summary:
- The code implements BFS (Level Order Traversal) in a recursive way by leveraging the height of the tree to print nodes level by level.
- Although this is a simple, intuitive method, it is not the most efficient in terms of space because it recalculates the height of the tree multiple times (once per level). A more efficient implementation would use a queue, which is the traditional approach for BFS.