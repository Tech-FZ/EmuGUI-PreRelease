from uiScripts.ui_Win81SupportNearsEnd import Ui_Dialog
from PySide6.QtWidgets import *
from PySide6 import QtGui

class Win812012R2NearEOS(QDialog, Ui_Dialog):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("EmuGUI - OS Support")

        eolText = """
        Starting 11th November, 2025, your PC as it is right now will no longer be supported.
        You will need the following specifications for your host system to remain supported:
        - Windows 10 1607, Server 2016 or the latest version of your Linux distribution (amd64)
        - 4-threaded CPU
        - 8 GB of RAM your OS can share with running applications
        
        Please visit the GitHub repository to learn more.
        """
        
        try:
            self.setWindowIcon(QtGui.QIcon("EmuGUI.png"))

        except:
            pass
        
        self.connectSignalsSlots()
        self.label.setText(eolText)

    def connectSignalsSlots(self):
        self.pushButton.clicked.connect(self.close)