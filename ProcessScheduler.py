from PyQt5.QtWidgets import QDialog, QWidget,QLineEdit, QGridLayout, QRadioButton, QHBoxLayout, QPushButton, QSpinBox, QApplication, QVBoxLayout, QLabel, QGroupBox
import sys
from PyQt5 import QtGui, QtCore

# main window
class NoOfProcessesWindow(QDialog) :
    def __init__(self):
        super().__init__()

        #setting the main window in the class constructor
        self.title = "Process Scheduler"
        self.left = 500
        self.top = 200
        self.width = 350
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
        self.spinBox.setMaximumWidth(100)
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
        self.left = 450
        self.top = 200
        self.width = 450
        self.height = 250
        self.iconName = "process.png"

        self.setWindowTitle(self.title)
        self.setWindowIcon(QtGui.QIcon(self.iconName))
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createLayout()

        self.show()

    def createLayout(self):
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

        # depending upon the user choice, the type of algorithm is chosen
        if self.radiobtn1.isChecked() :
            self.alg = "FCFS"
        elif self.radiobtn4.isChecked():
            self.alg = "RR"
        elif self.radiobtn3.isChecked():
            self.alg = "Priority"
        elif self.radiobtn2.isChecked():
            self.alg = "SJF"

        # opening new window with the target algorithm
        self.inputWinodw = GetInputWindow(self.noOfProcesses, self.alg)


# getting input window
class GetInputWindow (QDialog) :
    def __init__(self, noOfProcesses, algorithm):
        super().__init__()

        self.noOfProcesses = noOfProcesses
        self.algorithm = algorithm

        #setting the third window in the class constructor
        self.title = self.algorithm
        if self.noOfProcesses >1:
            self.left = 350
        else :
            self.left = 500
        self.top = 200
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
        self.priorityList = []

        # if Round Robin add the quantum input
        if (self.algorithm == "RR"):
            groupbox = QGroupBox("Quantum")
            groupbox.setFont(QtGui.QFont("Sanserif", 14))
            groupbox.setMaximumHeight(100)

            hbox = QHBoxLayout()

            self.label0 = QLabel("Quantum time")
            self.label0.setFont(QtGui.QFont("Sanserif", 12))
            hbox.addWidget(self.label0)

            self.lineEdit0 = QLineEdit(self)
            self.lineEdit0.setFont(QtGui.QFont("Sanserif", 12))
            self.lineEdit0.setMaximumWidth(100)
            hbox.addWidget(self.lineEdit0)

            self.lineQuantum = self.lineEdit0

            groupbox.setLayout(hbox)

            self.grid.addWidget(groupbox, 0, 0.5)

        # if priority or sjf determine the type
        elif self.algorithm == "Priority" or self.algorithm == "SJF":
            groupbox = QGroupBox("Type")
            groupbox.setFont(QtGui.QFont("Sanserif", 14))
            groupbox.setMaximumHeight(100)

            hbox = QHBoxLayout()

            self.radiobtn1 = QRadioButton("Preemptive")
            self.radiobtn1.setFont((QtGui.QFont("Sanserif", 12)))
            hbox.addWidget(self.radiobtn1)

            self.radiobtn2 = QRadioButton("Non-Preemptive")
            self.radiobtn2.setFont((QtGui.QFont("Sanserif", 12)))
            hbox.addWidget(self.radiobtn2)

            groupbox.setLayout(hbox)
            
            self.grid.addWidget(groupbox, 0, 0.5)

        for i in range(self.noOfProcesses):

            hbox = QHBoxLayout()

            # group box for each process
            groupbox = QGroupBox("Process " + str(i+1))
            groupbox.setFont(QtGui.QFont("Sanserif", 14))
            groupbox.setMinimumHeight(100)
            groupbox.setMaximumHeight(150)

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

            # just in case priority
            if self.algorithm == "Priority":
                hbox.addStretch()

                self.label3 = QLabel("Priority")
                self.label3.setFont(QtGui.QFont("Sanserif", 12))
                hbox.addWidget(self.label3)

                self.lineEdit3 = QLineEdit(self)
                self.lineEdit3.setFont(QtGui.QFont("Sanserif", 12))
                self.lineEdit3.setMaximumWidth(100)
                hbox.addWidget(self.lineEdit3)

                # appending the priority in a list
                # so as to access its value later on
                self.priorityList.append(self.lineEdit3)

            groupbox.setLayout(hbox)

            if i%2 == 0:
                if (self.algorithm == "RR" or self.algorithm == "Priority" or self.algorithm == "SJF"):
                    i+=1
                self.grid.addWidget(groupbox, i, 0)
            else :
                if (self.algorithm == "RR" or self.algorithm == "Priority" or self.algorithm == "SJF"):
                    i+=1
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
        self.priorityDict = dict()
        self.type = "Nothing"
        self.rrquantum = 0

        # in case of round robbin get the quantum value
        if self.algorithm == "RR":
            self.rrquantum = int(self.lineQuantum.text())
        elif self.algorithm == "Priority" or self.algorithm == "SJF":
            if self.radiobtn1.isChecked():
                self.type = "Preemptive"
            elif self.radiobtn2.isChecked():
                self.type = "Non-Preemptive"

        # fetch input values into dictionaries
        # where key is Pi and value is either arrivalTime or BurstTime
        for i in range(len(self.arrivalList)):
            processName = "P"+str(i+1)
            processArrival = int(self.arrivalList[i].text())
            processBurst = int(self.burstList[i].text())
            self.arrivalDict[processName] = processArrival
            self.burstDict[processName] = processBurst
            # in case of priority
            if self.algorithm == "Priority":
                processPriority = int(self.priorityList[i].text())
                self.priorityDict[processName] = processPriority

        self.hide()
        self.draw = Draw(self.arrivalDict, self.burstDict, self.priorityDict, self.algorithm, self.rrquantum, self.type)


