from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot
import gui

import car


class Simulator(QtWidgets.QMainWindow, gui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.__car = car.motion()
        self.populateFields()
        self.engineField.setText("0")
        self.trackVerticalProfileField.setPlainText(str(self.__car.getSimTrackProfile()))

    @pyqtSlot()
    def on_makeStepButton_clicked(self):
        try:
            self.__car.setThrottle(self.engineField.text())
            self.__car.makeStep()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", str(e))

        self.populateFields()

    def populateFields(self):
        self.timeField.setText(f"{self.__car.getSimTime():.2f}")
        self.positionField.setText(f"{self.__car.getSimDistance():.2f}")
        self.speedField.setText(f"{self.__car.getSimSpeed():.2f}")
        self.fuelField.setText(f"{self.__car.getSimFuel():.2f}")


if __name__ == "__main__":

    import sys
    app = QtWidgets.QApplication(sys.argv)

    ui = Simulator()
    ui.show()

    sys.exit(app.exec_())
