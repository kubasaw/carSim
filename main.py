from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QLabel, QGridLayout, QLineEdit, QPushButton, QMessageBox


class Simulator(QWidget):
    def __init__(self, car, parent=None):

        super().__init__(parent)
        self.__car = car
        self.createInterface()

    def createInterface(self):
        # etykietki
        et1 = QLabel("Time:", self)
        et2 = QLabel("Position:", self)
        et3 = QLabel("Speed:", self)
        et4 = QLabel("Fuel:", self)
        et5 = QLabel("Engine:", self)

        # pola
        self.timeVal = QLineEdit()
        self.positionVal = QLineEdit()
        self.speedVal = QLineEdit()
        self.fuelVal = QLineEdit()
        self.engineVal = QLineEdit()
        self.engineVal.setText("0")

        # button
        evalBtn = QPushButton("&Step", self)
        evalBtn.resize(evalBtn.sizeHint())

        # table
        simpleGrid = QGridLayout()
        simpleGrid.addWidget(et1, 0, 0)
        simpleGrid.addWidget(et2, 0, 1)
        simpleGrid.addWidget(et3, 0, 2)
        simpleGrid.addWidget(et4, 0, 3)
        simpleGrid.addWidget(et5,0,4)
        simpleGrid.addWidget(self.timeVal, 1, 0)
        simpleGrid.addWidget(self.positionVal, 1, 1)
        simpleGrid.addWidget(self.speedVal, 1, 2)
        simpleGrid.addWidget(self.fuelVal, 1, 3)
        simpleGrid.addWidget(self.engineVal,1,4)
        simpleGrid.addWidget(evalBtn, 2, 0, 1, 5)

        self.getSimValues()
        self.timeVal.setReadOnly(True)
        self.positionVal.setReadOnly(True)
        self.speedVal.setReadOnly(True)
        self.fuelVal.setReadOnly(True)

        evalBtn.clicked.connect(self.makeStep)

        # okno
        self.setLayout(simpleGrid)
        self.setWindowTitle("Simulator")
        self.show()

    def makeStep(self):
        try:
            self.__car.setThrottle(self.engineVal.text())
            self.__car.makeStep()
        except Exception as e:
            QMessageBox.critical(self,"Critical Error",str(e))
        self.getSimValues()

    def getSimValues(self):
        self.timeVal.setText(str(self.__car.getSimTime()))
        self.positionVal.setText(str(self.__car.getSimDistance()))
        self.speedVal.setText(str(self.__car.getSimSpeed()))
        self.fuelVal.setText(str(self.__car.getSimFuel()))


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    import car
    paks = car.motion()

    window = Simulator(paks)

    sys.exit(app.exec_())
