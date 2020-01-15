from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtChart import QChart, QLineSeries

import os
import sys

import serial.tools.list_ports
#import can

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

        self.positionChart = QChart()
        self.positionSeries = QLineSeries()        

        self.speedChart = QChart()
        self.speedSeries = QLineSeries()

        self.fuelChart = QChart()
        self.fuelSeries = QLineSeries()

        self.engineChart = QChart()
        self.engineSeries = QLineSeries()

        self.positionChart.addSeries(self.positionSeries)
        self.speedChart.addSeries(self.speedSeries)
        self.fuelChart.addSeries(self.fuelSeries)
        self.engineChart.addSeries(self.engineSeries)

        self.positionChart.legend().hide()
        self.speedChart.legend().hide()
        self.fuelChart.legend().hide()
        self.engineChart.legend().hide()   

        self.positionChart.createDefaultAxes()
        self.speedChart.createDefaultAxes()
        self.fuelChart.createDefaultAxes()
        self.engineChart.createDefaultAxes()
        
        self.positionChart.setTitle("Position")
        self.speedChart.setTitle("Speed")
        self.fuelChart.setTitle("Fuel")
        self.engineChart.setTitle("Engine")

        self.positionChart.setMargins(QMargins())
        self.speedChart.setMargins(QMargins())
        self.fuelChart.setMargins(QMargins())
        self.engineChart.setMargins(QMargins())

        self.positionChartW.setChart(self.positionChart)
        self.speedChartW.setChart(self.speedChart)
        self.fuelChartW.setChart(self.fuelChart)
        self.engineChartW.setChart(self.engineChart)

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
    def on_resetSimulationButton_clicked(self):
        self.__car = car.motion()
        self.__car.param.fromJSON(car.defaultParams())

        self.positionSeries = QLineSeries()
        self.speedSeries = QLineSeries()
        self.fuelSeries = QLineSeries()
        self.engineSeries = QLineSeries()

        self.populateFields()

    @pyqtSlot()
    def on_makeStepButton_clicked(self):
        try:
            # self.__car.setThrottle(self.engineField.text())
            self.__car.makeStep()
            # motionMessage=can.Message(arbitration_id=18,is_extended_id=False,data=self.__car.getCanBytes()[:])
            motionMessage = car.canMsg(
                StdId=18, Data=self.__car.getCanBytes()[:])
            print(motionMessage)
            self.__canbus.sendMsg(motionMessage)
            with open('log.dat', 'a') as outfile:
                outfile.write("%.1f\t%f\t%f\t%f\n" % (self.__car.getSimTime(),
                                                      self.__car.getSimDistance(), self.__car.getSimSpeed(), self.__car.getSimFuel()))
        except Exception as e:
            QtWidgets.QMessageBox.warning(
                self, _translate("Dialog", "Error"), str(e))

        self.populateFields()
        if float(self.timeField.text()) >= 240:
            if self.simulationStart.isChecked() == True:
                self.simulationStart.click()

    def populateFields(self):
        self.timeField.setText(f"{self.__car.getSimTime():.2f}")
        self.positionField.setText(f"{self.__car.getSimDistance():.2f}")
        self.speedField.setText(f"{self.__car.getSimSpeed():.2f}")
        self.fuelField.setText(f"{self.__car.getSimFuel():.2f}")
        self.engineField.setText(f"{self.__car.getThrottle():.2f}")

        xax = self.positionChart.axisX()

        if(self.__car.getSimTime()>self.positionChart.axisX().max()):
            self.positionChart.axisX().setMax(self.__car.getSimTime())
            self.speedChart.axisX().setMin(self.__car.getSimTime())
            self.fuelChart.axisX().setMin(self.__car.getSimTime())
            self.engineChart.axisX().setMin(self.__car.getSimTime())
        elif(self.__car.getSimTime()<self.positionChart.axisX().min()):
            self.positionChart.axisX().setMin(self.__car.getSimTime())
            self.speedChart.axisX().setMin(self.__car.getSimTime())
            self.fuelChart.axisX().setMin(self.__car.getSimTime())
            self.engineChart.axisX().setMin(self.__car.getSimTime())

        if(self.__car.getSimSpeed()>self.speedChart.axisY().max()):
            self.speedChart.axisY().setMax(self.__car.getSimSpeed())
        elif(self.__car.getSimSpeed()<self.speedChart.axisY().min()):
            self.speedChart.axisY().setMin(self.__car.getSimSpeed())

        if(self.__car.getSimFuel()>self.fuelChart.axisY().max()):
            self.fuelChart.axisY().setMax(self.__car.getSimFuel())
        elif(self.__car.getSimFuel()<self.fuelChart.axisY().min()):
            self.fuelChart.axisY().setMin(self.__car.getSimFuel())

        self.positionSeries.append(self.__car.getSimTime(),self.__car.getSimDistance())
        self.speedSeries.append(self.__car.getSimTime(),self.__car.getSimSpeed())
        self.fuelSeries.append(self.__car.getSimTime(),self.__car.getSimFuel())
        self.engineSeries.append(self.__car.getSimTime(),self.__car.getThrottle())



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
                self.__canbus = car.myCan(self.availablePorts.currentData(), [
                                          self.canReceived.appendPlainText], [
                                          self.__car.setSwitchingPoint], loopTime=0.025)
                self.__watch = QTimer(self)
                self.__watch.setInterval(1000)
                self.__watch.timeout.connect(self.syncTime)
                self.__watch.start()
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
            del(self.__watch)
            self.canInterfaceTypes.setEnabled(True)
            self.availablePorts.setEnabled(True)
            self.refreshAvailablePorts.setEnabled(True)

    @pyqtSlot()
    def syncTime(self):
        self.__canbus.sendMsg(car.canMsg(StdId=0, Data=int(
            self.__car.getSimTime()*1000.0).to_bytes(4, 'little')))

    @pyqtSlot(bool)
    def on_simulationStart_clicked(self, state):
        if state:
            self.__ticker = QTimer(self)
            self.__ticker.setInterval(100)
            self.__ticker.timeout.connect(self.on_makeStepButton_clicked)
            self.__ticker.start()
            self.__car.setThrottle(1)
            self.simulationStart.setText(
                _translate("MainWindow", "Stop Simulation!"))
            lapData = 1
            with open('log.dat', 'a') as outfile:
                outfile.write("%.1f\t%f\t%f\t%f\n" % (self.__car.getSimTime(),
                                                      self.__car.getSimDistance(), self.__car.getSimSpeed(), self.__car.getSimFuel()))
        

        else:
            self.__ticker.stop()
            self.simulationStart.setText(
                _translate("MainWindow", "Start Simulation!"))
            lapData = 0

        lapMessage = car.canMsg(StdId=32, Data=[lapData])
        print(lapMessage)
        self.__canbus.sendMsg(lapMessage)


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)

    ui = Simulator()
    ui.show()

    sys.exit(app.exec_())
