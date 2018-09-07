# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.7
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 480)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("background-color: rgb(0, 0, 0);")
        MainWindow.setLocale(QtCore.QLocale(QtCore.QLocale.Portuguese, QtCore.QLocale.Brazil))
        self.centralWidget = QtWidgets.QWidget(MainWindow)
        self.centralWidget.setObjectName("centralWidget")
        self.lcdNumber = QtWidgets.QLCDNumber(self.centralWidget)
        self.lcdNumber.setGeometry(QtCore.QRect(420, 110, 241, 51))
        self.lcdNumber.setStyleSheet("")
        self.lcdNumber.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.lcdNumber.setFrameShadow(QtWidgets.QFrame.Raised)
        self.lcdNumber.setSmallDecimalPoint(False)
        self.lcdNumber.setDigitCount(9)
        self.lcdNumber.setProperty("value", 0.0)
        self.lcdNumber.setObjectName("lcdNumber")
        self.btnStop = QtWidgets.QPushButton(self.centralWidget)
        self.btnStop.setGeometry(QtCore.QRect(690, 112, 91, 51))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.btnStop.setFont(font)
        self.btnStop.setStyleSheet(":enabled{background-color: rgb(204, 0, 0);\n"
"color: rgb(255, 255, 255);}")
        self.btnStop.setObjectName("btnStop")
        self.lstViewCodes = QtWidgets.QListView(self.centralWidget)
        self.lstViewCodes.setGeometry(QtCore.QRect(10, 110, 261, 192))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.lstViewCodes.setFont(font)
        self.lstViewCodes.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 0, 0);")
        self.lstViewCodes.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.lstViewCodes.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.lstViewCodes.setObjectName("lstViewCodes")
        self.btnRemove = QtWidgets.QPushButton(self.centralWidget)
        self.btnRemove.setEnabled(False)
        self.btnRemove.setGeometry(QtCore.QRect(10, 310, 261, 61))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.btnRemove.setFont(font)
        self.btnRemove.setStyleSheet(":enabled{color: rgb(255, 255, 255);\n"
"background-color: rgb(114, 159, 207);}")
        self.btnRemove.setObjectName("btnRemove")
        self.label = QtWidgets.QLabel(self.centralWidget)
        self.label.setGeometry(QtCore.QRect(10, 80, 251, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("color: rgb(255, 255, 255);")
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralWidget)
        self.label_2.setGeometry(QtCore.QRect(0, 10, 781, 51))
        font = QtGui.QFont()
        font.setPointSize(30)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color: rgb(255, 255, 255);")
        self.label_2.setTextFormat(QtCore.Qt.RichText)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.lcdOne = QtWidgets.QLCDNumber(self.centralWidget)
        self.lcdOne.setEnabled(False)
        self.lcdOne.setGeometry(QtCore.QRect(500, 210, 71, 51))
        self.lcdOne.setStyleSheet("color: rgb(52, 101, 164);")
        self.lcdOne.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.lcdOne.setFrameShadow(QtWidgets.QFrame.Raised)
        self.lcdOne.setMidLineWidth(0)
        self.lcdOne.setSmallDecimalPoint(False)
        self.lcdOne.setDigitCount(2)
        self.lcdOne.setProperty("value", 0.0)
        self.lcdOne.setObjectName("lcdOne")
        self.lcdTwo = QtWidgets.QLCDNumber(self.centralWidget)
        self.lcdTwo.setEnabled(False)
        self.lcdTwo.setGeometry(QtCore.QRect(580, 210, 71, 51))
        self.lcdTwo.setStyleSheet("color: rgb(204, 0, 0);")
        self.lcdTwo.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.lcdTwo.setFrameShadow(QtWidgets.QFrame.Raised)
        self.lcdTwo.setMidLineWidth(0)
        self.lcdTwo.setSmallDecimalPoint(False)
        self.lcdTwo.setDigitCount(2)
        self.lcdTwo.setSegmentStyle(QtWidgets.QLCDNumber.Filled)
        self.lcdTwo.setProperty("value", 0.0)
        self.lcdTwo.setProperty("intValue", 0)
        self.lcdTwo.setObjectName("lcdTwo")
        self.lcdPac = QtWidgets.QLCDNumber(self.centralWidget)
        self.lcdPac.setEnabled(False)
        self.lcdPac.setGeometry(QtCore.QRect(420, 210, 71, 51))
        self.lcdPac.setStyleSheet("color: rgb(237, 212, 0);")
        self.lcdPac.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.lcdPac.setFrameShadow(QtWidgets.QFrame.Raised)
        self.lcdPac.setMidLineWidth(0)
        self.lcdPac.setSmallDecimalPoint(False)
        self.lcdPac.setDigitCount(2)
        self.lcdPac.setProperty("value", 0.0)
        self.lcdPac.setObjectName("lcdPac")
        self.lcdFour = QtWidgets.QLCDNumber(self.centralWidget)
        self.lcdFour.setEnabled(False)
        self.lcdFour.setGeometry(QtCore.QRect(720, 210, 71, 51))
        self.lcdFour.setStyleSheet("color: rgb(117, 80, 123);")
        self.lcdFour.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.lcdFour.setFrameShadow(QtWidgets.QFrame.Raised)
        self.lcdFour.setMidLineWidth(0)
        self.lcdFour.setSmallDecimalPoint(False)
        self.lcdFour.setDigitCount(2)
        self.lcdFour.setProperty("value", 0.0)
        self.lcdFour.setObjectName("lcdFour")
        self.lcdThree = QtWidgets.QLCDNumber(self.centralWidget)
        self.lcdThree.setEnabled(False)
        self.lcdThree.setGeometry(QtCore.QRect(650, 210, 71, 51))
        self.lcdThree.setStyleSheet("color: rgb(245, 121, 0);")
        self.lcdThree.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.lcdThree.setFrameShadow(QtWidgets.QFrame.Raised)
        self.lcdThree.setMidLineWidth(0)
        self.lcdThree.setSmallDecimalPoint(False)
        self.lcdThree.setDigitCount(2)
        self.lcdThree.setProperty("value", 0.0)
        self.lcdThree.setObjectName("lcdThree")
        self.label_3 = QtWidgets.QLabel(self.centralWidget)
        self.label_3.setGeometry(QtCore.QRect(280, 108, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("color: rgb(237, 212, 0);")
        self.label_3.setTextFormat(QtCore.Qt.RichText)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralWidget)
        self.label_4.setGeometry(QtCore.QRect(280, 143, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet("color: rgb(52, 101, 164);")
        self.label_4.setTextFormat(QtCore.Qt.RichText)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.centralWidget)
        self.label_5.setGeometry(QtCore.QRect(280, 174, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet("color: rgb(204, 0, 0);")
        self.label_5.setTextFormat(QtCore.Qt.RichText)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.centralWidget)
        self.label_6.setGeometry(QtCore.QRect(280, 204, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet("color: rgb(245, 121, 0);")
        self.label_6.setTextFormat(QtCore.Qt.RichText)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.centralWidget)
        self.label_7.setGeometry(QtCore.QRect(280, 233, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setStyleSheet("color: rgb(117, 80, 123);")
        self.label_7.setTextFormat(QtCore.Qt.RichText)
        self.label_7.setObjectName("label_7")
        self.lifeBar = QtWidgets.QProgressBar(self.centralWidget)
        self.lifeBar.setEnabled(True)
        self.lifeBar.setGeometry(QtCore.QRect(420, 270, 81, 23))
        self.lifeBar.setAutoFillBackground(False)
        self.lifeBar.setStyleSheet("QProgressBar:horizontal {\n"
"border: 1px solid white;\n"
"border-radius: 3px;\n"
"background: black;\n"
"padding: 1px;\n"
"}\n"
"QProgressBar::chunk:horizontal {\n"
"background: red;\n"
"}")
        self.lifeBar.setMinimum(0)
        self.lifeBar.setMaximum(4)
        self.lifeBar.setProperty("value", 2)
        self.lifeBar.setTextVisible(False)
        self.lifeBar.setInvertedAppearance(True)
        self.lifeBar.setObjectName("lifeBar")
        MainWindow.setCentralWidget(self.centralWidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "BizSys"))
        self.btnStop.setText(_translate("MainWindow", "Stop"))
        self.btnRemove.setText(_translate("MainWindow", "-"))
        self.label.setText(_translate("MainWindow", "Participantes:"))
        self.label_2.setText(_translate("MainWindow", "PACMAN"))
        self.label_3.setText(_translate("MainWindow", "PACMAN "))
        self.label_4.setText(_translate("MainWindow", "BLUE"))
        self.label_5.setText(_translate("MainWindow", "RED"))
        self.label_6.setText(_translate("MainWindow", "ORANGE"))
        self.label_7.setText(_translate("MainWindow", "PURPLE"))

