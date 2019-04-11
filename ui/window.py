import sys
import time
from .. import bugs
from PyQt5.QtWidgets import QApplication, QWidget, QApplication, QWidget, QPushButton, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import pyqtSlot

#only for button
#from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
#from PyQt5.QtCore import pyqtSlot


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
    bug = "000000"
    bug_data = {}
    
    def __init__(self, *args, **kwargs):
        QWidget.__init__(self, *args, **kwargs)

        self.title = 'auto_un_annotator'
        self.left = 10
        self.top = 10
        self.width = 900
        self.height = 720
        self.initUI()

        self.label1 = QLabel("Bug # {} -TITLE HERE", self)
        font = QFont()
        font.setPointSize(20)
        self.label1.setFont(font)
        self.label2 = QLabel("Entry Type", self)
        comboBox1 = QComboBox(self)
        comboBox1.addItem("Defect 1")
        self.label3 = QLabel("Logs", self)
        coreslabel = QLabel("Cores",self)
        self.label4 = QLabel("Possible Dupes", self)
        crlabel = QLabel("CR",self)
        prlabel = QLabel("PR:", self)

        button = QPushButton('PyQt5 button', self)
        button.clicked.connect(self.on_click)
        button.setToolTip('This is an example button')

        self.layout = QGridLayout()
        self.layout.addWidget(self.label1, 1, 0, 1, 5)
        self.layout.addWidget(self.label2, 2, 0, 1, 5)
        self.layout.addWidget(self.label3, 3, 0, 1 ,5)
        self.layout.addWidget(coreslabel, 3, 3, 1, 2)
        self.layout.addWidget(self.label4, 5, 0, 1,5)
        
        self.layout.addWidget(crlabel, 6, 0, 1, 5)
        self.layout.addWidget(prlabel, 7, 0, 1, 5)
        self.layout.addWidget(button, 9,0, 1, 1)
        self.layout.addWidget(comboBox1, 2, 1, 1, 1)
        
        self.setLayout(self.layout) 
        

        #self.show()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        #self.show()
        self.show()
        #time.sleep(.1)
        
    @pyqtSlot()
    def on_click(self):
        print('PyQt5 button click')
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Window()
    sys.exit(app.exec_())
