from PyQt5.QtWidgets import QDialog, QWidget,QLineEdit, QGridLayout, QRadioButton, QHBoxLayout, QPushButton, QSpinBox, QApplication, QVBoxLayout, QLabel, QGroupBox
import sys
from PyQt5 import QtGui, QtCore

# main window
class NoOfProcessesWindow(QDialog) :
    def __init__(self):
        super().__init__()

        #setting the main window in the class constructor
        self.title = "Process Scheduler"
        self.left = 700
        self.top = 350
        self.width = 500
        self.height = 250
        self.iconName = "process.png"

        self.setWindowTitle(self.title)
        self.setWindowIcon(QtGui.QIcon(self.iconName))
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createLayout()

        self.show()

    def createLayout(self):
        # vbox & hbox to resize the window
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()

        groupbox = QGroupBox("How many processes?")
        groupbox.setFont(QtGui.QFont("Sanserif", 14))
        groupbox.setMinimumHeight(175)

        # label used for user friendly purposes
        self.label = QLabel("No. of processes : ")
        self.label.setFont(QtGui.QFont("Sanserif", 12))
        hbox.addWidget(self.label)

        # spin box to determine no of processes
        self.spinBox = QSpinBox()
        self.spinBox.setFont(QtGui.QFont("Sanserif", 10))
        self.spinBox.setMaximumWidth(150)
        hbox.addWidget(self.spinBox)

        # a push button to switch to 2nd menu
        self.button = QPushButton("Next", self)
        self.button.setFont(QtGui.QFont("Sanserif", 12))
        self.button.setToolTip("Proceed to next step")
        self.button.setMaximumWidth(300)
        self.button.setMinimumWidth(150)
        self.button.clicked.connect(self.onButtonPressed)

        groupbox.setLayout(hbox)
        vbox.addWidget(groupbox)
        vbox.addWidget(self.button, 0, QtCore.Qt.AlignCenter)
        self.setLayout(vbox)

    # function that calls 2nd window to choose type of process
    # when the button is pressed
    def onButtonPressed(self):
        self.hide()
        self.schedulertype = TypeOfSchedulingWindow(self.spinBox.value())


# 2nd window to determine scheduling algorithm
class TypeOfSchedulingWindow (QDialog) :
    def __init__(self, noOfProcesses):
        super().__init__()

        self.noOfProcesses = noOfProcesses

        #setting the second window in the class constructor
        self.title = "Process Scheduler"
        self.left = 700
        self.top = 350
        self.width = 600
        self.height = 250
        self.iconName = "process.png"

        self.setWindowTitle(self.title)
        self.setWindowIcon(QtGui.QIcon(self.iconName))
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createLayout()

        self.show()

    def createLayout(self):
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        grid = QGridLayout()

        groupbox = QGroupBox("Choose scheduling algorithm:")
        groupbox.setFont(QtGui.QFont("Sanserif", 14))
        groupbox.setMinimumHeight(175)

        # radio buttons to determine scheduling algorithm

        self.radiobtn1 = QRadioButton("First Come First Served")
        self.radiobtn1.setFont((QtGui.QFont("Sanserif", 12)))
        grid.addWidget(self.radiobtn1, 0, 0)

        self.radiobtn2 = QRadioButton("Shortest Job First")
        self.radiobtn2.setFont((QtGui.QFont("Sanserif", 12)))
        grid.addWidget(self.radiobtn2, 0, 1)

        self.radiobtn3 = QRadioButton("Priority")
        self.radiobtn3.setFont((QtGui.QFont("Sanserif", 12)))
        grid.addWidget(self.radiobtn3, 1, 0)

        self.radiobtn4 = QRadioButton("Round Robbin")
        self.radiobtn4.setFont((QtGui.QFont("Sanserif", 12)))
        grid.addWidget(self.radiobtn4, 1, 1)

        # a push button to switch to 3rd menu
        self.button = QPushButton("Next", self)
        self.button.setFont(QtGui.QFont("Sanserif", 12))
        self.button.setToolTip("Proceed to next step")
        self.button.setMinimumWidth(150)
        self.button.clicked.connect(self.onButtonPressed)

        # label used to remind user of no of processes
        self.label = QLabel("No. of processes chosen is " + str(self.noOfProcesses))
        self.label.setFont(QtGui.QFont("Sanserif", 12))

        groupbox.setLayout(grid)
        vbox.addWidget(groupbox)
        vbox.addWidget(self.label)
        vbox.addWidget(self.button, 0, QtCore.Qt.AlignCenter)
        self.setLayout(vbox)

    def onButtonPressed(self):
        self.hide()
        # depending upon the user choice, the targeted window opens
        if self.radiobtn1.isChecked() :
            self.fcfs = GetInputWindow(self.noOfProcesses)
        elif self.radiobtn4.isChecked():
            self.rr = RR(self.noOfProcesses)
        elif self.radiobtn3.isChecked():
            self.pr = Priority(self.noOfProcesses)
        elif self.radiobtn2.isChecked():
            self.sjf = SJF(self.noOfProcesses)


