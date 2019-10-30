from PyQt5 import QtWidgets
from PyQt5.QtCore import *

import os, sys

import serial.tools.list_ports

import gui
import car

_translate = QCoreApplication.translate

class Simulator(QtWidgets.QMainWindow, gui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.__car = car.motion()
        self.populateFields()
        self.engineField.setText("0")

        self.__car.param.fromJSON(car.defaultParams())

    @pyqtSlot()
    def on_makeStepButton_clicked(self):
        try:
            self.__car.setThrottle(self.engineField.text())
            self.__car.makeStep()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, _translate("Dialog","Error"), str(e))

        self.populateFields()

    @pyqtSlot()
    def on_actionAbout_triggered(self):
        self.AboutDialog = QtWidgets.QDialog()
        self.AboutDialog.ui = gui.Ui_AboutDialog()
        self.AboutDialog.ui.setupUi(self.AboutDialog)
        self.AboutDialog.setAttribute(Qt.WA_DeleteOnClose)
        self.AboutDialog.exec_()

    def populateFields(self):
        self.timeField.setText(f"{self.__car.getSimTime():.2f}")
        self.positionField.setText(f"{self.__car.getSimDistance():.2f}")
        self.speedField.setText(f"{self.__car.getSimSpeed():.2f}")
        self.fuelField.setText(f"{self.__car.getSimFuel():.2f}")

    @pyqtSlot()
    def on_actionExport_Settings_triggered(self):
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, _translate("Dialog","Save Config"), ".", filter=_translate("Dialog","Config Files (*.json)")+";;"+_translate("Dialog","All Files(*.*)"))
        if filename:
            fp = open(filename, 'w')
            self.__car.param.toJSON(file=fp)
            fp.close()

    @pyqtSlot()
    def on_actionImport_Settings_triggered(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, _translate("Dialog","Open Config"), ".", filter=_translate("Dialog","Config Files (*.json)")+";;"+_translate("Dialog","All Files(*.*)"))
        if filename:
            fp = open(filename, 'r')
            self.__car.param.fromJSON(fp)
            fp.close()
    
    @pyqtSlot()
    def on_refreshAvailablePorts_clicked(self):
        ports = serial.tools.list_ports.comports()
        for port, desc, hwid in sorted(ports):
            self.availablePorts.addItem("{}: {}".format(port, desc))

    

if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)

    if len(sys.argv)>1:
        translator = QTranslator()
        translator.load('carSim_'+ sys.argv[1], 'lang')
        app.installTranslator(translator)
    

    ui = Simulator()
    ui.show()

    sys.exit(app.exec_())
