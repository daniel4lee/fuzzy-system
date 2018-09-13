import os
from os.path import join, isfile

import math
import numpy as np
# (QWidget, QToolTip, QDesktopWidget, QPushButton, QApplication)
from PyQt5.QtWidgets import *
from PyQt5.QtCore import*
import matplotlib.style
from matplotlib.lines import Line2D
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
        self.ax.axis('equal')
        super().__init__(fig)
        self.dataset = dataset
        FigureCanvas.setSizePolicy(
            self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        imap = list(self.dataset.keys())[0]
        self.car = None
        self.dir = None
        self.car_trace = []
        self.plot_map(imap)

    def plot_map(self, imap):
        self.ax.clear()

        # creating end area polygon for drawing
        ea = []
        ea.append((self.dataset["{}".format(imap)].x[0],
                   self.dataset["{}".format(imap)].y[0]))
        ea.append((self.dataset["{}".format(imap)].x[0],
                   self.dataset["{}".format(imap)].y[1]))
        ea.append((self.dataset["{}".format(imap)].x[1],
                   self.dataset["{}".format(imap)].y[1]))
        ea.append((self.dataset["{}".format(imap)].x[1],
                   self.dataset["{}".format(imap)].y[0]))
        end_area = shapely.geometry.Polygon(ea)

        # creating map line for drawing
        verts = []
        for i in range(2, len(self.dataset["{}".format(imap)].x)):
            verts.append([self.dataset["{}".format(imap)].x[i],
                          self.dataset["{}".format(imap)].y[i]])
        map_line = shapely.geometry.LineString(verts)

        # initial car and dir line
        inicar = shapely.geometry.Point(self.dataset["{}".format(
            imap)].start[0], self.dataset["{}".format(imap)].start[1]).buffer(3)
        self.dir_point = (4*(math.cos(self.dataset["{}".format(imap)].start[2]*math.pi/180)),
                          4*(math.sin(self.dataset["{}".format(imap)].start[2]*math.pi/180)))
        self.car_center = (self.dataset["{}".format(
            imap)].start[0], self.dataset["{}".format(imap)].start[1])

        # plot on figurecanvas
        self.ax.plot(*np.array(map_line).T, color='k',
                     linewidth=3, solid_capstyle='round')
        self.ax.add_patch(descartes.PolygonPatch(
            end_area, fc='red', alpha=0.7))

        self.dir = self.ax.arrow(
            *self.car_center, *self.dir_point, head_width=1, head_length=1, fc='gold', ec='k')
        self.car = self.ax.add_patch(
            descartes.PolygonPatch(inicar, fc='royalblue', alpha=0.5))
        self.ax.autoscale(enable=True, axis='both', tight=None)
        self.draw()

    def plot_car(self, list9d):
        try:
            self.dir.remove()
            self.car.remove()
        except ValueError:
            pass
        # represent that it arrived the end area, hence output an txt file
        if (len(list9d[0]) != len(list9d[1])):
            '''outpath = join(os.path.realpath(os.path.join(
                os.getcwd(), os.path.dirname(__file__))), "train4D.txt")'''
            with open("train4D.txt", "w") as fp:
                for i in range(0, int(len(list9d[0]))):
                    s = ''
                    for j in range(2, 6):
                        if j == 5:
                            s = s + str('{:.7f}'.format(list9d[j][i]))
                        else:
                            s = s + str('{:.7f}'.format(list9d[j][i])) + ' '
                    fp.write(s+'\n')
        if (len(list9d[0]) != len(list9d[1])):
            '''outpath = join(os.path.realpath(os.path.join(
                os.getcwd(), os.path.dirname(__file__))), "train6D.txt")'''
            with open("train6D.txt", "w") as fp:
                for i in range(0, int(len(list9d[0]))):
                    s = ''
                    for j in range(6):
                        if j == 5:
                            s = s + str('{:.7f}'.format(list9d[j][i]))
                        else:
                            s = s + str('{:.7f}'.format(list9d[j][i])) + ' '
                    fp.write(s+'\n')

        # produce the animation according to the trace9d log

        for i in range(0, len(list9d[0])):
            if (len(list9d[0]) != len(list9d[1])) and (i+1 == len(list9d[0])):
                self.car_center = (list9d[0][i], list9d[1][i])
                newcar = shapely.geometry.Point(*self.car_center).buffer(3)
                self.car = self.ax.add_patch(
                    descartes.PolygonPatch(newcar, fc='lime', alpha=0.8))

            elif (len(list9d[0]) == len(list9d[1])) and (i+1 == len(list9d[0])):
                self.car_center = (list9d[0][i], list9d[1][i])
                newcar = shapely.geometry.Point(*self.car_center).buffer(3)
                self.car = self.ax.add_patch(
                    descartes.PolygonPatch(newcar, fc='r', alpha=1))
            else:
                self.car_center = (list9d[0][i], list9d[1][i])
                newcar = shapely.geometry.Point(*self.car_center).buffer(3)
                self.car = self.ax.add_patch(
                    descartes.PolygonPatch(newcar, fc='royalblue', alpha=0.5))

            self.dir_point = (
                4*(math.cos(math.radians(list9d[9][i]))), 4*(math.sin(math.radians(list9d[9][i]))))
            self.dir = self.ax.arrow(
                *self.car_center, *self.dir_point, head_width=1, head_length=1, fc='gold', ec='k')

            front_point = (self.car_center[0] + 3*(math.cos(math.radians(list9d[9][i]))),
                           self.car_center[1] + 3*(math.sin(math.radians(list9d[9][i]))))
            front_line = self.ax.plot([front_point[0], list9d[6][i][0]], [
                                      front_point[1], list9d[6][i][1]], linestyle='--', color='navy')

            right_point = (self.car_center[0] + 3*(math.cos(math.radians(list9d[9][i]-45))),
                           self.car_center[1] + 3*(math.sin(math.radians(list9d[9][i]-45))))
            right_line = self.ax.plot([right_point[0], list9d[7][i][0]], [
                                      right_point[1], list9d[7][i][1]], linestyle='--', color='navy')

            left_point = (self.car_center[0] + 3*(math.cos(math.radians(list9d[9][i]+45))),
                          self.car_center[1] + 3*(math.sin(math.radians(list9d[9][i]+45))))
            left_line = self.ax.plot([left_point[0], list9d[8][i][0]], [
                                     left_point[1], list9d[8][i][1]], linestyle='--', color='navy')

            self.trace = shapely.geometry.Point(*self.car_center).buffer(0.1)
            self.car_trace.append(self.ax.add_patch(
                descartes.PolygonPatch(self.trace, fc='grey', alpha=0.5)))
            self.draw()

            front_line[0].remove()
            right_line[0].remove()
            left_line[0].remove()
            self.dir.remove()
            self.car.remove()

            if(i+1 == len(list9d[0])):
                for p in self.car_trace:
                    p.remove()
                self.car_trace.clear()
            loop = QEventLoop()
            QTimer.singleShot(20, loop.quit)
            loop.exec_()
