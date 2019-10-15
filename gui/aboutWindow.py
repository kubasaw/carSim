# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\aboutWindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_AboutDialog(object):
    def setupUi(self, AboutDialog):
        AboutDialog.setObjectName("AboutDialog")
        AboutDialog.resize(378, 210)
        AboutDialog.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.aboutText = QtWidgets.QTextEdit(AboutDialog)
        self.aboutText.setGeometry(QtCore.QRect(10, 10, 271, 191))
        self.aboutText.setObjectName("aboutText")
        self.skapLogo = QtWidgets.QLabel(AboutDialog)
        self.skapLogo.setGeometry(QtCore.QRect(290, 90, 80, 80))
        self.skapLogo.setText("")
        self.skapLogo.setPixmap(QtGui.QPixmap(":/logos/skap_logo.png"))
        self.skapLogo.setScaledContents(True)
        self.skapLogo.setAlignment(QtCore.Qt.AlignCenter)
        self.skapLogo.setObjectName("skapLogo")
        self.iaLogo = QtWidgets.QLabel(AboutDialog)
        self.iaLogo.setGeometry(QtCore.QRect(290, 10, 80, 66))
        self.iaLogo.setText("")
        self.iaLogo.setPixmap(QtGui.QPixmap(":/logos/ia_logo.png"))
        self.iaLogo.setScaledContents(True)
        self.iaLogo.setAlignment(QtCore.Qt.AlignCenter)
        self.iaLogo.setObjectName("iaLogo")
        self.okButton = QtWidgets.QPushButton(AboutDialog)
        self.okButton.setGeometry(QtCore.QRect(290, 175, 80, 25))
        self.okButton.setObjectName("okButton")

        self.retranslateUi(AboutDialog)
        self.okButton.clicked.connect(AboutDialog.close)
        QtCore.QMetaObject.connectSlotsByName(AboutDialog)

    def retranslateUi(self, AboutDialog):
        _translate = QtCore.QCoreApplication.translate
        AboutDialog.setWindowTitle(_translate("AboutDialog", "About"))
        self.aboutText.setHtml(_translate("AboutDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Car Motion Simulator </span><span style=\" font-size:10pt; font-weight:600;\">carSim</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">© by Kuba Sawulski 2019</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">carSim is licensed under the</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:10pt; font-weight:600;\">GNU General Public License v3.0</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Permissions of this strong copyleft license are conditioned on making available complete source code of licensed works and modifications, which include larger works using a licensed work, under the same license. Copyright and license notices must be preserved. Contributors provide an express grant of patent rights.</span></p></body></html>"))
        self.okButton.setText(_translate("AboutDialog", "OK"))
from . import resources_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AboutDialog = QtWidgets.QDialog()
    ui = Ui_AboutDialog()
    ui.setupUi(AboutDialog)
    AboutDialog.show()
    sys.exit(app.exec_())
