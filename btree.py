import sys
filename = sys.argv[1];
M = int(sys.argv[2])
S = int(sys.argv[3])
count=0

class Bplustree:

    def __init__(self,degree):
        self.degree=degree
        self.root=None

    def insert(self,key):
        if self.root is None:
            self.root = Block(self.degree,True)
            self.root.keys[0]=key;
            self.root.n +=1
        else:
            if 2*self.degree-1==self.root.n :
                newnode = Block(self.degree,False)
                newnode.child[0]=self.root
                self.root.parent  = newnode
                newnode.split(0,self.root)
                i=0
                if newnode.keys[0]<key:
                    i+=1
                newnode.child[i].insert(key)
                self.flag=1
                self.root=newnode
            else:
                self.root.insert(key)

    def search(self, key):
        if self.root is not None:
            return self.root.search(key) is not None
        return False
    def countkeys(self, key,c):
        if self.root is not None:
            self.root.countkeys(key,c)
    def rangekeys(self, a,b):
        if self.root is not None:
            self.root.rangekeys(a,b)

class Block:

    def __init__(self,degree,isleaf):
        self.degree=degree
        self.isleaf=isleaf
        self.n=0
        self.keys = [None]*(2*degree-1)
        self.child = [None]*(2*degree)
        self.parent=None

    def insert(self,key):
        i=self.n-1
        if self.isleaf :
            while i>=0  and self.keys[i] > key:
                self.keys[i+1]=self.keys[i]
                i-=1
            self.keys[i+1]=key;
            self.n+=1

        else :
            while i>=0  and self.keys[i] > key:
                i-=1
            if self.child[i+1].n==2*self.degree-1:
                self.split(i + 1, self.child[i + 1])
                if self.keys[i+1] < key :
                    i+=1
            self.child[i+1].insert(key)

    def search(self, key):
        i = 0
        while i < self.n and key > self.keys[i]:
            i += 1
        if i < self.n and self.keys[i] == key:
            return self.keys[i]
        if self.isleaf:
            return None
        return self.child[i].search(key)

    def split(self,t,ch):
        childnode = Block(ch.degree,ch.isleaf)

        for i in range(self.degree - 1):
            childnode.keys[i] = ch.keys[i + self.degree]
        childnode.n = self.degree - 1

        if not ch.isleaf:
            for i in range(self.degree):
                childnode.child[i] = ch.child[i + self.degree]
        ch.n = self.degree - 1

        for i in range(self.n, t, -1):
            self.child[i + 1] = self.child[i]
        self.child[t + 1] = childnode
        for i in range(self.n - 1, t - 1, -1):
            self.keys[i + 1] = self.keys[i]
        self.keys[t] = ch.keys[self.degree - 1]
        self.n += 1

    def countkeys(self,key,c):
        global count
        i = 0
        while i < self.n:
            if not self.isleaf:
                self.child[i].countkeys(key,c)
            if self.keys[i]==key:
                count+=1
            i += 1
        if not self.isleaf:
            self.child[i].countkeys(key,c)

    def rangekeys(self,a,b):
        global count
        i = 0
        while i < self.n:
            if not self.isleaf:
                self.child[i].rangekeys(a,b)
            if self.keys[i]>=a and self.keys[i]<=b:
                count+=1
            i += 1
        if not self.isleaf:
            self.child[i].rangekeys(a,b)

def readfile():
    global count
    for line in open(filename,'r'):
        f = line.strip().split()
        if f[0]=='INSERT':
            obj.insert(int(f[1]))
        elif f[0]=='FIND':
            val = obj.search(int(f[1]))
            if val:
                print('YES')
            else:
                print('NO')
        elif f[0]=='COUNT':
            c=0
            count=0
            obj.countkeys(int(f[1]),c)
            print(count)
        elif f[0]=='RANGE':
            count=0
            obj.rangekeys(int(f[1]),int(f[2]))
            print(count)


if __name__ == '__main__':
    degree = int((S+4)/24)
    obj = Bplustree(degree)
    readfile()
