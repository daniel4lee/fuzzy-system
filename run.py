from PyQt5.QtCore import QCoreApplication, QObject, QRunnable, QThread, QThreadPool, pyqtSignal, pyqtSlot
import shapely.geometry as sp
import descartes
import math as M
class RunSignals(QObject):
    '''
    Defines the signals available from a running thread. 
    Supported signals are:
    finished
        No data
    error
        `tuple` (exctype, value, traceback.format_exc() )
    result
        `object` data returned from processing, anything
    '''
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
class CarRunning(QRunnable):
    """
    work thread
    """
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

        ''' creat car circle polygon & dir sensors '''
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

        '''initial dir, l, r line for counting intersection'''
        ix = self.data["{}".format(self.filename)].start[0]
        iy = self.data["{}".format(self.filename)].start[1]
        ifai = self.data["{}".format(self.filename)].start[2]
        dir_line = [[ix, iy], [ix + r * M.cos(M.radians(ifai)), iy + r * M.sin(M.radians(ifai))]]
        l_line = [[ix, iy], [ix + r * M.cos(M.radians(ifai + 45)), iy + r * M.sin(M.radians( ifai + 45 ))]]
        r_line = [[ix, iy], [ix + r * M.cos( M.radians(ifai - 45)), iy + r * M.sin(M.radians(ifai + 45))]]
        print('length',sp.LineString(r_line).intersection(map_line)[0].x)
        #while(not car.intersection(map_line)):
            #.clear()

        trace6d=[]
        for i in range(6):
            trace6d.append([])

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
