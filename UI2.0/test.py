class test:
    c=4
    def __init__(self):
        self.a=0
        self.b=1
        # self.sum=3
    def sum(self):
        return self.a+self.b
val=test()
vl=[]
vl.append(val)
for a in vl:
    print(a.sum())