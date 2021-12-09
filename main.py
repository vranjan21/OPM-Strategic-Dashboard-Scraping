# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Main.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import PyQt5

from PyQt5 import QtCore, QtGui, QtWidgets

# Define a stream, custom class, that reports data written to it, with a Qt signal
class EmittingStream(QtCore.QObject):

    textWritten = QtCore.pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        font = QtGui.QFont()
        font.setFamily("Arial")
        MainWindow.setFont(font)
        MainWindow.setFixedSize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(130, 20, 541, 51))
        font = QtGui.QFont()
        font.setFamily("Arial Black")
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(370, 80, 81, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(300, 100, 221, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(30, 170, 151, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(280, 460, 411, 23))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.progressBar.setFont(font)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(140, 460, 151, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.selectFolder = QtWidgets.QPushButton(self.centralwidget)
        self.selectFolder.setGeometry(QtCore.QRect(190, 160, 113, 32))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.selectFolder.setFont(font)
        self.selectFolder.setObjectName("selectFolder")
        self.selectedFolder = QtWidgets.QLabel(self.centralwidget)
        self.selectedFolder.setGeometry(QtCore.QRect(200, 210, 211, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.selectedFolder.setFont(font)
        self.selectedFolder.setObjectName("selectedFolder")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(30, 210, 151, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.label_7.setFont(font)
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(30, 280, 241, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.updateMeasureList = QtWidgets.QPushButton(self.centralwidget)
        self.updateMeasureList.setGeometry(QtCore.QRect(250, 270, 161, 32))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.updateMeasureList.setFont(font)
        self.updateMeasureList.setObjectName("updateMeasureList")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(30, 310, 541, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(30, 340, 141, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(30, 250, 141, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(13)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(30, 370, 141, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(13)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.savedTo = QtWidgets.QLabel(self.centralwidget)
        self.savedTo.setGeometry(QtCore.QRect(200, 340, 211, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.savedTo.setFont(font)
        self.savedTo.setObjectName("savedTo")
        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        self.label_13.setGeometry(QtCore.QRect(30, 400, 241, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.selectFolder_2 = QtWidgets.QPushButton(self.centralwidget)
        self.selectFolder_2.setGeometry(QtCore.QRect(260, 390, 211, 32))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.selectFolder_2.setFont(font)
        self.selectFolder_2.setObjectName("selectFolder_2")
        self.savedTo_2 = QtWidgets.QLabel(self.centralwidget)
        self.savedTo_2.setGeometry(QtCore.QRect(330, 500, 181, 16))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.savedTo_2.setFont(font)
        self.savedTo_2.setObjectName("savedTo_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionView_Documentation = QtWidgets.QAction(MainWindow)
        self.actionView_Documentation.setObjectName("actionView_Documentation")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.menuHelp.addAction(self.actionView_Documentation)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Strategic Performance Dashboard Measure Extraction"))
        self.label.setText(_translate("MainWindow", "Strategic Performance Dashboard Measure Extraction"))
        self.label_2.setText(_translate("MainWindow", "City of Austin"))
        self.label_3.setText(_translate("MainWindow", "Office of Performance Management"))
        self.label_4.setText(_translate("MainWindow", "Select Folder to Save To:"))
        self.label_5.setText(_translate("MainWindow", "Scrape Progress:"))
        self.selectFolder.setText(_translate("MainWindow", "Select Folder"))
        self.selectedFolder.setText(_translate("MainWindow", "Select a Folder First"))
        self.label_7.setText(_translate("MainWindow", "Selected Folder:"))
        self.label_8.setText(_translate("MainWindow", "Click to Scrape the List of Measures:"))
        self.updateMeasureList.setText(_translate("MainWindow", "Scrape Measure List"))
        self.label_9.setText(_translate("MainWindow", "Note: No need to scrape measure list again if current list of measures is suitable"))
        self.label_10.setText(_translate("MainWindow", "Measure Scrape List:"))
        self.label_11.setText(_translate("MainWindow", "Step 1:"))
        self.label_12.setText(_translate("MainWindow", "Step 2:"))
        self.savedTo.setText(_translate("MainWindow", "Saved To"))
        self.label_13.setText(_translate("MainWindow", "Click to Start Scrape & Extraction:"))
        self.selectFolder_2.setText(_translate("MainWindow", "Scrape Measure Information"))
        self.savedTo_2.setText(_translate("MainWindow", "Scrape Has Not Yet Started"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionView_Documentation.setText(_translate("MainWindow", "View Documentation"))
        self.actionAbout.setText(_translate("MainWindow", "About"))


        # Install a custom output stream by connecting sys.stdout to instance of EmmittingStream.
        sys.stdout = EmittingStream(textWritten=self.output_terminal_written)

        # Create my signal/connections for custom method
        self.selectFolder.clicked.connect(self.sourceDirButtonClicked)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def sourceDirButtonClicked(self):
        for i in range(10):
            print("The Source DIR button has been clicked " + str(i) + " times")

    # custom method to write anything printed out to console/terminal to my QTextEdit widget via append function.
    def output_terminal_written(self, text):
        self.output_terminal_textEdit.append(text)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
