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
    NAME = 0
    bug = "000000"
    bug_data = {}
    dataGroupBox = None
    dirbox = None
    freqlabel = None
    tree = None
    button = None
    button2 = None
    button3 = None 
    crlabel = None
    prlabel = None
    comboBox1 = None
    textboxCR = None
    textboxPR = None
    textboxFreq = None
    dialog = None
    current_dir = "/"
    current_url = ""
    urls = {}
    num_frequencies = 0
    bug_type = ""
    num_commits = 0
    num_lines_changed = 0
    test_results_green = False # is there a test link in PR
    
    def select_dir(self):
        f = self.tree.selectedIndexes()[0]
        new_dir = f.model().itemFromIndex(f).text()
        if new_dir == "..":
            index = self.current_dir.rfind("/",0, self.current_dir.rfind("/"))
            self.current_dir = self.current_dir[:index+1]
        else:
            if new_dir.startswith("[D] "):
                self.current_dir = self.current_dir + new_dir[4:] + "/"
                self.current_url = str(self.comboBox1.currentText())
                dir_listing = files.get_directory_listing(self.current_dir, self.current_url)
                self.populateTree(dir_listing)
            elif new_dir.endswith(".gz"):
                # download prompt
                fname = files.download_file(self.current_dir+new_dir, self.current_url)
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("File downloaded!")
                msg.setInformativeText(new_dir)
                msg.setWindowTitle("Success!")
                retval = msg.exec_()
            else:
                # get file
                d = QDialog()
                d.setWindowTitle(new_dir)
                d.resize(900,720)
                textbox = QPlainTextEdit(d)
                textbox.resize(880,700)
                textbox.setLineWrapMode(False)
                textbox.setPlainText(files.get_file(self.current_dir+new_dir, self.current_url))
                textbox.setReadOnly(True)
                d.setWindowModality(Qt.ApplicationModal)
                d.exec_()

    def on_combobox_change_testresults(self):
        # populate dataview
        self.current_url = str(self.comboBox1.currentText())
        dir_listing = files.get_directory_listing(self.current_dir, self.current_url)
        self.populateTree(dir_listing)
        pass
    
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)

        self.title = 'auto_un_annotator'
        self.left = 10
        self.top = 10
        self.width = 900
        self.height = 50
        self.initUI()
        self.BugLabel = QLabel("Enter Bug Number:", self)
        self.textBox1 = QLineEdit(self)
        self.textBox1.move(20, 20)
        self.textBox1.resize(50,40)

        #2nd textbox pop up
        self.textbox2 = QLineEdit(self)
        self.textbox2.move(20, 20)
        self.textbox2.resize(200,200)

        self.button2 = QPushButton('Retrieve', self)
        self.button2.clicked.connect(self.on_click_retrieve_button)
        self.button3 = QPushButton('Download', self)
        self.button3.clicked.connect(self.on_click_test)

        self.BugNumberLabel = QLabel("Bug # {} -TITLE HERE", self)
        self.freqlabel = QLabel("# Frequencies:", self)
        font = QFont()
        font.setPointSize(20)
        self.BugNumberLabel.setFont(font)
        self.TestLabel = QLabel("Test Links:", self)
        self.EntryTypeLabel = QLabel("Entry Type", self)
        self.comboBox1 = QComboBox(self)
        self.crlabel = QLabel("CR:",self)
        self.prlabel = QLabel("PR:", self)

        self.button = QPushButton('Compile Report', self)
        self.button.clicked.connect(self.on_click_report)
        self.button.setToolTip('This is an example button')
        self.textBox = QPlainTextEdit(self)
        self.textBox.move(250, 120)
        self.textBox.resize(10, 10)
        
        #mainLayout = QVBoxLayout()
        
        #self.setLayout(mainLayout)

        # create dynamic dataview widget
        self.dataGroupBox = QGroupBox("Directories")
        self.dirbox = QVBoxLayout()
        self.tree = QTreeView(self)
        self.dirbox.addWidget(self.tree)
        self.dataGroupBox.setLayout(self.dirbox)
        self.tree.doubleClicked.connect(self.select_dir)

        self.layout = QGridLayout()
        #tree layout

        self.layout.addWidget(self.BugLabel, 1, 0, 1, 5)
        self.layout.addWidget(self.textBox1, 1, 10, 1, 1)
        self.layout.addWidget(self.button2, 2, 10, 1, 1)
        
        self.setLayout(self.layout) 

        #self.show()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        #self.show()
        self.show()
        #time.sleep(.1)
    
    def populateTree(self, dir_listing):
        self.dataGroupBox.setTitle("Index of " + self.current_dir)
        root_model = QStandardItemModel()
        self.tree.setModel(root_model)
        for item in dir_listing:
            child_item = QStandardItem(item)
            root_model.invisibleRootItem().appendRow(child_item)

    def populateTestResults(self):
        # populate combobox
        self.comboBox1.clear()
        self.comboBox1.addItems(self.urls["TEST_RESULTS"])
        self.current_url = str(self.comboBox1.currentText())
        dir_listing = files.get_directory_listing(self.current_dir, self.current_url)
        self.current_dir = "/"
        self.populateTree(dir_listing)
        self.comboBox1.currentTextChanged.connect(self.on_combobox_change_testresults)

    def populateCR(self):
        # populate combobox
        pass

    def drawForm(self):
        self.left = 10
        self.top = 10
        self.width = 900
        self.height = 720
        self.initUI()

        #test button to show text
        self.layout.addWidget(self.comboBox1, 5, 1, 1, 1)
        self.layout.addWidget(self.BugLabel, 1, 0, 1, 5)
        self.layout.addWidget(self.textBox1, 1, 3, 1, 1)
        self.layout.addWidget(self.button2, 2, 3, 1, 1)
        self.layout.addWidget(self.button3, 10, 3, 1, 1)
        self.layout.addWidget(self.BugNumberLabel, 3, 0, 1, 5)
        self.layout.addWidget(self.freqlabel, 4, 0, 1, 5)
        self.layout.addWidget(self.textboxFreq, 4, 1, 1, 5)
        self.layout.addWidget(self.TestLabel, 5, 0, 1 ,5)
        #self.layout.addWidget(coreslabel, 5, 3, 1, 2)
        
        self.layout.addWidget(self.crlabel, 8, 0, 1, 5)
        self.layout.addWidget(self.prlabel, 9, 0, 1, 5)
        self.layout.addWidget(self.textboxCR, 8, 1, 1, 5)
        self.layout.addWidget(self.textboxPR, 9, 1, 1, 5)
        self.layout.addWidget(self.button, 10,0, 1, 1)
        self.layout.addWidget(self.dataGroupBox, 6, 0, 1, 5)
        
        self.setLayout(self.layout)

    @pyqtSlot()
    def on_click_retrieve_button(self):
        self.bug_data = bugs.get_bugs([("id",self.textBox1.text())])
        self.urls = files.get_test_urls(self.bug_data[0]["comments"])
        bug = self.textBox1.text()
        self.BugNumberLabel.setText("Bug {} - {}".format(bug, self.bug_data[0]["short_desc"]))
        self.num_frequencies = files.get_frequency_count(self.bug_data[0]["comments"])
        self.bug_type = self.bug_data[0]["cf_bug_type"]
        self.textboxCR = QLineEdit(self)
        self.textboxCR.setText(', '.join(self.urls["CR"]))
        self.textboxCR.setReadOnly(True)
        self.textboxPR = QLineEdit(self)
        self.textboxPR.setText(', '.join(self.urls["PR"]))
        self.textboxPR.setReadOnly(True)
        self.textboxFreq = QLineEdit(self)
        self.textboxFreq.setText(str(files.get_frequency_count(self.bug_data[0]["comments"])))
        self.textboxFreq.setReadOnly(True)
        self.populateTestResults()
        self.drawForm()
    
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
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    sys.exit(app.exec_())
