# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1020, 433)
        MainWindow.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 971, 341))
        self.tabWidget.setToolTipDuration(0)
        self.tabWidget.setObjectName("tabWidget")
        self.Connection = QtWidgets.QWidget()
        self.Connection.setObjectName("Connection")
        self.serialSettings = QtWidgets.QGroupBox(self.Connection)
        self.serialSettings.setGeometry(QtCore.QRect(9, 9, 231, 301))
        self.serialSettings.setObjectName("serialSettings")
        self.availablePorts = QtWidgets.QComboBox(self.serialSettings)
        self.availablePorts.setGeometry(QtCore.QRect(10, 50, 211, 22))
        self.availablePorts.setObjectName("availablePorts")
        self.refreshAvailablePorts = QtWidgets.QPushButton(self.serialSettings)
        self.refreshAvailablePorts.setGeometry(QtCore.QRect(10, 20, 211, 23))
        self.refreshAvailablePorts.setObjectName("refreshAvailablePorts")
        self.connectPort = QtWidgets.QPushButton(self.serialSettings)
        self.connectPort.setGeometry(QtCore.QRect(10, 270, 211, 23))
        self.connectPort.setCheckable(True)
        self.connectPort.setObjectName("connectPort")
        self.canInterfaceTypes = QtWidgets.QComboBox(self.serialSettings)
        self.canInterfaceTypes.setGeometry(QtCore.QRect(10, 80, 211, 22))
        self.canInterfaceTypes.setObjectName("canInterfaceTypes")
        self.canInterfaceTypes.addItem("")
        self.canInterfaceTypes.setItemText(0, "slcan")
        self.canInterfaceTypes.addItem("")
        self.canInterfaceTypes.setItemText(1, "serial")
        self.canReceived = QtWidgets.QPlainTextEdit(self.Connection)
        self.canReceived.setGeometry(QtCore.QRect(243, 20, 711, 291))
        self.canReceived.setObjectName("canReceived")
        self.tabWidget.addTab(self.Connection, "")
        self.Simulation = QtWidgets.QWidget()
        self.Simulation.setObjectName("Simulation")
        self.gridLayoutWidget = QtWidgets.QWidget(self.Simulation)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 317, 71))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.positionLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.positionLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.positionLabel.setObjectName("positionLabel")
        self.gridLayout.addWidget(self.positionLabel, 0, 1, 1, 1)
        self.engineField = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.engineField.setObjectName("engineField")
        self.gridLayout.addWidget(self.engineField, 1, 4, 1, 1)
        self.positionField = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.positionField.setReadOnly(True)
        self.positionField.setObjectName("positionField")
        self.gridLayout.addWidget(self.positionField, 1, 1, 1, 1)
        self.speedField = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.speedField.setReadOnly(True)
        self.speedField.setObjectName("speedField")
        self.gridLayout.addWidget(self.speedField, 1, 2, 1, 1)
        self.fuelField = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.fuelField.setReadOnly(True)
        self.fuelField.setObjectName("fuelField")
        self.gridLayout.addWidget(self.fuelField, 1, 3, 1, 1)
        self.fuelLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.fuelLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.fuelLabel.setObjectName("fuelLabel")
        self.gridLayout.addWidget(self.fuelLabel, 0, 3, 1, 1)
        self.speedLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.speedLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.speedLabel.setObjectName("speedLabel")
        self.gridLayout.addWidget(self.speedLabel, 0, 2, 1, 1)
        self.timeLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.timeLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.timeLabel.setObjectName("timeLabel")
        self.gridLayout.addWidget(self.timeLabel, 0, 0, 1, 1)
        self.timeField = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.timeField.setReadOnly(True)
        self.timeField.setObjectName("timeField")
        self.gridLayout.addWidget(self.timeField, 1, 0, 1, 1)
        self.makeStepButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.makeStepButton.setObjectName("makeStepButton")
        self.gridLayout.addWidget(self.makeStepButton, 2, 0, 1, 5)
        self.engineLabel = QtWidgets.QLabel(self.gridLayoutWidget)
        self.engineLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.engineLabel.setObjectName("engineLabel")
        self.gridLayout.addWidget(self.engineLabel, 0, 4, 1, 1)
        self.tabWidget.addTab(self.Simulation, "")
        self.Settings = QtWidgets.QWidget()
        self.Settings.setObjectName("Settings")
        self.langSelector = QtWidgets.QComboBox(self.Settings)
        self.langSelector.setGeometry(QtCore.QRect(70, 10, 69, 22))
        self.langSelector.setObjectName("langSelector")
        self.langSelector.addItem("")
        self.langSelector.setItemText(0, "")
        self.langSelectorLabel = QtWidgets.QLabel(self.Settings)
        self.langSelectorLabel.setGeometry(QtCore.QRect(10, 10, 47, 13))
        self.langSelectorLabel.setObjectName("langSelectorLabel")
        self.tabWidget.addTab(self.Settings, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1020, 21))
        self.menuBar.setObjectName("menuBar")
        self.menuMain = QtWidgets.QMenu(self.menuBar)
        self.menuMain.setObjectName("menuMain")
        self.menuAbout = QtWidgets.QMenu(self.menuBar)
        self.menuAbout.setObjectName("menuAbout")
        MainWindow.setMenuBar(self.menuBar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.actionClose = QtWidgets.QAction(MainWindow)
        self.actionClose.setObjectName("actionClose")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionImport_Settings = QtWidgets.QAction(MainWindow)
        self.actionImport_Settings.setObjectName("actionImport_Settings")
        self.actionExport_Settings = QtWidgets.QAction(MainWindow)
        self.actionExport_Settings.setObjectName("actionExport_Settings")
        self.menuMain.addAction(self.actionImport_Settings)
        self.menuMain.addAction(self.actionExport_Settings)
        self.menuMain.addSeparator()
        self.menuMain.addAction(self.actionClose)
        self.menuAbout.addAction(self.actionAbout)
        self.menuBar.addAction(self.menuMain.menuAction())
        self.menuBar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.actionClose.triggered.connect(MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Simulator"))
        self.serialSettings.setTitle(_translate("MainWindow", "Serial communication settings"))
        self.refreshAvailablePorts.setText(_translate("MainWindow", "Refresh"))
        self.connectPort.setText(_translate("MainWindow", "Connect"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Connection), _translate("MainWindow", "Connection"))
        self.positionLabel.setText(_translate("MainWindow", "Position"))
        self.fuelLabel.setText(_translate("MainWindow", "Fuel"))
        self.speedLabel.setText(_translate("MainWindow", "Speed"))
        self.timeLabel.setText(_translate("MainWindow", "Time"))
        self.makeStepButton.setText(_translate("MainWindow", "Make Simulation &Step!"))
        self.engineLabel.setText(_translate("MainWindow", "Engine"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Simulation), _translate("MainWindow", "Simulation"))
        self.langSelectorLabel.setText(_translate("MainWindow", "Language"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Settings), _translate("MainWindow", "Settings"))
        self.menuMain.setTitle(_translate("MainWindow", "Main"))
        self.menuAbout.setTitle(_translate("MainWindow", "About"))
        self.actionClose.setText(_translate("MainWindow", "Close"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionImport_Settings.setText(_translate("MainWindow", "Import Settings"))
        self.actionExport_Settings.setText(_translate("MainWindow", "Export Settings"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
