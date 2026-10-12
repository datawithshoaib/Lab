class BST:
    def __init__(self, key):
        self.key = key
        self.lchild = None 
        self.rchild = None

    def insert(self, data):
        if self.key is None:
            self.key = data
            return
        # to ignore the duplicates
        if self.key == data:
            return
        if self.key > data:
            if self.lchild:
                self.lchild.insert(data)
            else:
                self.lchild = BST(data)
        else:
            if self.rchild:
                self.rchild.insert(data)
            else:
                self.rchild = BST(data)

    def search(self, data):
        if self.key == data:
            print('Node is found!')
            return
        if data < self.key:
            if self.lchild:
                self.lchild.search(data)
            else:
                print('Node is not present in tree')
        else:
            if self.rchild:
                self.rchild.search(data)
            else:
                print('Node is not present in tree')
    
    def preorder(self):
        print(self.key, end=' ')
        if self.lchild:
            self.lchild.preorder()
        if self.rchild:
            self.rchild.preorder()
    
    def postorder(self):
        if self.lchild:
            self.lchild.postorder()
        if self.rchild:
            self.rchild.postorder()
        print(self.key, end = ' ')
    
    def inorder(self):
        if self.lchild:
            self.lchild.inorder()
        print(self.key, end = ' ')
        if self.rchild:
            self.rchild.inorder()

## test for search
root = BST(10)
l = [6, 3, 7, 8, 12, 20]
for i in l:
    root.insert(i)

# root.search(20)

## pre order traversal
# root.preorder()

## post order traversal
# root.postorder()
    
## in order traversal
root.inorder()
