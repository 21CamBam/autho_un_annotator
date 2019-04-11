import sys
import time
import bugs
import files
from PyQt5.QtWidgets import QApplication, QWidget, QApplication, QWidget, QPushButton, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import pyqtSlot

#only for button
#from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
#from PyQt5.QtCore import pyqtSlot

#This is showing another test 
#THIS IS A TEST
#class App(QWidget):
 #   def __init__(self):
  #      super().__init__()
   #     self.title = 'auto_un_annotator'
    #    self.left = 10
     #   self.top = 10
      #  self.width = 900
       # self.height = 720
 #       self.initUI()
#
        
        
  #  def initUI(self):
   #     self.setWindowTitle(self.title)
    #    self.setGeometry(self.left, self.top, self.width, self.height)
     #   self.show()
#
class Window(QWidget):

    #sample tree view variables
    FROM, SUBJECT, DATE = range(3)

    bug = "000000"
    bug_data = {}
    button2 = None
    button3 = None 
    current_dir = ""
    current_url = ""
    urls = {}
    num_frequencies = 0
    bug_type = ""
    num_commits = 0
    num_lines_changed = 0
    test_results_green = False # is there a test link in PR
    
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)

        self.title = 'auto_un_annotator'
        self.left = 10
        self.top = 10
        self.width = 900
        self.height = 720
        self.initUI()
        self.BugLabel = QLabel("Enter Bug Number", self)
        self.textBox1 = QLineEdit(self)
        self.textBox1.move(20, 20)
        self.textBox1.resize(50,40)

        #2nd textbox pop up
        self.textbox2 = QLineEdit(self)
        self.textbox2.move(20, 20)
        self.textbox2.resize(200,200)

        button2 = QPushButton('Retrieve', self)
        button2.clicked.connect(self.on_click_retrieve_button)

        #test button to show text
        button3 = QPushButton('Download', self)
        button3.clicked.connect(self.on_click_test)

        self.BugNumberLabel = QLabel("Bug # {} -TITLE HERE", self)
        font = QFont()
        font.setPointSize(20)
        self.BugNumberLabel.setFont(font)
        self.EntryTypeLabel = QLabel("Entry Type", self)
        comboBox1 = QComboBox(self)
        self.TestLabel = QLabel("Test Links:", self)
        #combo test
        comboBox1.addItem("Testing123")
        self.DupeLabel = QLabel("Possible Dupes", self)
        crlabel = QLabel("CR",self)
        prlabel = QLabel("PR:", self)

        button = QPushButton('Compile Report', self)
        button.clicked.connect(self.on_click_report)
        button.setToolTip('This is an example button')
        self.textBox = QPlainTextEdit(self)
        self.textBox.move(250, 120)
        self.textBox.resize(10, 10)
        

        #Sample Tree View
        self.dataGroupBox = QGroupBox("Inbox")
        self.dataView = QTreeView()
        self.dataView.setRootIsDecorated(False)
        self.dataView.setAlternatingRowColors(True)
        
        dataLayout = QHBoxLayout()
        dataLayout.addWidget(self.dataView)
        self.dataGroupBox.setLayout(dataLayout)
        
        #change this to display the directories from the logs
        model = self.createMailModel(self)
        self.dataView.setModel(model)
        self.addMail(model, 'service@github.com', 'Your Github Donation','03/25/2017 02:05 PM')
        self.addMail(model, 'support@github.com', 'Github Projects','02/02/2017 03:05 PM')
        self.addMail(model, 'service@phone.com', 'Your Phone Bill','01/01/2017 04:05 PM')
        
        #mainLayout = QVBoxLayout()
        
        #self.setLayout(mainLayout)


        # create dynamic dataview widget

        self.layout = QGridLayout()
        #tree layout
        self.layout.addWidget(self.dataGroupBox, 9, 0, 1, 5)

        self.layout.addWidget(self.BugLabel, 1, 0, 1, 5)
        self.layout.addWidget(self.textBox1, 1, 2, 1, 1)
        self.layout.addWidget(button2, 2, 2, 1, 1)
        self.layout.addWidget(button3, 10, 0, 1, 1)
        self.layout.addWidget(self.BugNumberLabel, 3, 0, 1, 5)
        #test test box
        #self.layout.addWidget(self.textBox, 5, 0, 1, 5)
        #test entry type label
        #self.layout.addWidget(self.EntryTypeLabel, 4, 1, 1, 5)
        self.layout.addWidget(self.TestLabel, 8, 0, 1 ,1)
        #self.layout.addWidget(coreslabel, 5, 3, 1, 2)
        self.layout.addWidget(self.DupeLabel, 5, 0, 1,5)
        
        self.layout.addWidget(crlabel, 6, 0, 1, 5)
        self.layout.addWidget(prlabel, 7, 0, 1, 5)
        self.layout.addWidget(button, 3, 5, 1, 1)
        self.layout.addWidget(comboBox1, 8, 1, 1, 1)
        
        
        self.setLayout(self.layout) 
        

        #self.show()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        #self.show()
        self.show()
        #time.sleep(.1)

    def populateTestResults(self):
        # populate combobox, comboBox1 should be where test links go
    
        pass

    def populateCR(self):
        # populate combobox
        pass

    def on_select_test_results(self):
        # set current_url
        # set current_dir
        # query for dir listing
        # populate dataview widget
        pass

    #define the tree view functions
    def createMailModel(self,parent):
        model = QStandardItemModel(0, 3, parent)
        model.setHeaderData(self.FROM, Qt.Horizontal, "From")
        model.setHeaderData(self.SUBJECT, Qt.Horizontal, "Subject")
        model.setHeaderData(self.DATE, Qt.Horizontal, "Date")
        return model
    
    def addMail(self,model, mailFrom, subject, date):
        model.insertRow(0)
        model.setData(model.index(0, self.FROM), mailFrom)
        model.setData(model.index(0, self.SUBJECT), subject)
        model.setData(model.index(0, self.DATE), date)

    @pyqtSlot()
    def on_click_retrieve_button(self):
        self.bug_data = bugs.get_bugs([("id",self.textBox1.text())])
        self.urls = files.get_test_urls(self.bug_data[0]["comments"])
        bug = self.textBox1.text()
    
    @pyqtSlot()
    def on_click_report(self):
        print('Open Report')

    @pyqtSlot()
    def on_click_test(self):
        print('Open Text')
        #textboxValue = self.textbox2.text()
        #QMessageBox.question(self, 'Message - pythonspot.com', "You typed: " + textboxValue, QMessageBox.Ok, QMessageBox.Ok)
        #self.textbox.setText("")
        #self.textBox1.setText("")
        self.BugNumberLabel.setText("Bug {} - {}".format(bug, self.bug_data[0]["short_desc"]))
        self.num_frequencies = files.get_frequency_count(self.bug_data[0]["comments"])
        self.bug_type = self.bug_data[0]["cf_bug_type"]
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    sys.exit(app.exec_())
