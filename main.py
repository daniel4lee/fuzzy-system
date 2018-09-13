"""
the main excution file
"""
import os
from os.path import join, isfile
from collections import namedtuple
import sys
from PyQt5.QtWidgets import QApplication
from fuzzy_system.gui.gui_root import GuiRoot
def main():
    """Read data as dictionary"""
    app = QApplication(sys.argv)
    gui_root = GuiRoot(read_file())
    sys.exit(app.exec_())
def read_file():
    """Read txt file in same location"""
    road_map = namedtuple('road_map', ['start', 'x', 'y'])
    datapath = join(os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__))), "data")
    folderfiles = os.listdir(datapath)
    dataset = {}
    paths = (join(datapath, f) for f in folderfiles if isfile(join(datapath, f)))
    for idx, content in enumerate(list(map(lambda path: open(path, 'r'), paths))):
        i = 0
        for line in content:
            if i == 0:
                dataset[folderfiles[idx]] = road_map(list(map(float, line.split(','))), [], [])
            else:
                dataset[folderfiles[idx]].x.append(float(line.split(',')[0]))
                dataset[folderfiles[idx]].y.append(float(line.split(',')[1]))
            i += 1
    return dataset

if __name__ == '__main__':
    main()
