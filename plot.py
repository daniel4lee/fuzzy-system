import math
import numpy as np
from PyQt5.QtWidgets import *#(QWidget, QToolTip, QDesktopWidget, QPushButton, QApplication)
from PyQt5.QtCore import*

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.path import Path
import matplotlib.patches as patches

import shapely.geometry
import descartes

import time
class PlotCanvas(FigureCanvas):
 
    def __init__(self, dataset={}):
        fig = Figure(figsize=(8, 8), dpi=100)
        self.ax = fig.add_subplot(111)
        super().__init__(fig)
        self.dataset = dataset
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        imap = list(self.dataset.keys())[0]
        self.car = None
        self.dir = None
        self.plot_map(imap)
    def plot_map(self, imap):
        self.ax.clear()
        verts = []
        for i in range(2, len(self.dataset["{}".format(imap)].x)):
                verts.append([self.dataset["{}".format(imap)].x[i], self.dataset["{}".format(imap)].y[i]])
        line = shapely.geometry.LineString(verts)
        inicar = shapely.geometry.Point(self.dataset["{}".format(imap)].start[0], self.dataset["{}".format(imap)].start[1]).buffer(3)
        fxpoint = (self.dataset["{}".format(imap)].start[0] + 4*(math.cos(self.dataset["{}".format(imap)].start[2]*math.pi/180)))
        fypoint = (self.dataset["{}".format(imap)].start[0] + 4*(math.sin(self.dataset["{}".format(imap)].start[2]*math.pi/180)))
        #print(fxpoint, fypoint) the dir
        inidir = [[self.dataset["{}".format(imap)].start[0], self.dataset["{}".format(imap)].start[1]], [fxpoint, fypoint]]
        self.ax.plot(*np.array(line).T, color='blue', linewidth=3, solid_capstyle='round')
        self.dir = self.ax.plot(*np.array(inidir).T, color='blue', linewidth=3, solid_capstyle='round')
        self.car = self.ax.add_patch(descartes.PolygonPatch(inicar, fc='blue', alpha=0.5))
        self.ax.autoscale(enable=True, axis='both', tight=None)
        self.draw()
    def plot_car(self, list6d):
        for i in range(0, int(len(list6d[0]))):
            #self.dir[0].remove()
            self.car.remove()

            newcar = shapely.geometry.Point(list6d[0][i],list6d[1][i] ).buffer(3)
            self.car = self.ax.add_patch(descartes.PolygonPatch(newcar, fc='blue', alpha=0.5))

            self.draw()
            print("print")
            loop = QEventLoop()
            QTimer.singleShot(200, loop.quit)
            loop.exec_()

