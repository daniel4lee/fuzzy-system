import math
import numpy as np
from PyQt5.QtWidgets import *#(QWidget, QToolTip, QDesktopWidget, QPushButton, QApplication)

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.path import Path
import matplotlib.patches as patches

import shapely.geometry
import descartes
class PlotCanvas(FigureCanvas):
 
    def __init__(self, dataset={}):
        fig = Figure(figsize=(8, 8), dpi=100)
        self.ax = fig.add_subplot(111)
        FigureCanvas.__init__(self, fig)
        self.dataset = dataset
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        imap = list(self.dataset.keys())[0]
        self.plot(imap)
    def plot(self, imap):
        verts = []
        for i in range(2, len(self.dataset["{}".format(imap)].x)):
                verts.append([self.dataset["{}".format(imap)].x[i], self.dataset["{}".format(imap)].y[i]])
        line = shapely.geometry.LineString(verts)
        car = shapely.geometry.Point(self.dataset["{}".format(imap)].start[0], self.dataset["{}".format(imap)].start[1]).buffer(3)
        fxpoint = (self.dataset["{}".format(imap)].start[0] + 4*(math.cos(self.dataset["{}".format(imap)].start[2]*math.pi/180)))
        fypoint = (self.dataset["{}".format(imap)].start[0] + 4*(math.sin(self.dataset["{}".format(imap)].start[2]*math.pi/180)))
        print(fxpoint, fypoint)
        fline = [[self.dataset["{}".format(imap)].start[0], self.dataset["{}".format(imap)].start[1]], [fxpoint, fypoint]]
        self.ax.plot(*np.array(line).T, color='blue', linewidth=3, solid_capstyle='round')
        self.ax.plot(*np.array(fline).T, color='blue', linewidth=3, solid_capstyle='round')
        self.ax.add_patch(descartes.PolygonPatch(car, fc='blue', alpha=0.5))
        self.ax.autoscale(enable=True, axis='both', tight=None)
        self.draw()
