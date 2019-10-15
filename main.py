from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, Qt

import sys

import gui
import car


class Simulator(QtWidgets.QMainWindow, gui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.__car = car.motion()
        self.populateFields()
        self.engineField.setText("0")
        self.trackVerticalProfileField.setPlainText(
            str(self.__car.track.getTrackProfile()))

    @pyqtSlot()
    def on_makeStepButton_clicked(self):
        try:
            self.__car.setThrottle(self.engineField.text())
            self.__car.makeStep()
        except:
            QtWidgets.QMessageBox.critical(self, "Error", sys.exc_info()[0])

        self.populateFields()

    @pyqtSlot()
    def on_actionAbout_triggered(self):
        self.AboutDialog = QtWidgets.QDialog()
        self.AboutDialog.ui=gui.Ui_AboutDialog()
        self.AboutDialog.ui.setupUi(self.AboutDialog)
        self.AboutDialog.setAttribute(Qt.WA_DeleteOnClose)
        self.AboutDialog.exec_()

    def populateFields(self):
        self.timeField.setText(f"{self.__car.getSimTime():.2f}")
        self.positionField.setText(f"{self.__car.getSimDistance():.2f}")
        self.speedField.setText(f"{self.__car.getSimSpeed():.2f}")
        self.fuelField.setText(f"{self.__car.getSimFuel():.2f}")

    def populateTrackProfile(self):
        trackProfile=self.__car.track.getTrackProfile()
        self.trackVerticalProfileTab.clear()

        nrows=len(trackProfile)
        self.trackVerticalProfileTab.setRowCount(nrows)
        for point in range(0,nrows):
            pass

            



if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)

    ui = Simulator()
    ui.show()

    sys.exit(app.exec_())