# getting input window
class GetInputWindow (QDialog) :
    def __init__(self, noOfProcesses):
        super().__init__()

        self.noOfProcesses = noOfProcesses

        #setting the third window in the class constructor
        self.title = "FCFS"
        if self.noOfProcesses >1:
            self.left = 550
        else :
            self.left = 700
        self.top = 350
        self.width = 600
        self.height = 250
        self.iconName = "process.png"

        self.setWindowTitle(self.title)
        self.setWindowIcon(QtGui.QIcon(self.iconName))
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createLayout()

        self.show()


    def createLayout(self):
        self.grid = QGridLayout()
        self.arrivalList = []
        self.burstList = []

        for i in range(self.noOfProcesses):

            hbox = QHBoxLayout()

            # group box for each process
            groupbox = QGroupBox("Process " + str(i+1))
            groupbox.setFont(QtGui.QFont("Sanserif", 14))
            groupbox.setMinimumHeight(175)

            self.label1 = QLabel("Arrival time")
            self.label1.setFont(QtGui.QFont("Sanserif", 12))
            hbox.addWidget(self.label1)

            # for the input of arrival time
            self.lineEdit1 = QLineEdit(self)
            self.lineEdit1.setFont(QtGui.QFont("Sanserif", 12))
            self.lineEdit1.setMaximumWidth(100)
            hbox.addWidget(self.lineEdit1)

            # appending the arrival time in a list
            # so as to access its value later on
            self.arrivalList.append(self.lineEdit1)

            hbox.addStretch()

            self.label2 = QLabel("Burst time")
            self.label2.setFont(QtGui.QFont("Sanserif", 12))
            hbox.addWidget(self.label2)

            # for the input of arrival time
            self.lineEdit2 = QLineEdit(self)
            self.lineEdit2.setFont(QtGui.QFont("Sanserif", 12))
            self.lineEdit2.setMaximumWidth(100)
            hbox.addWidget(self.lineEdit2)

            # appending the arrival time in a list
            # so as to access its value later on
            self.burstList.append(self.lineEdit2)

            groupbox.setLayout(hbox)

            if i%2 == 0:
                self.grid.addWidget(groupbox, i, 0)
            else :
                self.grid.addWidget(groupbox, i-1, 1)

        # a push button to draw
        self.button = QPushButton("Draw", self)
        self.button.setFont(QtGui.QFont("Sanserif", 12))
        self.button.setToolTip("Proceed to next step")
        self.button.setMinimumWidth(150)
        self.button.setMaximumWidth(150)
        self.button.clicked.connect(self.fetch)

        if self.noOfProcesses<=1:
            self.grid.addWidget(self.button, 1, 0)
        elif self.noOfProcesses%2 == 0:
            self.grid.addWidget(self.button,  1+self.noOfProcesses//2, 0)
        else:
            self.grid.addWidget(self.button)

        self.setLayout(self.grid)

    # fn to get user inputs
    def fetch(self):
        self.arrivalDict = dict()
        self.burstDict = dict()

        # fetch input values into dictionaries
        # where key is Pi and value is either arrivalTime or BurstTime
        for i in range(len(self.arrivalList)):
            processName = "P"+str(i+1)
            processArrival = int(self.arrivalList[i].text())
            processBurst = int(self.burstList[i].text())
            self.arrivalDict[processName] = processArrival
            self.burstDict[processName] = processBurst

        self.hide()
        self.draw = DrawFCFS(self.arrivalDict, self.burstDict)


class DrawFCFS (QDialog):
    def __init__(self, arrivaldict, burstdict):
        super().__init__()

        self.arrivalDict = arrivaldict
        self.burstDict = burstdict

        #setting the main window in the class constructor
        self.title = "FCFS"
        self.left = 700
        self.top = 350
        self.width = 500
        self.height = 250
        self.iconName = "process.png"

        self.setWindowTitle(self.title)
        self.setWindowIcon(QtGui.QIcon(self.iconName))
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createLayout()

        self.show()

    def createLayout(self):
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()

        groupbox = QGroupBox("Processes after scheduling")
        groupbox.setFont(QtGui.QFont("Sanserif", 14))
        groupbox.setMinimumHeight(175)

        # sorting dictionaries according to arrival time
        listofTuples = sorted(self.arrivalDict.items(), key=lambda x: x[1])
        for elem in listofTuples:
            self.button = QPushButton(self)
            self.button.setText(elem[0])
            self.button.setFont(QtGui.QFont("Sanserif", 12))
            tooltiptitle = "Arrival: " + str(elem[1]) + "\nBurst: " + str(self.burstDict[elem[0]])
            self.button.setToolTip(tooltiptitle)
            potentialwidth = self.burstDict[elem[0]] * 35
            self.button.setMinimumWidth(potentialwidth)

            hbox.addWidget(self.button)

        self.button = QPushButton("Reset", self)
        self.button.setFont(QtGui.QFont("Sanserif", 12))
        self.button.setToolTip("Go to main window")
        self.button.setMinimumWidth(150)
        self.button.clicked.connect(self.onButtonPressed)

        groupbox.setLayout(hbox)
        vbox.addWidget(groupbox)
        vbox.addWidget(self.button, 0, QtCore.Qt.AlignCenter)
        self.setLayout(vbox)

    def onButtonPressed(self):
        self.hide()
        self.reset = NoOfProcessesWindow()


# running the program
App = QApplication(sys.argv)
window = NoOfProcessesWindow()
sys.exit(App.exec())

# under modification

class SJF (QDialog) :
    def __init__(self, noOfProcesses):
        super().__init__()

        self.noOfProcesses = noOfProcesses

        #setting the third window in the class constructor
        self.title = "SJF"
        if self.noOfProcesses >1:
            self.left = 550
        else :
            self.left = 700
        self.top = 350
        self.width = 600
        self.height = 250
        self.iconName = "process.png"

        self.setWindowTitle(self.title)
        self.setWindowIcon(QtGui.QIcon(self.iconName))
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createLayout()

        self.show()

    def createLayout(self):
        self.grid = QGridLayout()
        for i in range(self.noOfProcesses):

            hbox = QHBoxLayout()

            groupbox = QGroupBox("Process " + str(i+1))
            groupbox.setFont(QtGui.QFont("Sanserif", 14))

            self.label1 = QLabel("Arrival time")
            self.label1.setFont(QtGui.QFont("Sanserif", 12))
            hbox.addWidget(self.label1)

            self.lineEdit1 = QLineEdit(self)
            self.lineEdit1.setFont(QtGui.QFont("Sanserif", 12))
            self.lineEdit1.setMaximumWidth(100)
            # self.lineEdit.returnPressed.connect(self.onPressed)
            hbox.addWidget(self.lineEdit1)

            hbox.addStretch()

            self.label2 = QLabel("Burst time")
            self.label2.setFont(QtGui.QFont("Sanserif", 12))
            hbox.addWidget(self.label2)

            self.lineEdit2 = QLineEdit(self)
            self.lineEdit2.setFont(QtGui.QFont("Sanserif", 12))
            self.lineEdit2.setMaximumWidth(100)
            # self.lineEdit.returnPressed.connect(self.onPressed)
            hbox.addWidget(self.lineEdit2)

            groupbox.setLayout(hbox)

            if i%2 == 0:
                self.grid.addWidget(groupbox, i, 0)
            else :
                 self.grid.addWidget(groupbox, i-1, 1)

        self.setLayout(self.grid)


class RR (QDialog) :
    def __init__(self, noOfProcesses):
        super().__init__()

        self.noOfProcesses = noOfProcesses

        #setting the third window in the class constructor
        self.title = "Round Robbin"
        if self.noOfProcesses >1:
            self.left = 550
        else :
            self.left = 700
        self.top = 350
        self.width = 600
        self.height = 250
        self.iconName = "process.png"

        self.setWindowTitle(self.title)
        self.setWindowIcon(QtGui.QIcon(self.iconName))
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createLayout()

        self.show()

    def createLayout(self):
        self.grid = QGridLayout()

        groupbox = QGroupBox("Quantum")
        groupbox.setFont(QtGui.QFont("Sanserif", 14))

        hbox = QHBoxLayout()

        self.label0 = QLabel("Quantum time")
        self.label0.setFont(QtGui.QFont("Sanserif", 12))
        hbox.addWidget(self.label0)

        self.lineEdit0 = QLineEdit(self)
        self.lineEdit0.setFont(QtGui.QFont("Sanserif", 12))
        self.lineEdit0.setMaximumWidth(100)
        # self.lineEdit.returnPressed.connect(self.onPressed)
        hbox.addWidget(self.lineEdit0)

        groupbox.setLayout(hbox)

        self.grid.addWidget(groupbox, 0, 0.5)

        for i in range(self.noOfProcesses):

            hbox = QHBoxLayout()

            groupbox = QGroupBox("Process " + str(i+1))
            groupbox.setFont(QtGui.QFont("Sanserif", 14))

            self.label1 = QLabel("Arrival time")
            self.label1.setFont(QtGui.QFont("Sanserif", 12))
            hbox.addWidget(self.label1)

            self.lineEdit1 = QLineEdit(self)
            self.lineEdit1.setFont(QtGui.QFont("Sanserif", 12))
            self.lineEdit1.setMaximumWidth(100)
            # self.lineEdit.returnPressed.connect(self.onPressed)
            hbox.addWidget(self.lineEdit1)

            hbox.addStretch()

            self.label2 = QLabel("Burst time")
            self.label2.setFont(QtGui.QFont("Sanserif", 12))
            hbox.addWidget(self.label2)

            self.lineEdit2 = QLineEdit(self)
            self.lineEdit2.setFont(QtGui.QFont("Sanserif", 12))
            self.lineEdit2.setMaximumWidth(100)
            # self.lineEdit.returnPressed.connect(self.onPressed)
            hbox.addWidget(self.lineEdit2)

            groupbox.setLayout(hbox)

            if i%2 == 0:
                self.grid.addWidget(groupbox, i+1, 0)
            else :
                self.grid.addWidget(groupbox, i, 1)

        self.setLayout(self.grid)


class Priority (QDialog) :
    def __init__(self, noOfProcesses):
        super().__init__()

        self.noOfProcesses = noOfProcesses

        #setting the third window in the class constructor
        self.title = "Priority"
        if self.noOfProcesses >1:
            self.left = 450
        else :
            self.left = 700
        self.top = 350
        self.width = 600
        self.height = 250
        self.iconName = "process.png"

        self.setWindowTitle(self.title)
        self.setWindowIcon(QtGui.QIcon(self.iconName))
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createLayout()

        self.show()

    def createLayout(self):
        self.grid = QGridLayout()
        for i in range(self.noOfProcesses):

            hbox = QHBoxLayout()

            groupbox = QGroupBox("Process " + str(i+1))
            groupbox.setFont(QtGui.QFont("Sanserif", 14))

            self.label1 = QLabel("Arrival time")
            self.label1.setFont(QtGui.QFont("Sanserif", 12))
            hbox.addWidget(self.label1)

            self.lineEdit1 = QLineEdit(self)
            self.lineEdit1.setFont(QtGui.QFont("Sanserif", 12))
            self.lineEdit1.setMaximumWidth(100)
            # self.lineEdit.returnPressed.connect(self.onPressed)
            hbox.addWidget(self.lineEdit1)

            hbox.addStretch()

            self.label2 = QLabel("Burst time")
            self.label2.setFont(QtGui.QFont("Sanserif", 12))
            hbox.addWidget(self.label2)

            self.lineEdit2 = QLineEdit(self)
            self.lineEdit2.setFont(QtGui.QFont("Sanserif", 12))
            self.lineEdit2.setMaximumWidth(100)
            # self.lineEdit.returnPressed.connect(self.onPressed)
            hbox.addWidget(self.lineEdit2)

            hbox.addStretch()

            self.label3 = QLabel("Priority")
            self.label3.setFont(QtGui.QFont("Sanserif", 12))
            hbox.addWidget(self.label3)

            self.lineEdit3 = QLineEdit(self)
            self.lineEdit3.setFont(QtGui.QFont("Sanserif", 12))
            self.lineEdit3.setMaximumWidth(100)
            # self.lineEdit.returnPressed.connect(self.onPressed)
            hbox.addWidget(self.lineEdit3)

            groupbox.setLayout(hbox)

            if i%2 == 0:
                self.grid.addWidget(groupbox, i, 0)
            else :
                 self.grid.addWidget(groupbox, i-1, 1)

        self.setLayout(self.grid)


