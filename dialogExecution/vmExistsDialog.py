from uiScripts.ui_VmExists import Ui_Dialog
from PySide6.QtWidgets import *
from PySide6 import QtGui
import sqlite3
import platform

if platform.system() == "Windows":
    import platformSpecific.windowsSpecific

else:
    import platformSpecific.unixSpecific
    
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
import locale

class VmAlreadyExistsDialog(QDialog, Ui_Dialog):
    def __init__(self, parent = None):
        try:
            super().__init__(parent)

        except:
            super().__init__()
            
        self.setupUi(self)
        self.setWindowTitle("EmuGUI - VM already exists")
        self.langDetect()
        
        try:
            self.setWindowIcon(QtGui.QIcon("EmuGUI.png"))

        except:
            pass
        
        self.connectSignalsSlots()

    def connectSignalsSlots(self):
        self.pushButton.clicked.connect(self.close)

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

                elif result[0][1] == "it":
                    langmode = "it"

                elif result[0][1] == "system":
                    langmode = "system"

                self.setLanguage(langmode)
                print("The query was executed successfully. The language slot already is in the database.")

            except:
                langmode = "system"
                self.setLanguage(langmode)
                print("The query was executed successfully. The language slot has been created.")
        
        except sqlite3.Error as e:
            print(f"The SQLite module encountered an error: {e}.")

    def setLanguage(self, langmode):
        if langmode == "system" or langmode == None:
            languageToUse = locale.getlocale()[0]

        else:
            languageToUse = langmode

        if languageToUse != None:
            if languageToUse.startswith("de"):
                translations.de.translateVmExistsDE(self)

            elif languageToUse.startswith("uk"):
                translations.uk.translateVmExistsUK(self)

            elif languageToUse.startswith("fr"):
                translations.fr.translateVmExistsFR(self)

            elif languageToUse.startswith("es"):
                translations.es.translateVmExistsES(self)

            elif languageToUse.startswith("ro"):
                translations.ro.translateVmExistsRO(self)

            elif languageToUse.startswith("ru"):
                translations.ru.translateVmExistsRU(self)

            elif languageToUse.startswith("be"):
                translations.be.translateVmExistsBE(self)

            elif languageToUse.startswith("cz"):
                translations.cz.translateVmExistsCZ(self)

            elif languageToUse.startswith("pt"):
                translations.pt.translateVmExistsPT(self)

            elif languageToUse.startswith("it"):
                translations.it.translateVmExistsIT(self)

            else:
                translations.en.translateVmExistsEN(self)
        
        else:
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
                        translations.de.translateVmExistsDE(self)

                    elif languageToUse.startswith("uk"):
                        translations.uk.translateVmExistsUK(self)

                    elif languageToUse.startswith("fr"):
                        translations.fr.translateVmExistsFR(self)

                    elif languageToUse.startswith("es"):
                        translations.es.translateVmExistsES(self)

                    elif languageToUse.startswith("ro"):
                        translations.ro.translateVmExistsRO(self)

                    elif languageToUse.startswith("ru"):
                        translations.ru.translateVmExistsRU(self)

                    elif languageToUse.startswith("be"):
                        translations.be.translateVmExistsBE(self)

                    elif languageToUse.startswith("cz"):
                        translations.cz.translateVmExistsCZ(self)

                    elif languageToUse.startswith("pt"):
                        translations.pt.translateVmExistsPT(self)

                    elif languageToUse.startswith("it"):
                        translations.it.translateVmExistsIT(self)

                    else:
                        translations.en.translateVmExistsEN(self)
            
            except:
                print("Translation can't be figured out. Using English language.")
                translations.en.translateVmExistsEN(self)