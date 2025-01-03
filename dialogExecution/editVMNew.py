from PySide6.QtWidgets import *
from PySide6 import QtGui
from PySide6.QtCore import *
from uiScripts.ui_EditVM2 import Ui_Dialog
import sqlite3
import platform

if platform.system() == "Windows":
    import platformSpecific.windowsSpecific

else:
    import platformSpecific.unixSpecific
    
import subprocess
from dialogExecution.vmExistsDialog import VmAlreadyExistsDialog
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
import errors.logman
import errors.logID
import errors.errCodes
from dialogExecution.errDialog import ErrDialog
import plugins.pluginmgr.hw_reader as hwpr # HWPR = HardWare Plug-in Reader
import services.pathfinder as pf
import services.vm_data as vmd
from datetime import datetime

class EditVMNewDialog(QDialog, Ui_Dialog):
    def __init__(self, vmdata, permanent, parent=None):
        try:
            super().__init__(parent)

        except:
            super().__init__()
            
        self.logman = errors.logman.LogMan()
        self.logman.logFile = self.logman.setLogFile()
        self.exec_folder = pf.retrieveExecFolder()
        self.setupUi(self)
        self.connectSignalsSlots()
        self.tabWidget.setCurrentIndex(0)
        self.hw_plugins = hwpr.read_hw_plugin()
        self.vmdata = vmdata
        self.permanent = permanent
        #self.vmSpecs = self.readTempVmFile()
        self.fillForm()
        self.langDetect()
        
        try:
            self.setWindowIcon(QtGui.QIcon(f"{self.exec_folder}EmuGUI.png"))

        except:
            pass

        self.logman.writeToLogFile(
            f"{errors.errCodes.errCodes[48]}: GUI \"Edit virtual machine\" opened successfully"
            )

    def connectSignalsSlots(self):
        self.btn_cancel.clicked.connect(self.close)
        self.btn_ok.clicked.connect(self.modeSelector)
        self.cb_vhdu.currentTextChanged.connect(self.vhdAddingChange)
        self.cb_arch.currentTextChanged.connect(self.archChanged)
        self.btn_vhdp.clicked.connect(self.vhdBrowseLocation)
        self.btn_biosf.clicked.connect(self.extBiosFileLocation)
        self.btn_kernel.clicked.connect(self.linuxKernelBrowseLocation)
        self.btn_initrd.clicked.connect(self.linuxInitridBrowseLocation)
        self.chb_rtc.checkStateChanged.connect(self.rtcTimeCheckboxHandler)
        self.btn_floppy.clicked.connect(self.floppyLocation)
        self.btn_cd1.clicked.connect(self.cd1Location)
        self.btn_cd2.clicked.connect(self.cd2Location)

        # For new and existing
        self.le_vhdp.setEnabled(True)
        self.btn_vhdp.setEnabled(True)

        # For new
        self.cb_vhdf.setEnabled(False)
        self.sb_maxsize.setEnabled(False)
        self.cb_hddc.setEnabled(False)

        self.vhdAddingChange()
    
    def langDetect(self):
        select_language = """
        SELECT name, value FROM settings
        WHERE name = "lang";
        """

        if platform.system() == "Windows":
            connection = platformSpecific.windowsSpecific.setupWindowsBackend()
        
        else:
            connection = platformSpecific.unixSpecific.setupUnixBackend()

        cursor = connection.cursor()

        try:
            cursor.execute(select_language)
            connection.commit()
            result = cursor.fetchall()

            # Language modes
            # system: language of OS
            # en: English
            # de: German
            langmode = "system"

            try:
                qemu_img_slot = str(result[0])                 

                if result[0][1] == "en":
                    langmode = "en"

                elif result[0][1] == "de":
                    langmode = "de"

                elif result[0][1] == "uk":
                    langmode = "uk"

                elif result[0][1] == "fr":
                    langmode = "fr"

                elif result[0][1] == "es":
                    langmode = "es"

                elif result[0][1] == "ro":
                    langmode = "ro"

                elif result[0][1] == "ru":
                    langmode = "ru"

                elif result[0][1] == "be":
                    langmode = "be"

                elif result[0][1] == "cz":
                    langmode = "cz"

                elif result[0][1] == "pt":
                    langmode = "pt"

                elif result[0][1] == "pl":
                    langmode = "pl"

                elif result[0][1] == "it":
                    langmode = "it"

                elif result[0][1] == "system":
                    langmode = "system"

                self.setLanguage(langmode)
                print("The query was executed successfully. The language slot already is in the database.")

                self.logman.writeToLogFile(
                    f"{errors.errCodes.errCodes[49]}: Language \"{langmode}\" taken from database successfully"
                )

            except:
                langmode = "system"

                self.logman.writeToLogFile(
                    f"{errors.errCodes.errCodes[50]}: Language could not be taken from database. Trying to use system language."
                )

                self.setLanguage(langmode)
                print("The query was executed successfully. The language slot has been created.")
        
        except sqlite3.Error as e:
            print(f"The SQLite module encountered an error: {e}.")

            self.logman.writeToLogFile(
                f"{errors.errCodes.errCodes[50]}: Could not connect to the database to detect the language. Trying to use system language."
                )

            self.setLanguage("system")

    def setLanguage(self, langmode):
        if langmode == "system" or langmode == None:
            languageToUse = locale.getlocale()[0]

        else:
            languageToUse = langmode

        print(languageToUse)

        if languageToUse != None:
            if languageToUse.startswith("de"):
                translations.de.translateEditVMDE(self, self.vmdata.vm_name)

            elif languageToUse.startswith("uk"):
                translations.uk.translateEditVMUK(self, self.vmdata.vm_name)

            elif languageToUse.startswith("fr"):
                translations.fr.translateEditVMFR(self, self.vmdata.vm_name)

            elif languageToUse.startswith("es"):
                translations.es.translateEditVMES(self, self.vmdata.vm_name)

            elif languageToUse.startswith("ro"):
                translations.ro.translateEditVMRO(self, self.vmdata.vm_name)

            elif languageToUse.startswith("ru"):
                translations.ru.translateEditVMRU(self, self.vmdata.vm_name)

            elif languageToUse.startswith("be"):
                translations.be.translateEditVMBE(self, self.vmdata.vm_name)

            elif languageToUse.startswith("cz"):
                translations.cz.translateEditVMCZ(self, self.vmdata.vm_name)

            elif languageToUse.startswith("pt"):
                translations.pt.translateEditVMPT(self, self.vmdata.vm_name)

            elif languageToUse.startswith("pl"):
                translations.pl.translateEditVMPL(self, self.vmdata.vm_name)
            
            elif languageToUse.startswith("it"):
                translations.it.translateEditVMIT(self, self.vmdata.vm_name)

            else:
                translations.en.translateEditVMEN(self, self.vmdata.vm_name)

            self.logman.writeToLogFile(
                f"{errors.errCodes.errCodes[52]}: Language \"{languageToUse}\" set successfully."
                )
        
        else:
            self.logman.writeToLogFile(
                f"{errors.errCodes.errCodes[51]}: The language couldn't be set via the locale module or the database. Trying to access temporary files."
                )
            
            if platform.system() == "Windows":
                langfile = platformSpecific.windowsSpecific.windowsLanguageFile()
            
            else:
                langfile = platformSpecific.unixSpecific.unixLanguageFile()
            
            try:
                with open(langfile, "r+") as language:
                    languageContent = language.readlines()
                    languageToUse = languageContent[0].replace("\n", "")
                
                if languageToUse != None:
                    if languageToUse.startswith("de"):
                        translations.de.translateEditVMDE(self, self.vmdata.vm_name)

                    elif languageToUse.startswith("uk"):
                        translations.uk.translateEditVMUK(self, self.vmdata.vm_name)

                    elif languageToUse.startswith("fr"):
                        translations.fr.translateEditVMFR(self, self.vmdata.vm_name)

                    elif languageToUse.startswith("es"):
                        translations.es.translateEditVMES(self, self.vmdata.vm_name)

                    elif languageToUse.startswith("ro"):
                        translations.ro.translateEditVMRO(self, self.vmdata.vm_name)

                    elif languageToUse.startswith("ru"):
                        translations.ru.translateEditVMRU(self, self.vmdata.vm_name)

                    elif languageToUse.startswith("be"):
                        translations.be.translateEditVMBE(self, self.vmdata.vm_name)

                    elif languageToUse.startswith("cz"):
                        translations.cz.translateEditVMCZ(self, self.vmdata.vm_name)

                    elif languageToUse.startswith("pt"):
                        translations.pt.translateEditVMPT(self, self.vmdata.vm_name)

                    elif languageToUse.startswith("pl"):
                        translations.pl.translateEditVMPL(self, self.vmdata.vm_name)

                    elif languageToUse.startswith("it"):
                        translations.it.translateEditVMIT(self, self.vmdata.vm_name)

                    else:
                        translations.en.translateEditVMEN(self, self.vmdata.vm_name)

                    self.logman.writeToLogFile(
                        f"{errors.errCodes.errCodes[52]}: Language \"{languageToUse}\" set successfully."
                    )
            
            except:
                print("Translation can't be figured out. Using English language.")
                translations.en.translateEditVMEN(self, self.vmdata.vm_name)

                if platform.system() == "Windows":
                    errorFile = platformSpecific.windowsSpecific.windowsErrorFile()
        
                else:
                    errorFile = platformSpecific.unixSpecific.unixErrorFile()

                with open(errorFile, "w+") as errCodeFile:
                    errCodeFile.write(errors.errCodes.errCodes[11])

                self.logman.writeToLogFile(
                    f"{errors.errCodes.errCodes[11]}: The desired language couldn't be applied and English must be used."
                )

                dialog = ErrDialog(self)
                dialog.exec()

    def vhdAddingChange(self):
        with open(f"{self.exec_folder}translations/createnewvhd.txt", "r+", encoding="utf8") as creNewVhdFile:
            creNewVhdContent = creNewVhdFile.read()

        with open(f"{self.exec_folder}translations/addexistingvhd.txt", "r+", encoding="utf8") as addExistVhdFile:
            addExistVhdContent = addExistVhdFile.read()

        with open(f"{self.exec_folder}translations/addnovhd.txt", "r+", encoding="utf8") as noVhdFile:
            noVhdContent = noVhdFile.read()

        if creNewVhdContent.__contains__(self.cb_vhdu.currentText()):
            # For new and existing
            self.le_vhdp.setEnabled(True)
            self.btn_vhdp.setEnabled(True)
            self.cb_hddc.setEnabled(True)

            # For new
            self.cb_vhdf.setEnabled(True)
            self.sb_maxsize.setEnabled(True)

        elif addExistVhdContent.__contains__(self.cb_vhdu.currentText()):
            # For new and existing
            self.le_vhdp.setEnabled(True)
            self.btn_vhdp.setEnabled(True)
            self.cb_hddc.setEnabled(True)

            # For new
            self.cb_vhdf.setEnabled(False)
            self.sb_maxsize.setEnabled(False)

        elif noVhdContent.__contains__(self.cb_vhdu.currentText()):
            # For new and existing
            self.le_vhdp.setEnabled(False)
            self.btn_vhdp.setEnabled(False)
            self.cb_hddc.setEnabled(False)

            # For new
            self.cb_vhdf.setEnabled(False)
            self.sb_maxsize.setEnabled(False)

    def vhdBrowseLocation(self):
        with open(f"{self.exec_folder}translations/createnewvhd.txt", "r+", encoding="utf8") as creNewVhdFile:
            creNewVhdContent = creNewVhdFile.read()

        with open(f"{self.exec_folder}translations/addexistingvhd.txt", "r+", encoding="utf8") as addExistVhdFile:
            addExistVhdContent = addExistVhdFile.read()

        if creNewVhdContent.__contains__(self.comboBox_2.currentText()):        
            filename, filter = QFileDialog.getSaveFileName(parent=self, caption='Save VHD file', dir='.', filter='Hard disk file (*.img);;QCOW2 disk image (*.qcow2);;QCOW disk image (*.qcow);;VirtualBox disk image (*.vdi);;VMware disk file (*.vmdk);;Virtual hard disk file with extra features (*.vhdx);;Virtual PC hard disks (*.vpc);;All files (*.*)')

            if filename:
                self.le_vhdp.setText(filename)

        elif addExistVhdContent.__contains__(self.comboBox_2.currentText()):        
            filename, filter = QFileDialog.getOpenFileName(parent=self, caption='Open VHD file', dir='.', filter='Hard disk file (*.img);;QCOW2 disk image (*.qcow2);;QCOW disk image (*.qcow);;VirtualBox disk image (*.vdi);;VMware disk file (*.vmdk);;Virtual hard disk file with extra features (*.vhdx);;Virtual PC hard disks (*.vpc);;All files (*.*)')

            if filename:
                self.le_vhdp.setText(filename)
                
    def rtcTimeCheckboxHandler(self):
        if self.chb_rtc.isChecked():
            self.dtb_rtc.setEnabled(True)
            
        else:
            self.dtb_rtc.setEnabled(False)
            
    def floppyLocation(self):
        filename, filter = QFileDialog.getOpenFileName(parent=self, caption='Select floppy disk', dir='.', filter='Floppy image (*.img);;Floppy file (*.flp);;Floppy image (*.ima);;All files (*.*)')

        if filename:
            self.le_floppy.setText(filename)

    def archChanged(self):
        while 1 < self.cb_machine.count():
            self.cb_machine.removeItem(1)

        while 1 < self.cb_cpu.count():
            self.cb_cpu.removeItem(1)

        if self.cb_arch.currentText() == "i386" or self.cb_arch.currentText() == "x86_64":
            for plugin in self.hw_plugins:
                try:
                    self.cb_machine.addItems(plugin["x86_machines"])

                except:
                    pass

                try:
                    self.cb_cpu.addItems(plugin["x86_cpus"])

                except:
                    pass

        elif self.cb_arch.currentText() == "mipsel":
            for plugin in self.hw_plugins:
                try:
                    self.cb_machine.addItems(plugin["mipsel_machines"])

                except:
                    pass

                try:
                    self.cb_cpu.addItems(plugin["mipsel_cpus"])

                except:
                    pass
        
        elif self.cb_arch.currentText() == "ppc" or self.cb_arch.currentText() == "ppc64":
            for plugin in self.hw_plugins:
                try:
                    self.cb_machine.addItems(plugin["ppc_machines"])

                except:
                    pass

                try:
                    self.cb_cpu.addItems(plugin["ppc_cpus"])

                except:
                    pass

        elif self.cb_arch.currentText() == "mips64el":
            for plugin in self.hw_plugins:
                try:
                    self.cb_machine.addItems(plugin["mips64el_machines"])

                except:
                    pass

                try:
                    self.cb_cpu.addItems(plugin["mips64el_cpus"])

                except:
                    pass
                
        elif self.cb_arch.currentText() == "aarch64":
            for plugin in self.hw_plugins:
                try:
                    self.cb_machine.addItems(plugin["aarch64_machines"])

                except:
                    pass

                try:
                    self.cb_cpu.addItems(plugin["aarch64_cpus"])

                except:
                    pass

        elif self.cb_arch.currentText() == "arm":
            for plugin in self.hw_plugins:
                try:
                    self.cb_machine.addItems(plugin["arm_machines"])

                except:
                    pass

                try:
                    self.cb_cpu.addItems(plugin["arm_cpus"])

                except:
                    pass

        elif self.cb_arch.currentText() == "sparc":
            for plugin in self.hw_plugins:
                try:
                    self.cb_machine.addItems(plugin["sparc_machines"])

                except:
                    pass

                try:
                    self.cb_cpu.addItems(plugin["sparc_cpus"])

                except:
                    pass

        elif self.cb_arch.currentText() == "sparc64":
            for plugin in self.hw_plugins:
                try:
                    self.cb_machine.addItems(plugin["sparc64_machines"])

                except:
                    pass

                try:
                    self.cb_cpu.addItems(plugin["sparc64_cpus"])

                except:
                    pass

        elif self.cb_arch.currentText() == "mips":
            for plugin in self.hw_plugins:
                try:
                    self.cb_machine.addItems(plugin["mips_machines"])

                except:
                    pass

                try:
                    self.cb_cpu.addItems(plugin["mips_cpus"])

                except:
                    pass

        elif self.cb_arch.currentText() == "mips64":
            for plugin in self.hw_plugins:
                try:
                    self.cb_machine.addItems(plugin["mips64_machines"])

                except:
                    pass

                try:
                    self.cb_cpu.addItems(plugin["mips64_cpus"])

                except:
                    pass

        elif self.cb_arch.currentText() == "alpha":
            for plugin in self.hw_plugins:
                try:
                    self.cb_machine.addItems(plugin["alpha_machines"])

                except:
                    pass

                try:
                    self.cb_cpu.addItems(plugin["alpha_cpus"])

                except:
                    pass

        elif self.cb_arch.currentText() == "riscv32":
            for plugin in self.hw_plugins:
                try:
                    self.cb_machine.addItems(plugin["riscv32_machines"])

                except:
                    pass

                try:
                    self.cb_cpu.addItems(plugin["riscv32_cpus"])

                except:
                    pass

        elif self.cb_arch.currentText() == "riscv64":
            for plugin in self.hw_plugins:
                try:
                    self.cb_machine.addItems(plugin["riscv64_machines"])

                except:
                    pass

                try:
                    self.cb_cpu.addItems(plugin["riscv64_cpus"])

                except:
                    pass

    def extBiosFileLocation(self):
        filename, filter = QFileDialog.getOpenFileName(parent=self, caption='Select BIOS file', dir='.', filter='BIN files (*.bin);;All files (*.*)')

        if filename:
            self.le_biosf.setText(filename)

    def linuxKernelBrowseLocation(self):
        filename, filter = QFileDialog.getOpenFileName(parent=self, caption='Select Linux kernel', dir='.', filter='All files (*.*)')

        if filename:
            self.le_kernel.setText(filename)

    def linuxInitridBrowseLocation(self):
        filename, filter = QFileDialog.getOpenFileName(parent=self, caption='Select Linux initrid image', dir='.', filter='IMG files (*.img);;All files (*.*)')

        if filename:
            self.le_initrd.setText(filename)
            
    def cd1Location(self):
        filename, filter = QFileDialog.getOpenFileName(parent=self, caption='Select first ISO file', dir='.', filter='ISO image (*.iso);;All files (*.*)')

        if filename:
            self.le_cd1.setText(filename)
            
    def cd2Location(self):
        filename, filter = QFileDialog.getOpenFileName(parent=self, caption='Select second ISO file', dir='.', filter='ISO image (*.iso);;All files (*.*)')

        if filename:
            self.le_cd2.setText(filename)

    def setupCB(self):
        for plugin in self.hw_plugins:
            try:
                self.cb_vga.addItems(plugin["graphics"])

            except:
                pass

            try:
                self.cb_net.addItems(plugin["networking"])

            except:
                pass

            try:
                self.cb_sound.addItems(plugin["sound"])

            except:
                pass

            try:
                self.cb_usb.addItems(plugin["usb_controllers"])

            except:
                pass

    def fillForm(self):
        try:
            with open(f"{self.exec_folder}translations/createnewvhd.txt", "r+", encoding="utf8") as creNewVhdFile:
                creNewVhdContent = creNewVhdFile.read()

            with open(f"{self.exec_folder}translations/addexistingvhd.txt", "r+", encoding="utf8") as addExistVhdFile:
                addExistVhdContent = addExistVhdFile.read()

            with open(f"{self.exec_folder}translations/addnovhd.txt", "r+", encoding="utf8") as noVhdFile:
                noVhdContent = noVhdFile.read()

            with open(f"{self.exec_folder}translations/letqemudecide.txt", "r+", encoding="utf8") as letQemuDecideFile:
                letQemuDecideContent = letQemuDecideFile.read()
            
            self.le_name.setText(self.vmdata.vm_name)
            
            i = 0
            
            while i < self.cb_arch.count():
                if self.cb_arch.itemText(i) == self.vmdata.arch:
                    self.cb_arch.setCurrentIndex(i)
                    break
                
                i += 1
                
            self.archChanged()
            
            i = 0
            
            while i < self.cb_machine.count():
                if letQemuDecideContent.__contains__(self.cb_machine.itemText(i)):
                    if self.vmdata.machine == "Let QEMU decide":
                        self.cb_machine.setCurrentIndex(i)
                        break
                    
                elif self.cb_machine.itemText(i) == self.vmdata.machine:
                    self.cb_machine.setCurrentIndex(i)
                    break
                
                i += 1
                
            i = 0
            
            while i < self.cb_cpu.count():
                if letQemuDecideContent.__contains__(self.cb_cpu.itemText(i)):
                    if self.vmdata.cpu == "Let QEMU decide":
                        self.cb_cpu.setCurrentIndex(i)
                        break
                    
                elif self.cb_cpu.itemText(i) == self.vmdata.machine:
                    self.cb_cpu.setCurrentIndex(i)
                    break
                
                i += 1
                
            try:
                self.sb_cpuc.setValue(int(self.vmdata.cores))
                
            except:
                if platform.system() == "Windows":
                    errorFile = platformSpecific.windowsSpecific.windowsErrorFile()
        
                else:
                    errorFile = platformSpecific.unixSpecific.unixErrorFile()

                with open(errorFile, "w+") as errCodeFile:
                    errCodeFile.write(errors.errCodes.errCodes[62])

                self.logman.writeToLogFile(
                            f"{errors.errCodes.errCodes[62]}: The CPU cores variable could not be converted. Please set it up yourself."
                            )

                dialog = ErrDialog(self)
                dialog.exec()
            
            try:    
                self.sb_ram.setValue(int(self.vmdata.ram))
                
            except:
                if platform.system() == "Windows":
                    errorFile = platformSpecific.windowsSpecific.windowsErrorFile()
        
                else:
                    errorFile = platformSpecific.unixSpecific.unixErrorFile()

                with open(errorFile, "w+") as errCodeFile:
                    errCodeFile.write(errors.errCodes.errCodes[61])

                self.logman.writeToLogFile(
                            f"{errors.errCodes.errCodes[61]}: The RAM variable could not be converted. Please set it up yourself."
                            )

                dialog = ErrDialog(self)
                dialog.exec()
                
            if self.vmdata.hda != "NULL" and self.vmdata.hda != "":
                self.le_vhdp.setText(self.vmdata.hda)
                i = 0
                
                while i < self.cb_vhdu.count():
                    if addExistVhdContent.__contains__(self.cb_vhdu.itemText(i)):
                        self.cb_vhdu.setCurrentIndex(i)
                        break
                    
                    i += 1
                    
            else:
                i = 0
                
                while i < self.cb_vhdu.count():
                    if noVhdContent.__contains__(self.cb_vhdu.itemText(i)):
                        self.cb_vhdu.setCurrentIndex(i)
                        break
                    
                    i += 1
                    
            self.vhdAddingChange()
            self.setupCB()
            
            i = 0
            
            while i < self.cb_hddc.count():
                if self.vmdata.hda_control == "Let QEMU decide":
                    if letQemuDecideContent.__contains__(self.cb_hddc.itemText(i)):
                        self.cb_hddc.setCurrentIndex(i)
                        break
                    
                elif self.cb_hddc.itemText(i) == self.vmdata.hda_control:
                    self.cb_hddc.setCurrentIndex(i)
                    break
                
                i += 1
            
            self.le_cd1.setText(self.vmdata.cd1)
                
            i = 0
            
            while i < self.cb_cdc1.count():
                if self.vmdata.cd_control1 == "Let QEMU decide":
                    if letQemuDecideContent.__contains__(self.cb_cdc1.itemText(i)):
                        self.cb_cdc1.setCurrentIndex(i)
                        break
                    
                elif self.cb_cdc1.itemText(i) == self.vmdata.cd_control1:
                    self.cb_cdc1.setCurrentIndex(i)
                    break
                
                i += 1
            
            self.le_cd2.setText(self.vmdata.cd2)
            
            i = 0
            
            while i < self.cb_cdc2.count():
                if self.vmdata.cd_control2 == "Let QEMU decide":
                    if letQemuDecideContent.__contains__(self.cb_cdc2.itemText(i)):
                        self.cb_cdc2.setCurrentIndex(i)
                        break
                    
                elif self.cb_cdc2.itemText(i) == self.vmdata.cd_control2:
                    self.cb_cdc2.setCurrentIndex(i)
                    break
                
                i += 1
            
            self.le_floppy.setText(self.vmdata.floppy)
            
            i = 0
            
            while i < self.cb_bootfrom.count():
                if self.vmdata.bootfrom == "Let QEMU decide":
                    if letQemuDecideContent.__contains__(self.cb_bootfrom.itemText(i)):
                        self.cb_bootfrom.setCurrentIndex(i)
                        break
                    
                elif self.cb_bootfrom.itemText(i) == self.vmdata.bootfrom:
                    self.cb_bootfrom.setCurrentIndex(i)
                    break
                
                i += 1
            
            i = 0
            
            while i < self.cb_vga.count():
                if self.vmdata.vga == "Let QEMU decide":
                    if letQemuDecideContent.__contains__(self.cb_vga.itemText(i)):
                        self.cb_vga.setCurrentIndex(i)
                        break
                    
                elif self.cb_vga.itemText(i) == self.vmdata.vga:
                    self.cb_vga.setCurrentIndex(i)
                    break
                
                i += 1
                
            i = 0
            
            while i < self.cb_net.count():
                if self.cb_net.itemText(i) == self.vmdata.net:
                    self.cb_net.setCurrentIndex(i)
                    break
                
                i += 1
                
            # BIOS stuff
            self.le_biosloc.setText(self.vmdata.biosdir)
            self.le_biosf.setText(self.vmdata.biosfile)
            
            self.le_addargs.setText(self.vmdata.addargs)
            
            i = 0
            
            while i < self.cb_sound.count():
                if self.cb_sound.itemText(i) == self.vmdata.sound:
                    self.cb_sound.setCurrentIndex(i)
                    break
                
                i += 1
                
            # Linux stuff
            self.le_kernel.setText(self.vmdata.kernel)
            self.le_initrd.setText(self.vmdata.initrd)
            self.le_cmd.setText(self.vmdata.linuxcmd)
            
            i = 0
            
            while i < self.cb_mouse.count():
                if self.cb_mouse.itemText(i) == self.vmdata.mouse:
                    self.cb_mouse.setCurrentIndex(i)
                    break
                
                i += 1
                
            i = 0
            
            while i < self.cb_kbdtype.count():
                if self.cb_kbdtype.itemText(i) == self.vmdata.kbd:
                    self.cb_kbdtype.setCurrentIndex(i)
                    break
                
                i += 1
                
            i = 0
            
            while i < self.cb_kbdlayout.count():
                if self.cb_kbdlayout.itemText(i) == self.vmdata.kbdlayout:
                    self.cb_kbdlayout.setCurrentIndex(i)
                    break
                
                i += 1
                
            self.chb_usb.setChecked(str(self.vmdata.usb_support) == "1")
            
            i = 0
            
            while i < self.cb_usb.count():
                if self.cb_usb.itemText(i) == self.vmdata.usb_controller:
                    self.cb_usb.setCurrentIndex(i)
                    break
                
                i += 1
                
            i = 0
            
            while i < self.cb_accel.count():
                if self.vmdata.hwaccel == "HAXM":
                    if self.cb_accel.itemText(i) == "HAXM (depreciated)":
                        self.cb_accel.setCurrentIndex(i)
                        break
                    
                elif self.cb_accel.itemText(i) == self.vmdata.hwaccel:
                    self.cb_accel.setCurrentIndex(i)
                    break
                
                i += 1
                
            if self.vmdata.timemgr == "system":
                self.chb_rtc.setChecked(True)
                
            else:
                date_format = "%Y-%m-%dT%H-%M-%S"
                
                try:
                    date_prop = datetime.strptime(self.vmdata.timemgr, date_format)
                    date_qtcompatible = QDate(y=date_prop.year, m=date_prop.month, d=date_prop.day)
                    time_qtcompatible = QTime(h=date_prop.hour, m=date_prop.minute, s=date_prop.second)
                    self.dtb_rtc.setDateTime(QDateTime(date=date_qtcompatible, time=time_qtcompatible))
                    
                except:
                    if platform.system() == "Windows":
                        errorFile = platformSpecific.windowsSpecific.windowsErrorFile()
        
                    else:
                        errorFile = platformSpecific.unixSpecific.unixErrorFile()

                    with open(errorFile, "w+") as errCodeFile:
                        errCodeFile.write(errors.errCodes.errCodes[63])

                    self.logman.writeToLogFile(
                                f"{errors.errCodes.errCodes[63]}: The datetime variable could not be converted. Please set it up yourself."
                                )

                    dialog = ErrDialog(self)
                    dialog.exec()
            
        except OSError as ex:
            if platform.system() == "Windows":
                errorFile = platformSpecific.windowsSpecific.windowsErrorFile()
        
            else:
                errorFile = platformSpecific.unixSpecific.unixErrorFile()

            with open(errorFile, "w+") as errCodeFile:
                errCodeFile.write(errors.errCodes.errCodes[59])

            self.logman.writeToLogFile(
                        f"{errors.errCodes.errCodes[59]}: The files required to initialise the combo boxes could not be read: \"{ex}\""
                        )

            dialog = ErrDialog(self)
            dialog.exec()
            
        except Exception as ex:
            if platform.system() == "Windows":
                errorFile = platformSpecific.windowsSpecific.windowsErrorFile()
        
            else:
                errorFile = platformSpecific.unixSpecific.unixErrorFile()

            with open(errorFile, "w+") as errCodeFile:
                errCodeFile.write(errors.errCodes.errCodes[60])

            self.logman.writeToLogFile(
                        f"{errors.errCodes.errCodes[60]}: An error previously unknown to the EmuGUI developers occured: \"{ex}\""
                        )

            dialog = ErrDialog(self)
            dialog.exec()

    """
    def readTempVmFile(self):
        with open(f"{self.exec_folder}translations/createnewvhd.txt", "r+", encoding="utf8") as creNewVhdFile:
            creNewVhdContent = creNewVhdFile.read()

        with open(f"{self.exec_folder}translations/addexistingvhd.txt", "r+", encoding="utf8") as addExistVhdFile:
            addExistVhdContent = addExistVhdFile.read()

        with open(f"{self.exec_folder}translations/addnovhd.txt", "r+", encoding="utf8") as noVhdFile:
            noVhdContent = noVhdFile.read()

        with open(f"{self.exec_folder}translations/letqemudecide.txt", "r+", encoding="utf8") as letQemuDecideFile:
            letQemuDecideContent = letQemuDecideFile.read()

        # Searching temporary files
        if platform.system() == "Windows":
            tempVmDef = platformSpecific.windowsSpecific.windowsTempVmStarterFile()
        
        else:
            tempVmDef = platformSpecific.unixSpecific.unixTempVmStarterFile()

        vmSpecs = []

        with open(tempVmDef, "r+") as tempVmDefFile:
            vmSpecsRaw = tempVmDefFile.readlines()

        for vmSpec in vmSpecsRaw:
            vmSpecNew = vmSpec.replace("\n", "")
            vmSpecs.append(vmSpecNew)

        # Setting VM variables

        self.le_name.setText(vmdata.vm_name)
        self.setWindowTitle(f"EmuGUI - Edit {vmdata.vm_name}")

        i = 0

        while i < self.cb_arch.count():
            if self.cb_arch.itemText(i) == vmSpecs[1]:
                self.cb_arch.setCurrentIndex(i)
                break

            i += 1

        self.archChanged()

        i = 0

        while i < self.cb_machine.count():
            if letQemuDecideContent.__contains__(self.cb_machine.itemText(i)):
                if vmSpecs[2] == "Let QEMU decide":
                    self.cb_machine.setCurrentIndex(i)
                    break

            elif self.cb_machine.itemText(i) == vmSpecs[2]:
                self.cb_machine.setCurrentIndex(i)
                break

            i += 1

        i = 0

        while i < self.cb_cpu.count():
            if letQemuDecideContent.__contains__(self.cb_cpu.itemText(i)):
                if vmSpecs[3] == "Let QEMU decide":
                    self.cb_cpu.setCurrentIndex(i)
                    break

            if self.cb_cpu.itemText(i) == vmSpecs[3]:
                self.cb_cpu.setCurrentIndex(i)
                break

            i += 1

        self.sb_ram.setValue(int(vmSpecs[4]))

        if vmSpecs[5] != "NULL":
            self.le_vhdp.setText(vmSpecs[5])
            i = 0

            while i < self.cb_vhdu.count():
                if addExistVhdContent.__contains__(self.cb_vhdu.itemText(i)): #self.comboBox_2.itemText(i) == "Add existing virtual hard drive" or self.comboBox_2.itemText(i) == "Existierende virtuelle Festplatte anfügen":
                    self.cb_vhdu.setCurrentIndex(i)
                    break

                i += 1

        else:
            i = 0

            while i < self.cb_vhdu.count():
                if noVhdContent.__contains__(self.cb_vhdu.itemText(i)): #self.comboBox_2.itemText(i) == "Don't add a virtual hard drive" or self.comboBox_2.itemText(i) == "Keine virtuelle Festplatte anfügen":
                    self.cb_vhdu.setCurrentIndex(i)
                    break

                i += 1

        self.vhdAddingChange()
        self.setupCB()

        i = 0

        while i < self.cb_vga.count():
            if vmSpecs[6] == "Let QEMU decide":
                if letQemuDecideContent.__contains__(self.cb_vga.itemText(i)):
                    self.cb_vga.setCurrentIndex(i)
                    break

            elif self.cb_vga.itemText(i) == vmSpecs[6]:
                self.cb_vga.setCurrentIndex(i)
                break

            i += 1

        i = 0

        while i < self.cb_net.count():
            if self.cb_net.itemText(i) == vmSpecs[7]:
                self.cb_net.setCurrentIndex(i)
                break

            i += 1

        if vmSpecs[8] == "1":
            self.checkBox_2.setChecked(True)

        self.le_biosloc.setText(vmSpecs[10])

        if vmSpecs[9] == "1":
            self.checkBox_3.setChecked(True)

        self.le_addargs.setText(vmSpecs[11])

        i = 0

        while i < self.cb_sound.count():
            if self.cb_sound.itemText(i) == vmSpecs[12]:
                self.cb_sound.setCurrentIndex(i)
                break

            i += 1

        self.le_kernel.setText(vmSpecs[13])
        self.le_initrd.setText(vmSpecs[14])
        self.le_cmd.setText(vmSpecs[15])

        i = 0

        while i < self.cb_mouse.count():
            if self.cb_mouse.itemText(i) == vmSpecs[16]:
                self.cb_mouse.setCurrentIndex(i)
                break

            i += 1

        self.le_biosf.setText(vmSpecs[18])
        self.sb_cpuc.setValue(int(vmSpecs[17]))

        i = 0

        while i < self.cb_kbdtype.count():
            if self.cb_kbdtype.itemText(i) == vmSpecs[19]:
                self.cb_kbdtype.setCurrentIndex(i)
                break

            i += 1

        if vmSpecs[20] == "1":
            self.chb_usb.setChecked(True)

        i = 0

        while i < self.cb_usb.count():
            if self.cb_usb.itemText(i) == vmSpecs[21]:
                self.cb_usb.setCurrentIndex(i)
                break

            i += 1

        i = 0

        while i < self.cb_kbdlayout.count():
            if self.cb_kbdlayout.itemText(i) == vmSpecs[22]:
                self.cb_kbdlayout.setCurrentIndex(i)
                break

            i += 1

        i = 0

        while i < self.cb_accel.count():
            if vmSpecs[23] == "HAXM":
                if self.cb_accel.itemText(i) == "HAXM (depreciated)":
                    self.cb_accel.setCurrentIndex(i)
                    break

            else:
                if self.cb_accel.itemText(i) == vmSpecs[23]:
                    self.cb_accel.setCurrentIndex(i)
                    break

            i += 1

        i = 0

        while i < self.cb_cdc1.count():
            if vmSpecs[24] == "Let QEMU decide":
                if letQemuDecideContent.__contains__(self.cb_cdc1.itemText(i)):
                    self.cb_cdc1.setCurrentIndex(i)
                    break

            elif self.cb_cdc1.itemText(i) == vmSpecs[24]:
                self.cb_cdc1.setCurrentIndex(i)
                break

            i += 1

        i = 0

        while i < self.cb_cdc2.count():
            if vmSpecs[25] == "Let QEMU decide":
                if letQemuDecideContent.__contains__(self.cb_cdc2.itemText(i)):
                    self.cb_cdc2.setCurrentIndex(i)
                    break

            elif self.cb_cdc2.itemText(i) == vmSpecs[25]:
                self.cb_cdc2.setCurrentIndex(i)
                break

            i += 1
            
        i = 0

        while i < self.cb_hddc.count():
            if vmSpecs[26] == "Let QEMU decide":
                if letQemuDecideContent.__contains__(self.cb_hddc.itemText(i)):
                    self.cb_hddc.setCurrentIndex(i)
                    break

            elif self.cb_hddc.itemText(i) == vmSpecs[25]:
                self.cb_hddc.setCurrentIndex(i)
                break

            i += 1
        
        return vmSpecs
    """
    
    def modeSelector(self):
        if self.permanent:
            self.finishCreation()
            
        else:
            self.oneTimeEdit()
            
        self.close()
    
    def vhdManager(self):
        if platform.system() == "Windows":
            connection = platformSpecific.windowsSpecific.setupWindowsBackend()
        
        else:
            connection = platformSpecific.unixSpecific.setupUnixBackend()

        cursor = connection.cursor()
        
        if self.le_vhdp.text() == "" or self.le_vhdp.isEnabled() == False:
            vhd = "NULL"
        
        else:
            vhd = self.le_vhdp.text()

            if platform.system() == "Windows":
                tempVmDef = platformSpecific.windowsSpecific.windowsTempVmStarterFile()
        
            else:
                tempVmDef = platformSpecific.unixSpecific.unixTempVmStarterFile()

            with open(tempVmDef, "r+") as tempVmDefFile:
                vmSpecsRaw = tempVmDefFile.readlines()

            vhdAction = vmSpecsRaw[0]

            if self.cb_vhdf.isEnabled():
                vhdAction = "overwrite"

            else:
                vhdAction = "keep"

            get_qemu_img_bin = """
            SELECT value FROM settings
            WHERE name = "qemu-img"
            """

            vhd_cmd = ""

            try:
                cursor.execute(get_qemu_img_bin)
                connection.commit()
                result = cursor.fetchall()
                qemu_binary = result[0][0]
                vhd_size_in_b = None

                if self.cb_maxsize.currentText().startswith("K"):
                    vhd_size_in_b = self.sb_maxsize.value() * 1024

                elif self.cb_maxsize.currentText().startswith("M"):
                    vhd_size_in_b = self.sb_maxsize.value() * 1024 * 1024

                elif self.cb_maxsize.currentText().startswith("G"):
                    vhd_size_in_b = self.sb_maxsize.value() * 1024 * 1024 * 1024

                print(vhd_size_in_b)

                vhd_cmd = f"{qemu_binary} create -f {self.cb_vhdf.currentText()} \"{vhd}\" {str(vhd_size_in_b)}"

                if vhdAction.startswith("overwrite"):
                    subprocess.Popen(vhd_cmd)

                print("The query was executed and the virtual disk created successfully.")
        
            except sqlite3.Error as e:
                print(f"The SQLite module encountered an error: {e}.")

            except:
                print(f"The query was executed successfully, but the virtual disk couldn't be created. Trying to use subprocess.run")

                try:
                    #vhd_cmd_split = vhd_cmd.split(" ")
                    vhd_cmd_split = [qemu_binary, "create", "-f", self.cb_vhdf.currentText(), vhd, str(vhd_size_in_b)]

                    if vhdAction.startswith("overwrite"):
                        subprocess.run(vhd_cmd_split)

                    print("The query was executed and the virtual disk created successfully.")
                
                except:
                    print("The virtual disk could not be created. Please check if the path and the QEMU settings are correct.")
                    
        return vhd
    
    def oneTimeEdit(self):
        with open(f"{self.exec_folder}translations/createnewvhd.txt", "r+", encoding="utf8") as creNewVhdFile:
            creNewVhdContent = creNewVhdFile.read()

        with open(f"{self.exec_folder}translations/addexistingvhd.txt", "r+", encoding="utf8") as addExistVhdFile:
            addExistVhdContent = addExistVhdFile.read()

        with open(f"{self.exec_folder}translations/addnovhd.txt", "r+", encoding="utf8") as noVhdFile:
            noVhdContent = noVhdFile.read()

        with open(f"{self.exec_folder}translations/letqemudecide.txt", "r+", encoding="utf8") as letQemuDecideFile:
            letQemuDecideContent = letQemuDecideFile.read()
                
        self.vmdata.vm_name = self.le_name.text()
        self.vmdata.arch = self.cb_arch.currentText()
        
        if letQemuDecideContent.__contains__(self.cb_machine.currentText()):
            self.vmdata.machine = "Let QEMU decide"
            
        else:
            self.vmdata.machine = self.cb_machine.currentText()
        
        if letQemuDecideContent.__contains__(self.cb_cpu.currentText()):
            self.vmdata.cpu = "Let QEMU decide"
        
        else:
            self.vmdata.cpu = self.cb_cpu.currentText()
            
        self.vmdata.cores = self.sb_cpuc.value()
        self.vmdata.ram = self.sb_ram.value()
        
        if letQemuDecideContent.__contains__(self.cb_vga.currentText()):
            self.vmdata.vga = "Let QEMU decide"
            
        else:
            self.vmdata.vga = self.cb_vga.currentText()
        
        self.vmdata.net = self.cb_net.currentText()
        self.vmdata.biosdir = self.le_biosloc.text()
        self.vmdata.biosfile = self.le_biosf.text()
        self.vmdata.sound = self.cb_sound.currentText()
        self.vmdata.kernel = self.le_kernel.text()
        self.vmdata.initrd = self.le_initrd.text()
        self.vmdata.linuxcmd = self.le_cmd.text()
        self.vmdata.mouse = self.cb_mouse.currentText()
        self.vmdata.kbd = self.cb_kbdtype.currentText()
        self.vmdata.kbdlayout = self.cb_kbdlayout.currentText()
        
        if self.chb_usb.isChecked():
            self.vmdata.usb_support = "1"
            
        else:
            self.vmdata.usb_support = "0"
        
        self.vmdata.usb_controller = self.cb_usb.currentText()
        self.vmdata.hwaccel = self.cb_accel.currentText()
        
        if letQemuDecideContent.__contains__(self.cb_cdc1.currentText()):
            self.vmdata.cd_control1 = "Let QEMU decide"
        
        else:
            self.vmdata.cd_control1 = self.cb_cdc1.currentText()
            
        if letQemuDecideContent.__contains__(self.cb_cdc2.currentText()):
            self.vmdata.cd_control2 = "Let QEMU decide"
        
        else:
            self.vmdata.cd_control2 = self.cb_cdc2.currentText()
            
        if letQemuDecideContent.__contains__(self.cb_hddc.currentText()):
            self.vmdata.hda_control = "Let QEMU decide"
        
        else:
            self.vmdata.hda_control = self.cb_hddc.currentText()
        
        self.vmdata.cd1 = self.le_cd1.text()
        self.vmdata.cd2 = self.le_cd2.text()
        
        if letQemuDecideContent.__contains__(self.cb_bootfrom.currentText()):
            self.vmdata.bootfrom = "Let QEMU decide"
        
        else:
            self.vmdata.bootfrom = self.cb_bootfrom.currentText()
        
        self.vmdata.floppy = self.le_floppy.text()
        
        if self.dtb_rtc.isEnabled():
            self.vmdata.timemgr = self.dtb_rtc.text()
            
        else:
            self.vmdata.timemgr = "system"
            
        self.vmdata.hda = self.vhdManager()
        self.vmdata.addargs = self.le_addargs.text()

    def finishCreation(self):
        with open(f"{self.exec_folder}translations/letqemudecide.txt", "r+", encoding="utf8") as letQemuDecideVariants:
            letQemuDecideVariantsStr = letQemuDecideVariants.read()

        with open(f"{self.exec_folder}translations/systemdefault.txt", "r+", encoding="utf8") as sysDefFile:
            sysDefContent = sysDefFile.read()

        # This applies the changes to your VM.
        
        if platform.system() == "Windows":
            connection = platformSpecific.windowsSpecific.setupWindowsBackend()
        
        else:
            connection = platformSpecific.unixSpecific.setupUnixBackend()

        cursor = connection.cursor()

        machine = self.cb_machine.currentText()
        cpu = self.cb_cpu.currentText()

        if cpu.startswith("Icelake-Client"):
            cpu = "Icelake-Client"

        ram = self.sb_ram.value()

        if letQemuDecideVariantsStr.__contains__(machine):
            machine = "Let QEMU decide"

        if letQemuDecideVariantsStr.__contains__(cpu):
            cpu = "Let QEMU decide"
            
        vhd = self.vhdManager()

        """ if self.le_vhdp.text() == "" or self.le_vhdp.isEnabled() == False:
            vhd = "NULL"
        
        else:
            vhd = self.le_vhdp.text()

            if platform.system() == "Windows":
                tempVmDef = platformSpecific.windowsSpecific.windowsTempVmStarterFile()
        
            else:
                tempVmDef = platformSpecific.unixSpecific.unixTempVmStarterFile()

            with open(tempVmDef, "r+") as tempVmDefFile:
                vmSpecsRaw = tempVmDefFile.readlines()

            vhdAction = vmSpecsRaw[0]

            if self.cb_vhdf.isEnabled():
                vhdAction = "overwrite"

            else:
                vhdAction = "keep"

            get_qemu_img_bin = ""
            SELECT value FROM settings
            WHERE name = "qemu-img"
            ""

            vhd_cmd = ""

            try:
                cursor.execute(get_qemu_img_bin)
                connection.commit()
                result = cursor.fetchall()
                qemu_binary = result[0][0]
                vhd_size_in_b = None

                if self.cb_maxsize.currentText().startswith("K"):
                    vhd_size_in_b = self.sb_maxsize.value() * 1024

                elif self.cb_maxsize.currentText().startswith("M"):
                    vhd_size_in_b = self.sb_maxsize.value() * 1024 * 1024

                elif self.cb_maxsize.currentText().startswith("G"):
                    vhd_size_in_b = self.sb_maxsize.value() * 1024 * 1024 * 1024

                print(vhd_size_in_b)

                vhd_cmd = f"{qemu_binary} create -f {self.cb_vhdf.currentText()} \"{vhd}\" {str(vhd_size_in_b)}"

                if vhdAction.startswith("overwrite"):
                    subprocess.Popen(vhd_cmd)

                print("The query was executed and the virtual disk created successfully.")
        
            except sqlite3.Error as e:
                print(f"The SQLite module encountered an error: {e}.")

            except:
                print(f"The query was executed successfully, but the virtual disk couldn't be created. Trying to use subprocess.run")

                try:
                    #vhd_cmd_split = vhd_cmd.split(" ")
                    vhd_cmd_split = [qemu_binary, "create", "-f", self.cb_vhdf.currentText(), vhd, str(vhd_size_in_b)]

                    if vhdAction.startswith("overwrite"):
                        subprocess.run(vhd_cmd_split)

                    print("The query was executed and the virtual disk created successfully.")
                
                except:
                    print("The virtual disk could not be created. Please check if the path and the QEMU settings are correct.") """

        if letQemuDecideVariantsStr.__contains__(self.cb_vga.currentText()):
            vga = "Let QEMU decide"
        
        else:
            vga = self.cb_vga.currentText()

        print(vga)

        if self.cb_net.currentText() == "none":
            networkAdapter = "none"
        
        else:
            networkAdapter = self.cb_net.currentText()

        """ if self.checkBox_2.isChecked():
            usbtablet = 1

        else:
            usbtablet = 0 """

        """ if self.checkBox_3.isChecked():
            win2k = 1

        else:
            win2k = 0 """
            
        win2k = 0 # The bug caused by this is intended for now.

        ext_bios_dir = self.le_biosloc.text()

        add_args = self.le_addargs.text()

        if self.chb_usb.isChecked() or self.cb_mouse.currentText() == "USB Mouse":
            usb_support = 1

        elif self.cb_mouse.currentText() == "USB Tablet Device" or self.cb_kbdtype.currentText() == "USB Keyboard":
            usb_support = 1

        else:
            usb_support = 0

        kbdlayout = self.cb_kbdlayout.currentText()

        if letQemuDecideVariantsStr.__contains__(self.cb_cdc1.currentText()):
            cd_control1 = "Let QEMU decide"
        
        else:
            cd_control1 = self.cb_cdc1.currentText()

        if letQemuDecideVariantsStr.__contains__(self.cb_cdc2.currentText()):
            cd_control2 = "Let QEMU decide"
        
        else:
            cd_control2 = self.cb_cdc2.currentText()

        if letQemuDecideVariantsStr.__contains__(self.cb_hddc.currentText()):
            hda_control = "Let QEMU decide"
        
        else:
            hda_control = self.cb_hddc.currentText()

        if self.cb_accel.currentText() == "HAXM (depreciated)":
            accelerator = "HAXM"

        else:
            accelerator = self.cb_accel.currentText()
            
        if self.dtb_rtc.isEnabled():
            timemgr = self.dtb_rtc.text()
            
        else:
            timemgr = "system"
            
        if letQemuDecideVariantsStr.__contains__(self.cb_bootfrom.currentText()):
            bootfrom = "Let QEMU decide"
            
        else:
            bootfrom = self.cb_bootfrom.currentText()
        
        insert_into_vm_database = f"""
        UPDATE virtualmachines
        SET name = "{self.le_name.text()}", architecture = "{self.cb_arch.currentText()}", machine = "{machine}", cpu = "{cpu}",
        ram = {ram}, hda = "{vhd}", vga = "{vga}", net = "{networkAdapter}",
        win2k = {win2k}, dirbios = "{ext_bios_dir}", additionalargs = "{add_args}", sound = "{self.cb_sound.currentText()}",
        linuxkernel = "{self.le_kernel.text()}", linuxinitrid = "{self.le_initrd.text()}", linuxcmd = "{self.le_cmd.text()}",
        mousetype = "{self.cb_mouse.currentText()}", cores = {self.sb_cpuc.value()}, filebios = "{self.le_biosf.text()}",
        keyboardtype = "{self.cb_kbdtype.currentText()}", usbsupport = {usb_support}, usbcontroller = "{self.cb_usb.currentText()}",
        kbdtype = "{kbdlayout}", acceltype = "{accelerator}", storagecontrollercd1 = "{cd_control1}",
        storagecontrollercd2 = "{cd_control2}", hdacontrol = "{hda_control}", cd1 = "{self.le_cd1.text()}", cd2 = "{self.le_cd2.text()}",
        floppy = "{self.le_floppy.text()}", timemgr = "{timemgr}", bootfrom = "{bootfrom}"
        WHERE name = "{self.vmdata.vm_name}";
        """

        cursor = connection.cursor()

        try:
            cursor.execute(insert_into_vm_database)
            connection.commit()
            print("The query was executed successfully.")
        
        except sqlite3.Error as e:
            print(f"The SQLite module encountered an error: {e}.")

            if platform.system() == "Windows":
                errorFile = platformSpecific.windowsSpecific.windowsErrorFile()
        
            else:
                errorFile = platformSpecific.unixSpecific.unixErrorFile()

            with open(errorFile, "w+") as errCodeFile:
                errCodeFile.write(errors.errCodes.errCodes[53])

            self.logman.writeToLogFile(
                f"{errors.errCodes.errCodes[53]}: The VM couldn't be edited due to a database issue."
            )

            dialog = ErrDialog(self)
            dialog.exec()