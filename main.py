from PyQt5 import QtWidgets
from PyQt5.QtCore import *

import os
import sys

import serial.tools.list_ports
import can

import gui
import car

import time

_translate = QCoreApplication.translate


class Simulator(QtWidgets.QMainWindow, gui.Ui_MainWindow):
    def __init__(self):
        super().__init__()

        self.__car = car.motion()
        self.__car.param.fromJSON(car.defaultParams())

        self.__translator = QTranslator(self)

        self.setupUi(self)
        self.populateFields()
        self.engineField.setText("1")

        for file in os.listdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lang')):
            if file.startswith('carSim_') and file.endswith('.qm'):
                self.langSelector.addItem(file[7:-3])

    def changeEvent(self, event):
        if event.type() == QEvent.LanguageChange:
            self.retranslateUi(self)
        super().changeEvent(event)

    @pyqtSlot(str)
    def on_langSelector_currentTextChanged(self, lang):
        if lang:
            self.__translator.load(QLocale(lang), 'carSim', '_', 'lang', '.qm')
            QtWidgets.QApplication.instance().installTranslator(self.__translator)
        else:
            QtWidgets.QApplication.instance().removeTranslator(self.__translator)

    @pyqtSlot()
    def on_makeStepButton_clicked(self):
        try:
            # self.__car.setThrottle(self.engineField.text())
            self.__car.makeStep()
            motionMessage=can.Message(arbitration_id=18,is_extended_id=False,data=self.__car.getCanBytes()[:])
            print(motionMessage)
            self.__canbus.send(motionMessage)
        except Exception as e:
            QtWidgets.QMessageBox.critical(
                self, _translate("Dialog", "Error"), str(e))

        self.populateFields()

    def populateFields(self):
        self.timeField.setText(f"{self.__car.getSimTime():.2f}")
        self.positionField.setText(f"{self.__car.getSimDistance():.2f}")
        self.speedField.setText(f"{self.__car.getSimSpeed():.2f}")
        self.fuelField.setText(f"{self.__car.getSimFuel():.2f}")
        self.engineField.setText(f"{self.__car.getThrottle():.2f}")

    @pyqtSlot()
    def on_actionAbout_triggered(self):
        self.AboutDialog = QtWidgets.QDialog()
        self.AboutDialog.ui = gui.Ui_AboutDialog()
        self.AboutDialog.ui.setupUi(self.AboutDialog)
        self.AboutDialog.setAttribute(Qt.WA_DeleteOnClose)
        self.AboutDialog.exec_()

    @pyqtSlot()
    def on_actionExport_Settings_triggered(self):
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, _translate("Dialog", "Save Config"), ".", filter=_translate("Dialog", "Config Files (*.json)")+";;"+_translate("Dialog", "All Files(*.*)"))
        if filename:
            fp = open(filename, 'w')
            self.__car.param.toJSON(file=fp)
            fp.close()

    @pyqtSlot()
    def on_actionImport_Settings_triggered(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, _translate("Dialog", "Open Config"), ".", filter=_translate("Dialog", "Config Files (*.json)")+";;"+_translate("Dialog", "All Files(*.*)"))
        if filename:
            fp = open(filename, 'r')
            self.__car.param.fromJSON(fp)
            fp.close()

    @pyqtSlot()
    def on_refreshAvailablePorts_clicked(self):
        ports = serial.tools.list_ports.comports()
        self.availablePorts.clear()
        for port, desc, hwid in sorted(ports):
            self.availablePorts.addItem(desc, port)

    @pyqtSlot(bool)
    def on_connectPort_clicked(self, state):
        if state:
            try:
                self.__canbus = car.myCan(self.availablePorts.currentData())
            except Exception as e:
                self.connectPort.setChecked(False)
                QtWidgets.QMessageBox.critical(
                    self, _translate("Dialog", "Error"), str(e))
            else:
                self.connectPort.setText(
                    _translate("MainWindow", "Disconnect"))
                self.canInterfaceTypes.setEnabled(False)
                self.availablePorts.setEnabled(False)
                self.refreshAvailablePorts.setEnabled(False)


        else:
            self.connectPort.setText(_translate("MainWindow", "Connect"))
            del(self.__canbus)
            self.canInterfaceTypes.setEnabled(True)
            self.availablePorts.setEnabled(True)
            self.refreshAvailablePorts.setEnabled(True)
    
    @pyqtSlot(bool)
    def on_simulationStart_clicked(self,state):
        if state:
            self.__ticker = QTimer(self)
            self.__ticker.setInterval(100)
            self.__ticker.timeout.connect(self.on_makeStepButton_clicked)
            self.__ticker.start()
            self.__car.setThrottle(1)
            self.simulationStart.setText(_translate("MainWindow","Stop Simulation!"))
            lapData=1

        else:
            self.__ticker.stop()
            self.simulationStart.setText(_translate("MainWindow","Start Simulation!"))
            lapData=0
        
        lapMessage=can.Message(arbitration_id=32,is_extended_id=False,data=[lapData])
        print(lapMessage)
        self.__canbus.send(lapMessage)




if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)

    ui = Simulator()
    ui.show()

    sys.exit(app.exec_())
