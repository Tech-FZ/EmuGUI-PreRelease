import os
import sqlite3
from pathlib import Path
from win32com.shell import shell, shellcon

def setupWindowsBackend():
    connection = None

    try:
        connection = sqlite3.connect(f"{shell.SHGetFolderPath(0,shellcon.CSIDL_PERSONAL, None, 0)}\\EmuGUI\\virtual_machines.sqlite")
        print("Connection established.")

    except sqlite3.Error as e:
        print(f"The SQLite module encountered an error: {e}. Trying to create the file.")

        try:
            windowsCreEmuGUIFolder()
            file = open(f"{shell.SHGetFolderPath(0,shellcon.CSIDL_PERSONAL, None, 0)}\\EmuGUI\\virtual_machines.sqlite", "w+")
            file.close()

        except:
            print("EmuGUI wasn't able to create the file.")

        try:
            connection = sqlite3.connect(f"{shell.SHGetFolderPath(0,shellcon.CSIDL_PERSONAL, None, 0)}\\EmuGUI\\virtual_machines.sqlite")
            print("Connection established.")

        except sqlite3.Error as e:
            print(f"The SQLite module encountered an error: {e}.")

    return connection

def windowsTempVmStarterFile():
    fileName = f"{shell.SHGetFolderPath(0,shellcon.CSIDL_PERSONAL, None, 0)}\\EmuGUI\\vmstart.txt"
    return fileName

def windowsLanguageFile():
    fileName = f"{shell.SHGetFolderPath(0,shellcon.CSIDL_PERSONAL, None, 0)}\\EmuGUI\\lang.txt"
    return fileName

def windowsUpdateFile():
    fileName = f"{shell.SHGetFolderPath(0,shellcon.CSIDL_PERSONAL, None, 0)}\\EmuGUI\\update.txt"
    return fileName

def windowsExportFile():
    fileName = f"{shell.SHGetFolderPath(0,shellcon.CSIDL_PERSONAL, None, 0)}\\EmuGUI\\vmdef.txt"
    return fileName

def windowsErrorFile():
    fileName = f"{shell.SHGetFolderPath(0,shellcon.CSIDL_PERSONAL, None, 0)}\\EmuGUI\\error.txt"

    return fileName

def windowsLogFile(logID):
    fileName = f"{shell.SHGetFolderPath(0,shellcon.CSIDL_PERSONAL, None, 0)}\\EmuGUI\\log-{logID}.txt"

    return fileName

def windowsCreEmuGUIFolder():
    Path(f"{shell.SHGetFolderPath(0,shellcon.CSIDL_PERSONAL, None, 0)}\\EmuGUI").mkdir(parents=True, exist_ok=True)
