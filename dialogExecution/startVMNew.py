from PySide6.QtWidgets import *
from PySide6 import QtGui
from uiScripts.ui_StartVM_new import Ui_Dialog
import platform

if platform.system() == "Windows":
    import platformSpecific.windowsSpecific

else:
    import platformSpecific.unixSpecific
    import shlex
    
import sqlite3
import subprocess
from PySide6.QtCore import QDateTime
from random import randint
import magic
import translations.de
import translations.uk
import translations.en
import translations.fr
import translations.es
import translations.ro
import translations.be
import translations.cz
import translations.ru
import translations.pt
import translations.it
import translations.pl
import locale
import errors.errCodes
from dialogExecution.errDialog import ErrDialog
import services.pathfinder as pf
import errors.logman
import services.vm_data as vmd

class StartVmNewDialog(QDialog, Ui_Dialog):
    def __init__(self, vmdata, parent=None):
        self.logman = errors.logman.LogMan()
        self.logman.logFile = self.logman.setLogFile()
        
        try:
            super().__init__(parent)

        except:
            super().__init__()
            
        self.setupUi(self)
        self.exec_folder = pf.retrieveExecFolder()
        self.connectSignalsSlots()
        self.vmdata = vmd.VirtualMachineData(vmdata)
        
        self.architectures = [
            "i386", "x86_64", "ppc", "ppc64", "mips64", "mips64el",
            "mipsel", "mips", "aarch64", "arm", "sparc", "sparc64",
            "alpha", "riscv32", "riscv64"
        ]
        
        try:
            self.setWindowIcon(QtGui.QIcon(f"{self.exec_folder}EmuGUI.png"))

        except:
            pass

        if platform.system() == "Windows":
            self.connection = platformSpecific.windowsSpecific.setupWindowsBackend()
        
        else:
            self.connection = platformSpecific.unixSpecific.setupUnixBackend()
        
    def connectSignalsSlots(self):
        pass