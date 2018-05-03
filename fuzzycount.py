import math

class counting():
    def __init__(self, x, y, theta):
        #do?
    def gfun(self, x, m, o):
        temp = -((x-m)**2)
        temp = temp/(2*(o**2))
        return math.exp(temp) 
    def sfun(self, x, a, b):
        if x < a:
            return 0
        elif a <= x and x < (a+b)/2:
            return 2*(((x-a)/(b-a))**2)
        elif (a+b)/2 <= x and x < b:
            return 1-(2*(((x-b)/(b-a))**2))
        elif b <= x:
            return 1    
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
