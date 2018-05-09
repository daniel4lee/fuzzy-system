"""Build the tkinter gui root"""
import math
from PyQt5.QtWidgets import *#(QWidget, QToolTip, QDesktopWidget, QPushButton, QApplication)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QCoreApplication, QObject, QRunnable, QThread, QThreadPool, pyqtSignal, pyqtSlot 
import sys
from plot import PlotCanvas
from run import CarRunning

THREADS = []

class GuiRoot(QWidget):
    """Root of gui."""
    def __init__(self, dataset):
        """Create GUI root with datasets dict"""
        super().__init__()
        self.threadpool = QThreadPool()
        self.setFixedSize(1000, 600)
        self.center()
        self.setWindowTitle('HW 1')      
        self.show()
        self.datalist = dataset.keys()
        self.data = dataset
        self.file_run_creation(self.datalist)
        self.operation_type_creation()
        self.fuzzy_rule_setting_creation()
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        vbox.addWidget(self.file_run)
        vbox.addWidget(self.operation_type)
        vbox.addWidget(self.fuzzy_rules)
        hbox.addLayout(vbox)
        self.m = PlotCanvas(self.data)
        hbox.addWidget(self.m)
        self.setLayout(hbox)

    def file_run_creation(self, datalist):
        self.file_run = QGroupBox("File choose")
        layout = QGridLayout()
        layout.setSpacing(10)
        self.file_choose = QComboBox()
        for i in datalist:
            self.file_choose.addItem("{}".format(i))
        self.file_choose.currentTextChanged.connect(self.file_changed)
        self.run_btn = QPushButton("Start", self)
        self.run_btn.clicked.connect(self.run)
        layout.addWidget(self.file_choose, 1, 0, 1, 3)
        layout.addWidget(self.run_btn, 1, 3, 1, 1)
        self.file_run.setLayout(layout)
    
    def operation_type_creation(self):
        """Operation field"""
        self.operation_type = QGroupBox("Operation type")
        vbox = QVBoxLayout()
        """set implication region"""
        l1bg = QButtonGroup(self)
        l1_layout = QHBoxLayout()
        implication = QLabel("Implication :")
        self.radio_d = QRadioButton("Dienes-Rescher")
        self.radio_z = QRadioButton("Zadel")
        l1bg.addButton(self.radio_d, 11)
        l1bg.addButton(self.radio_z, 12)
        self.radio_d.setChecked(True)
        l1_layout.addWidget(implication)
        l1_layout.addWidget(self.radio_d)
        l1_layout.addWidget(self.radio_z)
        """Set and operation region"""
        l2_layout = QHBoxLayout()
        l2bg = QButtonGroup(self)
        and_op = QLabel("AND operation :")
        self.radio_a_m = QRadioButton("Minimum")
        self.radio_a_a = QRadioButton("Algebraic product")
        self.radio_a_b = QRadioButton("Bounded product")
        self.radio_a_d = QRadioButton("Drastic Product")
        l2bg.addButton(self.radio_a_m, 21)
        l2bg.addButton(self.radio_a_a, 22)
        l2bg.addButton(self.radio_a_b, 23)
        l2bg.addButton(self.radio_a_d, 24)
        self.radio_a_m.setChecked(True)
        l2_layout.addWidget(and_op)
        l2_layout.addWidget(self.radio_a_m)
        l2_layout.addWidget(self.radio_a_a)
        l2_layout.addWidget(self.radio_a_b)
        l2_layout.addWidget(self.radio_a_d)
        """Set or operation region"""
        l3_layout = QHBoxLayout()
        l3bg = QButtonGroup(self)
        or_op = QLabel("OR operation :")
        self.radio_o_m = QRadioButton("Minimum")
        self.radio_o_a = QRadioButton("Algebraic sum")
        self.radio_o_b = QRadioButton("Bounded sum")
        self.radio_o_d = QRadioButton("Drastic sum")
        l3bg.addButton(self.radio_o_m, 31)
        l3bg.addButton(self.radio_o_a, 32)
        l3bg.addButton(self.radio_o_b, 33)
        l3bg.addButton(self.radio_o_d, 34)
        self.radio_o_m.setChecked(True)
        l3_layout.addWidget(or_op)
        l3_layout.addWidget(self.radio_o_m)
        l3_layout.addWidget(self.radio_o_a)
        l3_layout.addWidget(self.radio_o_b)
        l3_layout.addWidget(self.radio_o_d)

        vbox.addLayout(l1_layout)
        vbox.addLayout(l2_layout)
        vbox.addLayout(l3_layout)
        self.operation_type.setLayout(vbox)
        
    def semantic_rule_setting_creation(self):
        """Creat the field for setting relative value of each term set"""
        self.rule_setting = QGroupBox("rule parameter setting")
    def fuzzy_rule_setting_creation(self):
        """ Creat the field for setting fuzzy rule"""
        self.fuzzy_rules = QGroupBox("Fuzzy rules setting")
        layout = QVBoxLayout()
        self.table =QTableWidget(3,10)
        self.table.setItem(0, 0, QTableWidgetItem("Front dist."))
        self.table.setItem(1, 0, QTableWidgetItem("L-R dist."))
        self.table.setItem(2, 0, QTableWidgetItem("Result"))
        """fill the table"""
        for i in range(3):
            self.table.setItem(1, 1+(i*3), QTableWidgetItem("small"))
            self.table.setItem(0, 1+i, QTableWidgetItem("small"))
            self.table.setItem(1, 2+(i*3), QTableWidgetItem("medium"))
            self.table.setItem(0, 4+i, QTableWidgetItem("medium"))
            self.table.setItem(1, 3+(i*3), QTableWidgetItem("large"))
            self.table.setItem(0, 7+i, QTableWidgetItem("large"))
        self.sml_l=[]
        for i in range(9):
            sml = QComboBox()
            sml.addItem("small")
            sml.addItem("medium")
            sml.addItem("large")
            self.sml_l.append(sml)
            self.table.setCellWidget(2, 1+i, self.sml_l[i])
        layout.addWidget(self.table)
        self.fuzzy_rules.setLayout(layout)

    def file_changed(self):
        """print map"""
        self.m.plot_map(self.file_choose.currentText())
    def run(self):
        text = self.file_choose.currentText()
        checked_op = []
        if self.radio_d.isChecked():
            checked_op.append('1d')
        elif self.radio_z.isChecked():
            checked_op.append('1z')
        if self.radio_a_m.isChecked():
            checked_op.append("2m")
        elif self.radio_a_a.isChecked():
            checked_op.append("2a")
        elif self.radio_a_b.isChecked():
            checked_op.append("2b")
        elif self.radio_a_d.isChecked():
            checked_op.append("2d") 
        if self.radio_o_m.isChecked():
            checked_op.append("3m")
        elif self.radio_o_a.isChecked():
            checked_op.append("3a")
        elif self.radio_o_b.isChecked():
            checked_op.append("3b")
        elif self.radio_o_d.isChecked():
            checked_op.append("3d")
        selected_fuzzy = []
        for i in range(9):
            selected_fuzzy.append(self.sml_l[i].currentText())
        car = CarRunning(checked_op, selected_fuzzy, self.data, text)
        car.signals.result.connect(self.plot_output)
        self.threadpool.start(car)
    def plot_output(self, s):
        self.m.plot_car(s)
    def center(self):
        """Place window in the center"""
        qr = self.frameGeometry()
        central_p = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(central_p)
        self.move(qr.topLeft())
    def exit(self):
        """Stop threads and destroy gui"""
        for thread in THREADS:
            thread.stop()
        self.after(500, self.destroy)


if __name__ == '__main__':
    print("Error: This file can only be imported. Execute 'main.py'")
