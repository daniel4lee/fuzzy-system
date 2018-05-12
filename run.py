from PyQt5.QtCore import QCoreApplication, QObject, QRunnable, QThread, QThreadPool, pyqtSignal, pyqtSlot
import shapely.geometry as sp
import descartes
import math as M


class RunSignals(QObject):
    result = pyqtSignal(object)


class CarRunning(QRunnable):
    """ 
    work thread, will execute "run" first
    """

    def __init__(self, oplist, fuzzylist, data, filename):
        super(CarRunning, self).__init__()
        self.data = data[filename]
        self.fuzzylist = fuzzylist
        self.signals = RunSignals()

        self.oplist = oplist  # temp not used

    @pyqtSlot()
    def run(self):
        """
        Run this function 
        """
        trace6d = []
        for i in range(6):
            trace6d.append([])

        # creat end area by shapely
        end_area = []
        end_area.append([self.data.x[0], self.data.y[0]])
        end_area.append([self.data.x[1], self.data.y[0]])
        end_area.append([self.data.x[0], self.data.y[1]])
        end_area.append([self.data.x[1], self.data.y[1]])
        end_area = sp.Polygon(sp.LineString(end_area))

        # creat map line by shapely
        map_line = []
        for i in range(2, len(self.data.x)):
            map_line.append([self.data.x[i], self.data.y[i]])
        map_line = sp.LineString(map_line)

        car_center = (self.data.start[0], self.data.start[1])
        car = sp.Point(*car_center).buffer(3)
        # main loop for computing through fuzzy architecture
        while(not car.intersection(map_line)):
            '''if(car.intersection(end_area)):
                print("end!!")
                break'''
            # return signal here !!
            # creat car circle polygon by shapely and initial it, r, x, y
            if (len(trace6d[0]) == 0):
                # count the distance
                max_px = max_py = -M.inf
                min_px = min_py = M.inf
                for i, j in zip(self.data.x[2:], self.data.y[2:]):
                    if(i > max_px):
                        max_px = i
                    if(i < min_px):
                        min_px = i
                    if(j > max_py):
                        max_py = j
                    if(j < min_py):
                        min_py = j
                r = ((max_px - min_px)**2 + (max_py - min_py)**2)**(0.5)
                # initial x y fai
                x = self.data.start[0]
                y = self.data.start[1]
                fai = self.data.start[2]
                output = 0
            else:
                """update new point for computing """
                car_center = (car_center[0] + M.cos(M.radians(fai + output)) + M.sin(M.radians(fai))*M.sin(M.radians(output)),
                              car_center[1] + M.sin(M.radians(fai + output)) - M.sin(M.radians(output))*M.cos(M.radians(fai)))
                car = sp.Point(*car_center).buffer(3)
                x = car_center[0]
                y = car_center[1]
                fai = fai - M.degrees(M.asin(2*M.sin(M.radians(output))/6))
            ##
            trace6d[0].append(x)
            trace6d[1].append(y)
            # dir, l, r line for counting intersection

            dir_line = [
                [x, y], [x + r * M.cos(M.radians(fai)), y + r * M.sin(M.radians(fai))]]
            l_line = [[x, y], [
                x + r * M.cos(M.radians(fai + 45)), y + r * M.sin(M.radians(fai + 45))]]
            r_line = [[x, y], [
                x + r * M.cos(M.radians(fai - 45)), y + r * M.sin(M.radians(fai - 45))]]

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

            # define front distance function and computing firing strength
            front_small = self.g_decreasing_funct(dir_dist, 5, 5)
            front_medium = self.gfun(dir_dist, 12, 5)
            front_large = self.gufun(dir_dist, 20, 5)

            # define left-right distance function and computing firing strength
            l_r = l_dist-r_dist
            lr_s = self.g_decreasing_funct(l_r, -10, 5)
            lr_m = self.gfun(l_r, 0, 5)
            lr_l = self.gufun(l_r, 10, 5)

            # define consequence function and computing firing strength
            rule = []
            for i in range(0, 9):
                rule.append([])
            # totall z in range of 81
            for z in range(-400, 410):
                r_s = self.g_decreasing_funct(z/10, -10, 20)
                r_m = self.gfun(z/10, 0, 20)
                r_l = self.gufun(z/10, 10, 20)
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
            for i in range(-400, 410):
                output_l.append(max(min(front_small, lr_s, rule[0][i+400]),
                                    min(front_small, lr_m, rule[1][i+400]),
                                    min(front_small, lr_l, rule[2][i+400]),
                                    min(front_medium, lr_s, rule[3][i+400]),
                                    min(front_medium, lr_m, rule[4][i+400]),
                                    min(front_medium, lr_l, rule[5][i+400]),
                                    min(front_large, lr_s, rule[6][i+400]),
                                    min(front_large, lr_m, rule[7][i+400]),
                                    min(front_large, lr_l, rule[8][i+400])))
            up = 0
            base = 0
            for i in range(-400, 410):
                up += i/10*output_l[i+400]
                base += output_l[i+400]
            if base != 0:
                output = up/base
            ### record wheel angle in trace6d ###
            trace6d[5].append(output)
            # clear paremeter
            rule.clear()
            output_l.clear()

        self.signals.result.emit(trace6d)

    def gfun(self, x, m, o):
        return M.exp(-(x - m)**2 / o**2)

    def gufun(self, x, m, o):
        if(x > m):
            return 1
        else:
            return M.exp(-(x - m)**2 / o**2)

    def g_decreasing_funct(self, x, m, o):
        if(x < m):
            return 1
        else:
            return M.exp(-(x - m)**2 / o**2)

    def ANDop(self, mode, a, b):
        if mode == 'm':
            return min(a, b)

    def ORop(self, mode, a, b):
        if mode == 'm':
            return max(a, b)

    def Implication(self, mode, a, b):
        if mode == 'd':
            return max(1-a, b)
        elif mode == 'z':
            return max(min(a, b), 1-a)

    def distance(self, points, car_loc):
        if isinstance(points, sp.MultiPoint):
            min_dis = ((points[0].x - car_loc[0])**2 +
                       (points[0].y - car_loc[1])**2)**(1/2)
            for i in range(1, len(points)):
                temp = ((points[i].x - car_loc[0])**2 +
                        (points[i].y - car_loc[1])**2)**(1/2)
                if(temp < min_dis):
                    min_dis = temp
            return min_dis
        elif isinstance(points, sp.Point):
            return ((points.x - car_loc[0])**2 + (points.y - car_loc[1])**2)**(1/2)
