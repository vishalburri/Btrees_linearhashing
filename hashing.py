
import sys

filename = sys.argv[1];
M = int(sys.argv[2])
S = int(sys.argv[3])

class Buckets:
    def __init__(self):
        self.node = []
        self.overflow = None

class HashTable:
    def __init__(self,buffersize):
        self.buffersize=buffersize
        self.len = 0
        self.n=2
        self.i=1
        self.capacity = 0.75
        self.buckets = []
        b1 = Buckets()
        b2 = Buckets()
        self.buckets.append(b1)
        self.buckets.append(b2)

    def hash(self,key):
        return key%(1<<int(self.i))

    def insert(self,key):
        self.len+=1
        if float(self.len)/float((self.n)*(self.buffersize)) > self.capacity:
            self.n+=1
            b=Buckets()
            self.buckets.append(b)
            if self.n > (1<<self.i):
                self.i+=1
            c=0
            temp = self.n-1
            while temp!=0:
                temp=temp>>1
                c+=1
            cb = self.n - (1<<(c-1))-1
            temp =[]
            buck = self.buckets[cb]
            while buck!=None:
                temp+=buck.node
                buck.node=[]
                buck=buck.overflow

            for i in temp:
                self.len-=1
                self.insert(i)

        hashval = self.hash(key)
        if hashval > self.n:
            hashval -= (1<<(self.i-1))
        if len(self.buckets[hashval].node) <self.buffersize:
            self.buckets[hashval].node.append(key)
        else:
            b = Buckets()
            b.node.append(key)
            self.buckets[hashval].overflow = b

    def begininsert(self,key):
        hashval = self.hash(key)
        if hashval >= self.n:
            hashval -= (1<<(self.i-1))
        buck = self.buckets[hashval]
        while buck is not None:
            if key in buck.node:
                return 0
            buck=buck.overflow
        self.insert(key)
        #print(key)
        return 1

def readfile():
    current = 0
    for line in open(filename,'r'):
        record = line.strip()
        if len(inputbuffers[current]) == buffersize:
            prev_current = current
            current += 1
        if (current == len(inputbuffers) - 1 and len(inputbuffers[current]) == buffersize - 1):
            inputbuffers[current].append(record)
            process(obj, inputbuffers,outputbuffer)
            current=0
            continue
        else:
            inputbuffers[current].append(record)
    if len(inputbuffers[0])!=0:
        process(obj, inputbuffers,outputbuffer)

def process(obj,inputbuffers,outputbuffer):
    for index in range(len(inputbuffers)):
        for j in inputbuffers[index]:
            val = obj.begininsert(int(j))
            if val==1:
                outputbuffer.append(j)
                if (len(outputbuffer))==buffersize:
                    for k in range(len(outputbuffer)):
                        print(outputbuffer[k])
                    del outputbuffer[:]

    if len(outputbuffer)!=0:
        for i in range(len(outputbuffer)):
            print(outputbuffer[i])
        del outputbuffer[:]
                            
    for inputbuffer in inputbuffers:
        del inputbuffer[:]


if __name__ == '__main__':
    p = 4
    buffersize = int(S/p)
    inputbuffers = []
    outputbuffer=[]
    for i in range(M-1):
        inputbuffers.append([])
    obj = HashTable(buffersize)
    readfile()