# last window for drawing processes gantt chart
class Draw (QDialog):
    def __init__(self, arrivaldict, burstdict, prioritydict, algorithm, rrquantum, type):
        super().__init__()

        self.arrivalDict = arrivaldict
        self.burstDict = burstdict
        self.priorityDict = prioritydict
        self.algorithm = algorithm
        self.quantum = rrquantum
        self.type = type

        self.totalBurstTime = sum(self.burstDict.values())
        self.avgWaitingTime = 0

        #setting the window in the class constructor
        self.title = self.algorithm
        self.left = 300
        self.top = 200
        self.width = 100
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
        buttonHbox = QHBoxLayout()

        groupbox = QGroupBox("Processes after scheduling")
        groupbox.setFont(QtGui.QFont("Sanserif", 14))
        groupbox.setMinimumHeight(175)

        # First Come First Served
        if self.algorithm == "FCFS":
            # sorting dictionaries according to arrival time
            listofTuples = sorted(self.arrivalDict.items(), key=lambda x: x[1])
           
            for elem in listofTuples:
                self.button = QPushButton(self)
                self.button.setText(elem[0])
                self.button.setFont(QtGui.QFont("Sanserif", 12))
                tooltiptitle = "Arrival: " + str(elem[1]) + "\nBurst: " + str(self.burstDict[elem[0]])
                self.button.setToolTip(tooltiptitle)
                potentialwidth = self.burstDict[elem[0]]
                self.button.setMinimumWidth(potentialwidth*35)
                self.button.setMaximumWidth(potentialwidth*50)

                hbox.addWidget(self.button)


        # Non-preemptive Priority
        elif self.algorithm == "Priority" and self.type == "Non-Preemptive":
            # getting the processes that arrived firstly
            firstarrival = min(self.arrivalDict.values())
            noOfFirstArrivals = sum(v == firstarrival for v in self.arrivalDict.values())

            priorityDictofFirstArrivals = dict()

            # getting highest priority of processes arrived firstly by sorting them
            for item in self.arrivalDict.items():
                if item[1]==firstarrival:
                    priorityDictofFirstArrivals[item[0]] = self.priorityDict[item[0]]
            listofTuples = sorted(priorityDictofFirstArrivals.items(), key=lambda x: x[1])
      
            firstelement = listofTuples[0][0]
            # putting first element in ordered list for drawing
            orderedlist = [firstelement]
            # removing the first element from arrival list 
            self.arrivalDict.pop(firstelement)

            soFarBurst = self.burstDict[firstelement]

            # as long as not all processes are taken
            while soFarBurst < self.totalBurstTime:
                # getting processes to get processed next
                listofTuples = sorted(self.arrivalDict.items(), key=lambda x: x[1])

                priorityDictofOtherArrivals = dict()

                # if process arrived while processing the ones before it, include it with the next ones
                for elem in listofTuples:
                    if elem[1] <= firstarrival+soFarBurst:
                        priorityDictofOtherArrivals[elem[0]] = self.priorityDict[elem[0]]
                    else :
                        break
             
                listofTuples = sorted(priorityDictofOtherArrivals.items(), key=lambda x: x[1])
                
                # adding ready processes to the ordered list 
                for elem in listofTuples:
                    orderedlist.append(elem[0])
                    self.arrivalDict.pop(elem[0])
                    soFarBurst += self.burstDict[elem[0]]

            for p in orderedlist:
                self.button = QPushButton(self)
                self.button.setText(p)
                self.button.setFont(QtGui.QFont("Sanserif", 12))
                potentialwidth = self.burstDict[p]
                self.button.setMinimumWidth(potentialwidth*35)
                self.button.setMaximumWidth(potentialwidth*50)

                hbox.addWidget(self.button)


        # reset button to go back to main window
        self.button = QPushButton("Reset", self)
        self.button.setFont(QtGui.QFont("Sanserif", 12))
        self.button.setToolTip("Go to main window")
        self.button.setMaximumWidth(150)
        self.button.clicked.connect(self.reset)

        # exit button
        self.button1 = QPushButton("Exit", self)
        self.button1.setFont(QtGui.QFont("Sanserif", 12))
        self.button1.setToolTip("Exit the program")
        self.button1.setMaximumWidth(150)
        self.button1.clicked.connect(self.exit)

        buttonHbox.addStretch()
        buttonHbox.addWidget(self.button)
        buttonHbox.addWidget(self.button1)

        buttonGroupbox = QGroupBox()
        buttonGroupbox.setLayout(buttonHbox)

        groupbox.setLayout(hbox)
        vbox.addWidget(groupbox)
        vbox.addWidget(buttonGroupbox)
        self.setLayout(vbox)

    def reset(self):
        self.hide()
        self.newwindow = NoOfProcessesWindow()

    def exit(self):
        sys.exit()


# running the program
App = QApplication(sys.argv)
window = NoOfProcessesWindow()
sys.exit(App.exec())
