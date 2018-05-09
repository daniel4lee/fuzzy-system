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


c = shapely.geometry.Point(1,1).buffer(1)


fig = Figure(figsize=(5,5), dpi=90)
ring_mixed = shapely.geometry.LineString([(0, 0), (0, 2), (1, 1),
    (2, 2), (2, 0), (1, 0.8), (0, 0)])
ax = fig.add_subplot(111)
ax.plot(*np.array(ring_mixed).T, color='blue', linewidth=3, solid_capstyle='round')
ax.add_patch(descartes.PolygonPatch(c, fc='blue', alpha=0.5))
ax.set_title('General Polygon')
xrange = [-1, 3]
yrange = [-1, 3]
ax.set_xlim(*xrange)
ax.set_ylim(*yrange)
ax.set_aspect(1)
i = c.intersection(ring_mixed)
print(i)
ax.draw()
#print i.geoms[1].coords[0]