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

    def __init__(self, data, filename, fuzzylist, fuzzy_variable):
        super(CarRunning, self).__init__()
        self.data = data[filename]
        self.fuzzylist = fuzzylist # small, medium, large
        self.fuzzy_variable = fuzzy_variable # mean and sd
        self.signals = RunSignals()

    @pyqtSlot()
    def run(self):
        """
        Run this function 
        """
         # trace data [0] = car center x, [1] = car center y, [2] = direction length, 
         # [3] = right length, [4] = left length, [5] = thita, [6] = direct point on map line
         # [7] = right point on map line, [8] left point on map line, [9] the angle between dir car and horizontal
        trace_10d = []
        for i in range(10):
            trace_10d.append([])

        # creat end area by shapely
        end_area = []
        end_area.append((self.data.x[0], self.data.y[0]))
        end_area.append((self.data.x[1], self.data.y[0]))
        end_area.append((self.data.x[1], self.data.y[1]))
        end_area.append((self.data.x[0], self.data.y[1]))
        end_area = sp.Polygon(end_area)
        

        # creat map line by shapely
        map_line = []
        for i in range(2, len(self.data.x)):
            map_line.append([self.data.x[i], self.data.y[i]])
        map_line = sp.LineString(map_line)

        car_center = (self.data.start[0], self.data.start[1])
        car = sp.Point(*car_center).buffer(3)
        # main loop for computing through fuzzy architecture
        while(not car.intersection(map_line)):

            # let data list[1] be 1 longer as signal here !!
            if(end_area.contains(sp.Point(car_center))):
                trace_10d[1].append(0)
                break
                
            # creat car circle polygon by shapely and initial it, r, x, y
            if (len(trace_10d[0]) == 0):
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
            trace_10d[0].append(x)
            trace_10d[1].append(y)
            trace_10d[9].append(fai)
            # dir, l, r line for counting intersection

            dir_line = [
                [x, y], [x + r * M.cos(M.radians(fai)), y + r * M.sin(M.radians(fai))]]
            l_line = [[x, y], [
                x + r * M.cos(M.radians(fai + 45)), y + r * M.sin(M.radians(fai + 45))]]
            r_line = [[x, y], [
                x + r * M.cos(M.radians(fai - 45)), y + r * M.sin(M.radians(fai - 45))]]

            # First, computing the dir, l, and r distance between car and wall
            temp = sp.LineString(dir_line).intersection(map_line)
            temp = self.distance(temp, car_center)
            dir_dist = temp[0]
            trace_10d[6].append(temp[1])
            temp = sp.LineString(r_line).intersection(map_line)
            temp = self.distance(temp, car_center)
            r_dist = temp[0]
            trace_10d[7].append(temp[1])
            temp = sp.LineString(l_line).intersection(map_line)
            temp = self.distance(temp, car_center)
            l_dist = temp[0]
            trace_10d[8].append(temp[1])

            ### record distace set in trace6d ###
            trace_10d[2].append(dir_dist)
            trace_10d[3].append(r_dist)
            trace_10d[4].append(l_dist)

            # define front distance function and computing firing strength
            front_small = self.g_decreasing_funct(dir_dist, self.fuzzy_variable[0], self.fuzzy_variable[1])
            front_medium = self.gfun(dir_dist, self.fuzzy_variable[2], self.fuzzy_variable[3])
            front_large = self.gufun(dir_dist, self.fuzzy_variable[4], self.fuzzy_variable[5])

            # define left-right distance function and computing firing strength
            l_r = l_dist-r_dist
            lr_s = self.g_decreasing_funct(l_r, self.fuzzy_variable[6], self.fuzzy_variable[7])
            lr_m = self.gfun(l_r, self.fuzzy_variable[8], self.fuzzy_variable[9])
            lr_l = self.gufun(l_r, self.fuzzy_variable[10], self.fuzzy_variable[11])

            # define consequence function and computing firing strength
            rule = []
            for i in range(0, 9):
                rule.append([])
            # totall z in range of 81
            for z in range(-400, 410):
                r_s = self.g_decreasing_funct(z/10, self.fuzzy_variable[12], self.fuzzy_variable[13])
                r_m = self.gfun(z/10, self.fuzzy_variable[14], self.fuzzy_variable[15])
                r_l = self.gufun(z/10, self.fuzzy_variable[16], self.fuzzy_variable[17])
                for b in range(9):
                    self.fuzzy_assign(rule[b], self.fuzzylist[b], r_s, r_m, r_l)

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
            if (output > 40):
                output = 40
            elif (output < -40):
                output = -40
            ### record wheel angle in trace6d ###
            trace_10d[5].append(output)
            # clear paremeter
            rule.clear()
            output_l.clear()

        self.signals.result.emit(trace_10d)

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
    def fuzzy_assign(self, rule_value_list, rule_description, s, m, l):
        if(rule_description == 'small'):
            rule_value_list.append(s)
        elif(rule_description == 'medium'):
            rule_value_list.append(m)
        elif(rule_description == 'large'):
            rule_value_list.append(l)

    def distance(self, points, car_loc):
        if isinstance(points, sp.MultiPoint):
            min_dis = ((points[0].x - car_loc[0])**2 +
                       (points[0].y - car_loc[1])**2)**(1/2)
            min_point = (points[0].x, points[0].y)
            for i in range(1, len(points)):
                temp = ((points[i].x - car_loc[0])**2 +
                        (points[i].y - car_loc[1])**2)**(1/2)
                if(temp < min_dis):
                    min_dis = temp
                    min_point = (points[i].x, points[i].y)
            l = [min_dis, min_point]
            return l
        elif isinstance(points, sp.Point):
            l = []
            l.append(((points.x - car_loc[0])**2 + (points.y - car_loc[1])**2)**(1/2))
            min_point = (points.x, points.y)
            l.append(min_point)
            return l