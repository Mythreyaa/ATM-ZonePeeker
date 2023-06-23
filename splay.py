class Node:
    def __init__(self,bank_det=[],par = None,left = None,right = None):
        self.bank_det = bank_det
        self.parent = par
        self.left = left
        self.right = right

class SplayTrees:
    def __init__(self):
        self.root = None

    def leftrot(self,p):
        rt = p.right
        subt = rt.left

        p.right = subt
        if subt:
            subt.parent = p
        
        rt.parent = p.parent
        if not p.parent:
            self.root = rt
        
        elif p == p.parent.left:
            p.parent.left = rt

        elif p == p.parent.right:
            p.parent.right = rt

        rt.left = p
        p.parent = rt
       
        return rt
    
    def rightrot(self,p):
        lt = p.left
        subt = lt.right

        p.left = subt
        if subt:
            subt.parent = p

        lt.parent = p.parent
        if not p.parent:
            self.root = lt
        
        elif p == p.parent.left:
            p.parent.left = lt

        elif p == p.parent.right:
            p.parent.right = lt

        lt.right = p
        p.parent = lt
        
        return lt

    def splay(self,new):
        while new.parent:
            if new.parent == self.root:
                if new == self.root.left:
                    self.rightrot(self.root)
                
                else:
                    self.leftrot(self.root)
        
            else:
                p = new.parent
                gp = new.parent.parent
                if new == p.left and p == gp.left:
                    self.rightrot(gp)
                    self.rightrot(p)
                    
                elif new == p.right and p == gp.right:
                    self.leftrot(gp)
                    self.leftrot(p)
                   
                elif new == p.left and p == gp.right:
                    self.rightrot(p)
                    self.leftrot(gp)
                   
                elif new == p.right and p == gp.left:
                    self.leftrot(p)
                    self.rightrot(gp)

    def ord_val(self,item):
        self.c=0
        for i in item:
            self.c += ord(i.lower())
        print(item,self.c)
        return self.c

    def insert(self,data,p = None):
        if not p:
            p = self.root

        if not p:
            new = Node(data)
            self.root = new
            self.splay(new)

        elif self.ord_val(data.bank_det[0][0]) < self.ord_val(p.bank_det[0][0]):
            if not p.left:
                new = Node(data,par = p)
                p.left = new
                self.splay(new)
                return
            
            else:
                self.insert(data,p.left)
        
        elif self.ord_val(data.bank_det[0][0]) > self.ord_val(p.bank_det[0][0]):
            if not p.right:
                new = Node(data,par = p)
                p.right = new
                self.splay(new)
                return
            
            else:
                self.insert(data,p.right)

    def maximum(self,p):
        if not p.right:
            return p
        self.maximum(p.right)

    def join(self,left,right):
        if left:
            maxleft = self.maximum(left)
            self.splay(maxleft)
            left.right = right
            right.parent = left
            self.root = left

        else:
            self.root = right

    def split(self,root):
        templ = None
        tempr = None
        if root.right:
            tempr = root.right
            root.right.parent = None
            root.right = None

        if root.left:
            templ = root.left
            root.left.parent = None
            root.left = None

        self.join(templ,tempr)

    #Top-down
    def delete(self,data,p = None):
        if not p:
            p = self.root

        if not p:
            return None
        
        if p.data == data:
            self.splay(p)
            self.split(p)
            return

        elif data < p.data:
            if not p.left:
                print("Data not found!")
                self.splay(p)
                return
            self.delete(data,p.left)

        elif data > p.data:
            if not p.right:
                print(f"Data {data} not found!")
                self.splay(p)
                return
            self.delete(data,p.right)

    def search(self,data,p = None):
        if not p:
            p = self.root
        
        if not self.root:
            return False

        if data[0] != p.bank_det[0] and data[1] != p.bank_det[1] and not p.left and not p.right:
            self.splay(p)
            return "Element not found!"

        elif data[0] == p.bank_det[0] and data[1] == p.bank_det[1]:
            self.splay(p)
            return p.bank_det
        
        elif self.ord_val(data.bank_det[0][0]) < self.ord_val(p.bank_det[0][0]):
            return self.search(data,p.left)

        elif self.ord_val(data.bank_det[0][0]) > self.ord_val(p.bank_det[0][0]):
            return self.search(data,p.right)

    def inorder(self,p=None):
        if not p:
            p = self.root 
        print(p.data)
        if p.left != None:
            self.inorder(p.left)
        #print(p.data)
        if p.right != None:
            self.inorder(p.right)

if __name__ == "__main__":
    s = SplayTrees()
    
    s.insert(10)
    s.insert(20)
    s.insert(30)
    s.insert(100)
    s.insert(90)
    s.insert(40)
    s.insert(50)
    s.insert(60)
    s.insert(70)
    s.insert(80)
    s.insert(150)
    s.insert(110)
    s.insert(120)
    
    print("Insertion - inorder")
    s.inorder()
    print("-------------------------------------------")
    s.delete(10)
    s.delete(120)
    s.delete(155)
    
    print("Deletion - inorder")
    s.inorder()
    print("---------------------------------------------")
    
    print(s.search(70))
    print(s.search(120))
        


