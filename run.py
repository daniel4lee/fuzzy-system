from PyQt5.QtCore import QCoreApplication, QObject, QRunnable, QThread, QThreadPool, pyqtSignal, pyqtSlot
import shapely.geometry as sp
import descartes
import math as M
class RunSignals(QObject):
    result = pyqtSignal(object)
class CarRunning(QRunnable):
    """ work thread """
    def __init__(self, oplist, fuzzylist, data, filename):
        super(CarRunning, self).__init__()
        self.data = data
        self.oplist = oplist
        self.fuzzylist= fuzzylist
        self.filename = filename
        self.signals = RunSignals()
    @pyqtSlot()
    def run(self):
        """ Run this function """

        trace6d = []
        for i in range(6):
            trace6d.append([])
        ''' creat end area '''
        ea = []
        ea.append([self.data["{}".format(self.filename)].x[0], self.data["{}".format(self.filename)].y[0]])
        ea.append([self.data["{}".format(self.filename)].x[1], self.data["{}".format(self.filename)].y[0]])
        ea.append([self.data["{}".format(self.filename)].x[0], self.data["{}".format(self.filename)].y[1]])
        ea.append([self.data["{}".format(self.filename)].x[1], self.data["{}".format(self.filename)].y[1]])
        end_area =sp.Polygon(sp.LineString(ea))

        ''' creat map line'''
        verts = []
        for i in range(2, len(self.data["{}".format(self.filename)].x)):
            verts.append([self.data["{}".format(self.filename)].x[i], self.data["{}".format(self.filename)].y[i]])
        map_line = sp.LineString(verts)

        while(not car.intersection(map_line)):
            '''if(car.intersection(end_area)):
                print("end!!")
                break'''
                #return signal here !!
            ''' creat car circle polygon & dir sensors '''
            if len(trace6d[0]) == 0:
                car_center = (self.data["{}".format(self.filename)].start[0], self.data["{}".format(self.filename)].start[1])
                car = sp.Point(self.data["{}".format(self.filename)].start[0], self.data["{}".format(self.filename)].start[1]).buffer(3)
                ''' count the distance '''
                max_px = 0
                max_py = 0
                min_px = 0
                min_py = 0
                for i in range(2, len(self.data["{}".format(self.filename)].x)):
                    if(self.data["{}".format(self.filename)].x[i] > max_px):
                        max_px = self.data["{}".format(self.filename)].x[i]
                    if(self.data["{}".format(self.filename)].x[i] < min_px):
                        min_px = self.data["{}".format(self.filename)].x[i]
                    if(self.data["{}".format(self.filename)].y[i] > max_py):
                        max_py = self.data["{}".format(self.filename)].y[i]
                    if(self.data["{}".format(self.filename)].y[i] < min_py):
                        min_py = self.data["{}".format(self.filename)].y[i]
                r = ((max_px - min_px)**2 + (max_py - min_py)**2)**(0.5)
                '''initial x y fai'''
                x = self.data["{}".format(self.filename)].start[0]
                y = self.data["{}".format(self.filename)].start[1]
                fai = self.data["{}".format(self.filename)].start[2]
            else: !

            trace6d[0].append(self.data["{}".format(self.filename)].start[0])
            trace6d[1].append(self.data["{}".format(self.filename)].start[1])

            '''dir, l, r line for counting intersection'''
            dir_line = [[x, y], [x + r * M.cos(M.radians(fai)), y + r * M.sin(M.radians(fai))]]
            l_line = [[x, y], [x + r * M.cos(M.radians(fai + 45)), y + r * M.sin(M.radians( fai + 45 ))]]
            r_line = [[x, y], [x + r * M.cos( M.radians(fai - 45)), y + r * M.sin(M.radians(fai - 45))]]
                    
            # First, computing the dir, l, and r distance between car and wall
            temp = sp.LineString(dir_line).intersection(map_line)
            dir_dist = self.distance(temp, car_center)
            temp = sp.LineString(l_line).intersection(map_line)
            l_dist = self.distance(temp, car_center)
            temp = sp.LineString(r_line).intersection(map_line)
            r_dist = self.distance(temp, car_center)
            
            ### record distace set in trace6d ###
            trace6d[2].append(dir_dist)
            trace6d[3].append(r_dist)
            trace6d[4].append(l_dist)

            #define front distance function and computing firing strength
            f_s = self.gdfun(dir_dist, 5, 5)
            f_m = self.gfun(dir_dist, 12, 5)
            f_l = self.gufun(dir_dist, 20, 5)

            #define left-right distance function and computing firing strength
            l_r = l_dist-r_dist
            lr_s = self.gdfun(l_r, -10, 5)
            lr_m = self.gfun(l_r, 0, 5)
            lr_l = self.gufun(l_r, 10, 5)

            #define consequence function and computing firing strength
            rule = []
            for i in range(0, 9):
                rule.append([])
            # totall z in range of 81
            for z in range(-40, 41):
                r_s = self.gdfun(z, -10, 20)
                r_m = self.gfun(z, 0, 20)
                r_l = self.gufun(z, 10, 20)
                rule[0].append(r_l)
                rule[1].append(r_s)
                rule[2].append(r_s)
                rule[3].append(r_l)
                rule[4].append(r_s)
                rule[5].append(r_s)
                rule[6].append(r_l)
                rule[7].append(r_s)
                rule[8].append(r_s)
            
            # output computing 
            output_l = []
            for i in range(-40, 41):
                output_l.append( max( min(f_s, lr_s, rule[0][i+40]), min(f_s, lr_m, rule[1][i+40]), min(f_s, lr_l, rule[2][i+40]), 
                min(f_m, lr_s, rule[3][i+40]), min(f_m, lr_m, rule[4][i+40]), min(f_m, lr_l, rule[5][i+40]), min(f_l, lr_s, rule[6][i+40]), 
                min(f_l, lr_m, rule[7][i+40]), min(f_l, lr_l, rule[8][i+40]) ))
            up = 0
            base = 0
            for i in range(-40, 41):
                up += i*output_l[i+40]
                base += output_l[i+40]
            output = up/base
            ### record wheel angle in trace6d ###
            trace6d[5].append(output)

            """update new point for computing """
            car_center = (car_center[0] + M.cos(M.radians(ifai + output)) + M.sin(M.radians(ifai))*M.sin(M.radians(output)),
            car_center[1] + M.sin(M.radians(ifai + output)) - M.sin(M.radians(output))*M.cos(M.radians(ifai)))
            car = sp.Point(car_center[0], car_center[1]).buffer(3)
            trace6d[0].append(car_center[0])
            trace6d[1].append(car_center[1])
            ix = car_center[0]
            iy = car_center[1]
            ifai = ifai - M.asin(2*M.sin(M.radians(output))/6)
            dir_line = [[ix, iy], [ix + r * M.cos(M.radians(ifai)), iy + r * M.sin(M.radians(ifai))]]
            l_line = [[ix, iy], [ix + r * M.cos(M.radians(ifai + 45)), iy + r * M.sin(M.radians( ifai + 45 ))]]
            r_line = [[ix, iy], [ix + r * M.cos( M.radians(ifai - 45)), iy + r * M.sin(M.radians(ifai + 45))]]
            # clear paremeter
            rule.clear()
            output_l.clear()
        '''for fill the trace6d in same len'''
        temp = sp.LineString(dir_line).intersection(map_line)
        dir_dist = self.distance(temp, car_center)
        temp = sp.LineString(l_line).intersection(map_line)
        l_dist = self.distance(temp, car_center)
        temp = sp.LineString(r_line).intersection(map_line)
        r_dist = self.distance(temp, car_center)
            ### record distace set in trace6d ###
        trace6d[2].append(dir_dist)
        trace6d[3].append(r_dist)
        trace6d[4].append(l_dist)

            #define front distance function and computing firing strength
        f_s = self.gdfun(dir_dist, 5, 5)
        f_m = self.gfun(dir_dist, 12, 5)
        f_l = self.gufun(dir_dist, 20, 5)

            #define left-right distance function and computing firing strength
        l_r = l_dist-r_dist
        lr_s = self.gdfun(l_r, -10, 5)
        lr_m = self.gfun(l_r, 0, 5)
        lr_l = self.gufun(l_r, 10, 5)

            #define consequence function and computing firing strength
        rule = []
        for i in range(0, 9):
            rule.append([])
            # totall z in range of 81
        for z in range(-40, 41):
            r_s = self.gdfun(z, -10, 20)
            r_m = self.gfun(z, 0, 20)
            r_l = self.gufun(z, 10, 20)
            rule[0].append(r_l)
            rule[1].append(r_s)
            rule[2].append(r_s)
            rule[3].append(r_l)
            rule[4].append(r_s)
            rule[5].append(r_s)
            rule[6].append(r_l)
            rule[7].append(r_s)
            rule[8].append(r_s)
            
            # output computing 
        output_l = []
        for i in range(-40, 41):
            output_l.append( max( min(f_s, lr_s, rule[0][i+40]), min(f_s, lr_m, rule[1][i+40]), min(f_s, lr_l, rule[2][i+40]), 
            min(f_m, lr_s, rule[3][i+40]), min(f_m, lr_m, rule[4][i+40]), min(f_m, lr_l, rule[5][i+40]), min(f_l, lr_s, rule[6][i+40]), 
            min(f_l, lr_m, rule[7][i+40]), min(f_l, lr_l, rule[8][i+40]) ))
        up = 0
        base = 0
        for i in range(-40, 41):
            up += i*output_l[i+40]
            base += output_l[i+40]
        output = up/base
            ### record wheel angle in trace6d ###
        trace6d[5].append(output)
        verts.clear()
        ea.clear()
        self.signals.result.emit(trace6d)
    def gfun(self, x, m, o):
        temp = -((x-m)**2)
        temp = temp/(2*(o**2))
        return M.exp(temp)
    def gufun(self, x, m, o):
        if(x > m):
            return 1
        else:
            temp = -((x-m)**2)
            temp = temp/(2*(o**2))
            return M.exp(temp)
    def gdfun(self, x, m, o):
        if(x < m):
            return 1
        else:
            temp = -((x-m)**2)
            temp = temp/(2*(o**2))
            return M.exp(temp)
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
    def distance(self, points, car_loc):
        if isinstance(points, sp.MultiPoint):
            min_dis = ((points[0].x - car_loc[0])**2 + (points[0].y - car_loc[1])**2)**(1/2)
            for i in range(1, len(points)):
                temp = ((points[i].x - car_loc[0])**2 + (points[i].y - car_loc[1])**2)**(1/2)
                if(temp < min_dis):
                    min_dis = temp
            return min_dis
        elif isinstance(points, sp.Point):
            return ((points.x - car_loc[0])**2 + (points.y - car_loc[1])**2)**(1/2)
