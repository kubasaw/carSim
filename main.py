from PyQt5 import QtWidgets
from PyQt5.QtCore import pyqtSlot, Qt, QSortFilterProxyModel, QRect, QItemSelectionModel

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
        self.proxyTrackModel = QSortFilterProxyModel()
        self.proxyTrackModel.setSourceModel(
            car.guiConnector.tableGuiConnector(self.__car.track.getTrackProfile()))
        self.trackVerticalProfileTab.setModel(self.proxyTrackModel)
        #self.trackVerticalProfileTab.sortByColumn(0,Qt.AscendingOrder)
        #self.trackVerticalProfileTab.reset()

    @pyqtSlot()
    def on_rowInsertButton_clicked(self):
        self.trackVerticalProfileTab.model().insertRow(0)
        self.trackVerticalProfileTab.selectRow(0)
        self.trackVerticalProfileTab.setFocus()

    @pyqtSlot()
    def on_rowDeleteButton_clicked(self):
        indexes = self.trackVerticalProfileTab.selectionModel().selectedIndexes()
        for i in indexes:
            if not i.isValid():
                continue
            print(i.row())
            self.trackVerticalProfileTab.model().removeRow(i.row())

    @pyqtSlot()
    def on_makeStepButton_clicked(self):
        try:
            self.__car.setThrottle(self.engineField.text())
            self.__car.makeStep()
        except:
            QtWidgets.QMessageBox.critical(self, "Error", sys.exc_info()[0])

        self.populateFields()
        print(self.__car.track.getTrackProfile())

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


if __name__ == "__main__":

    app = QtWidgets.QApplication(sys.argv)

    ui = Simulator()
    ui.show()

    sys.exit(app.exec_())
