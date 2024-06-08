import os
import pwd
import sqlite3
homedir = os.getenv("HOME")
def setupUnixBackend():
    try:
        userName = os.getlogin()
    
    except:
        userName = pwd.getpwuid(os.getuid())[0]
    
    connection = None

    try:
        connection = sqlite3.connect(f"{homedir}/EmuGUI/virtual_machines.sqlite")
        print("Connection established.")
    
    except sqlite3.Error as e:
        print(f"The SQLite module encountered an error: {e}. Trying to create the file.")

        try:
            unixCreEmuGUIFolder()
            file = open(f"{homedir}/EmuGUI/virtual_machines.sqlite", "w+")
            file.close()
        
        except:
            print("EmuGUI wasn't able to create the file.")

        try:
            connection = sqlite3.connect(f"{homedir}/EmuGUI/virtual_machines.sqlite")

        except sqlite3.Error as e:
            print(f"The SQLite module encountered an error: {e}.")
    
    return connection

def unixTempVmStarterFile():
    fileName = f"{homedir}/EmuGUI/vmstart.txt"
    return fileName

def unixLanguageFile():
    fileName = f"{homedir}/EmuGUI/lang.txt"    
    return fileName

def unixUpdateFile():
    fileName = f"{homedir}/EmuGUI/update.txt"
    return fileName

def unixExportFile():
    fileName = f"{homedir}/EmuGUI/vmdef.txt"    
    return fileName
def unixErrorFile():
    fileName = f"{homedir}/EmuGUI/error.txt"    
    return fileName
def unixLogFile(logID):
    fileName = f"{homedir}/EmuGUI/log-{logID}.txt"    
    return fileName
def unixCreEmuGUIFolder():
    os.mkdir(f"{homedir}/EmuGUI")
