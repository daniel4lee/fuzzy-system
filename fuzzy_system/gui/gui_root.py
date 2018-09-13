"""Build the tkinter gui root"""
import math
# (QWidget, QToolTip, QDesktopWidget, QPushButton, QApplication)
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QCoreApplication, QObject, QRunnable, QThread, QThreadPool, pyqtSignal, pyqtSlot
import sys
from fuzzy_system.counting.plot import PlotCanvas
from fuzzy_system.counting.run import CarRunning

THREADS = []


class GuiRoot(QWidget):
    """Root of gui."""

    def __init__(self, dataset):
        """Create GUI root with datasets dict"""
        super().__init__()
        self.threadpool = QThreadPool()
        self.setFixedSize(1000, 620)
        self.center()
        self.setWindowTitle('HW 1')
        self.show()
        self.datalist = dataset.keys()
        self.data = dataset
        self.file_run_creation(self.datalist)
        self.operation_type_creation()
        self.fuzzy_rule_setting_creation()
        self.semantic_rule_setting_creation()
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        vbox.addWidget(self.file_run)
        vbox.addWidget(self.operation_type)
        vbox.addWidget(self.rule_setting)
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
        self.radio_mamdani = QRadioButton("Mamdani")
        #self.radio_z = QRadioButton("Zadel")
        l1bg.addButton(self.radio_mamdani, 11)
        #l1bg.addButton(self.radio_z, 12)
        self.radio_mamdani.setChecked(True)
        l1_layout.addWidget(implication)
        l1_layout.addWidget(self.radio_mamdani)
        l1_layout.insertSpacing(-1, 340)
        # l1_layout.addWidget(self.radio_z)
        """Set and operation region"""
        l2_layout = QHBoxLayout()
        l2bg = QButtonGroup(self)
        and_op = QLabel("t-norms :")
        self.radio_a_m = QRadioButton("Minimum")
        #self.radio_a_a = QRadioButton("Algebraic product")
        #self.radio_a_b = QRadioButton("Bounded product")
        #self.radio_a_d = QRadioButton("Drastic Product")
        l2bg.addButton(self.radio_a_m, 21)
        #l2bg.addButton(self.radio_a_a, 22)
        #l2bg.addButton(self.radio_a_b, 23)
        #l2bg.addButton(self.radio_a_d, 24)
        self.radio_a_m.setChecked(True)
        l2_layout.addWidget(and_op)
        l2_layout.addWidget(self.radio_a_m)
        # l2_layout.addWidget(self.radio_a_a)
        # l2_layout.addWidget(self.radio_a_b)
        # l2_layout.addWidget(self.radio_a_d)
        l2_layout.insertSpacing(-1, 340)
        """Set or operation region"""
        l3_layout = QHBoxLayout()
        l3bg = QButtonGroup(self)
        or_op = QLabel("t-conorms :")
        self.radio_o_m = QRadioButton("Maximum")
        #self.radio_o_a = QRadioButton("Algebraic sum")
        #self.radio_o_b = QRadioButton("Bounded sum")
        #self.radio_o_d = QRadioButton("Drastic sum")
        l3bg.addButton(self.radio_o_m, 31)
        #l3bg.addButton(self.radio_o_a, 32)
        #l3bg.addButton(self.radio_o_b, 33)
        #l3bg.addButton(self.radio_o_d, 34)
        self.radio_o_m.setChecked(True)
        l3_layout.addWidget(or_op)
        l3_layout.addWidget(self.radio_o_m)
        # l3_layout.addWidget(self.radio_o_a)
        # l3_layout.addWidget(self.radio_o_b)
        # l3_layout.addWidget(self.radio_o_d)
        l3_layout.insertSpacing(-1, 340)
        vbox.addLayout(l1_layout)
        vbox.addLayout(l2_layout)
        vbox.addLayout(l3_layout)
        self.operation_type.setLayout(vbox)

    def semantic_rule_setting_creation(self):
        """Creat the field for setting relative value of each term set"""
        self.rule_setting = QGroupBox("Gaussian function parameter setting")
        layout = QVBoxLayout()
        self.variable_table = QTableWidget(4, 7)
        self.variable_table.setItem(1, 0, QTableWidgetItem("Front dist."))
        self.variable_table.setItem(2, 0, QTableWidgetItem("L-R dist."))
        self.variable_table.setItem(3, 0, QTableWidgetItem("Result"))

        self.variable_table.setItem(0, 1, QTableWidgetItem("mean of small"))
        self.variable_table.setItem(0, 3, QTableWidgetItem("mean of medium"))
        self.variable_table.setItem(0, 5, QTableWidgetItem("mean of large"))
        self.variable_table.setItem(0, 2, QTableWidgetItem("SD of small"))
        self.variable_table.setItem(0, 4, QTableWidgetItem("SD of medium"))
        self.variable_table.setItem(0, 6, QTableWidgetItem("SD of large"))
        """fill the table"""
        self.values = []
        for i in range(9):
            self.mean = QDoubleSpinBox()
            self.mean.setRange(-100, 100)

            self.sd = QDoubleSpinBox()
            self.sd.setDecimals(3)
            self.sd.setValue(5)
            self.sd.setMinimum(0.1)
            self.sd.setToolTip("The standard deviation value for "
                               "Gaussian function.")
            self.values.append(self.mean)
            self.values.append(self.sd)
        z = 0
        self.values[0].setValue(3)
        self.values[0].setToolTip(
            "The mean for monotonically decreasing Gaussian function.")
        self.values[1].setValue(10)
        self.values[2].setValue(12)
        self.values[2].setToolTip("The mean for Gaussian function.")
        self.values[4].setValue(20)
        self.values[4].setToolTip(
            "The mean for monotonically increasing Gaussian function.")

        self.values[6].setValue(-8)
        self.values[8].setValue(0)
        self.values[10].setValue(6)
        self.values[11].setValue(3)
        self.values[6].setToolTip(
            "The mean for monotonically decreasing Gaussian function.")
        self.values[8].setToolTip("The mean for Gaussian function.")
        self.values[10].setToolTip(
            "The mean for monotonically increasing Gaussian function.")

        self.values[12].setValue(-10)
        self.values[13].setValue(20)
        self.values[14].setValue(0)
        self.values[15].setValue(21)
        self.values[16].setValue(13)
        self.values[17].setValue(18)

        self.values[12].setToolTip(
            "The mean for monotonically decreasing Gaussian function.")
        self.values[14].setToolTip("The mean for Gaussian function.")
        self.values[16].setToolTip(
            "The mean for monotonically increasing Gaussian function.")

        for q in range(1, 4):
            for i in range(1, 7, 2):
                self.variable_table.setCellWidget(q, i, self.values[z])
                z += 1
                self.variable_table.setCellWidget(q, i+1, self.values[z])
                z += 1
        self.variable_table.verticalHeader().setVisible(False)
        self.variable_table.horizontalHeader().setVisible(False)
        self.variable_table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.variable_table)
        self.rule_setting.setLayout(layout)

    def fuzzy_rule_setting_creation(self):
        """ Creat the field for setting fuzzy rule"""
        self.fuzzy_rules = QGroupBox("Fuzzy rules setting")
        layout = QVBoxLayout()
        self.table = QTableWidget(3, 10)
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
        self.sml_l = []
        for i in range(9):
            sml = QComboBox()
            sml.addItem("small")
            sml.addItem("medium")
            sml.addItem("large")
            self.sml_l.append(sml)
            self.table.setCellWidget(2, 1+i, self.sml_l[i])
        self.sml_l[0].setCurrentIndex(2)
        self.sml_l[1].setCurrentIndex(2)
        self.sml_l[3].setCurrentIndex(2)
        self.sml_l[4].setCurrentIndex(1)
        self.sml_l[6].setCurrentIndex(2)
        self.sml_l[7].setCurrentIndex(1)
        self.table.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setVisible(False)
        layout.addWidget(self.table)
        self.fuzzy_rules.setLayout(layout)

    def file_changed(self):
        """
        plot new map
        """
        self.m.plot_map(self.file_choose.currentText())

    def run(self):
        text = self.file_choose.currentText()
        #checked_op = []
        # if self.radio_mamdani.isChecked():
        # checked_op.append('1d')
        selected_fuzzy = []
        for i in range(9):
            selected_fuzzy.append(self.sml_l[i].currentText())
        gaussian_function_variable = []
        for i in range(18):
            gaussian_function_variable.append(self.values[i].value())
        car = CarRunning(self.data, text, selected_fuzzy,
                         gaussian_function_variable)
        car.signals.result.connect(self.plot_output)

        self.file_choose.setDisabled(True)
        self.run_btn.setDisabled(True)
        self.radio_mamdani.setDisabled(True)
        self.radio_a_m.setDisabled(True)
        self.radio_o_m.setDisabled(True)
        for i in range(9):
            self.sml_l[i].setDisabled(True)
        for i in range(18):
            self.values[i].setDisabled(True)

        self.threadpool.start(car)

    def plot_output(self, s):

        self.m.plot_car(s)

        self.file_choose.setDisabled(False)
        self.run_btn.setDisabled(False)
        self.radio_mamdani.setDisabled(False)
        self.radio_a_m.setDisabled(False)
        self.radio_o_m.setDisabled(False)
        for i in range(9):
            self.sml_l[i].setDisabled(False)
        for i in range(18):
            self.values[i].setDisabled(False)

    def center(self):
        """Place window in the center"""
        qr = self.frameGeometry()
        central_p = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(central_p)
        self.move(qr.topLeft())


if __name__ == '__main__':
    print("Error: This file can only be imported. Execute 'main.py'")
