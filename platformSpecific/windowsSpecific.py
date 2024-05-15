import os
import sqlite3
from pathlib import Path

def setupWindowsBackend():
    connection = None

    try:
        connection = sqlite3.connect(f"{os.environ['USERPROFILE']}\\Documents\\EmuGUI\\virtual_machines.sqlite")
        print("Connection established.")

    except sqlite3.Error as e:
        print(f"The SQLite module encountered an error: {e}. Trying to create the file.")

        try:
            windowsCreEmuGUIFolder()
            file = open(f"{os.environ['USERPROFILE']}\\Documents\\EmuGUI\\virtual_machines.sqlite", "w+")
            file.close()

        except:
            print("EmuGUI wasn't able to create the file.")

        try:
            connection = sqlite3.connect(f"{os.environ['USERPROFILE']}\\Documents\\EmuGUI\\virtual_machines.sqlite")
            print("Connection established.")

        except sqlite3.Error as e:
            print(f"The SQLite module encountered an error: {e}.")

    return connection

def windowsTempVmStarterFile():
    fileName = f"{os.environ['USERPROFILE']}\\Documents\\EmuGUI\\vmstart.txt"
    return fileName

def windowsLanguageFile():
    fileName = f"{os.environ['USERPROFILE']}\\Documents\\EmuGUI\\lang.txt"
    return fileName

def windowsUpdateFile():
    fileName = f"{os.environ['USERPROFILE']}\\Documents\\EmuGUI\\update.txt"
    return fileName

def windowsExportFile():
    fileName = f"{os.environ['USERPROFILE']}\\Documents\\EmuGUI\\vmdef.txt"
    return fileName

def windowsErrorFile():
    fileName = f"{os.environ['USERPROFILE']}\\Documents\\EmuGUI\\error.txt"

    return fileName

def windowsLogFile(logID):
    fileName = f"{os.environ['USERPROFILE']}\\Documents\\EmuGUI\\log-{logID}.txt"

    return fileName

def windowsCreEmuGUIFolder():
    Path(f"{os.environ['USERPROFILE']}\\Documents\\EmuGUI").mkdir(parents=True, exist_ok=True)
