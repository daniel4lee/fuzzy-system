import math

class counting():
    def __init__(self, x, y, theta):
        #do?
    def gfun(self, x, m, o):
        temp = -((x-m)**2)
        temp = temp/(2*(o**2))
        return math.exp(temp) 
    def ANDop(self, mode, a, b):
        if mode=='m':
            return min(a,b)
    def ORop(self, mode, a, b):
        if mode=='m':
            return max(a,b)
    def Implication(self, mode, a, b):
        if mode=='d':
            return max(1-a, b)
        elif mode=='z':
            return max(min(a,b), 1-a)
