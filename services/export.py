import platform
from dialogExecution.errDialog import ErrDialog
from emugui import Window
import errors.logman
from services.vm_data import *
import zipfile
import os
import platformSpecific
import errors

def exportVirtualMachine(vmdata, zipFileName, dataDefFile, logman, mainWin):
    if (isinstance(vmdata, VirtualMachineData) and isinstance(zipFileName, str) and isinstance(dataDefFile, str) and isinstance(logman, errors.logman.LogMan)):
        if (isinstance(mainWin, Window)):
            with zipfile.ZipFile(zipFileName, "w") as vmFile:
                vmFile.write(dataDefFile, os.path.basename(dataDefFile))

                if vmdata.hda != "NULL":
                    vmFile.write(vmdata.hda, os.path.basename(vmdata.hda))

            if os.path.exists(zipFileName):
                print("Export successful!")

            else:
                print("Export failed!")

                if platform.system() == "Windows":
                    errorFile = platformSpecific.windowsSpecific.windowsErrorFile()
        
                else:
                    errorFile = platformSpecific.unixSpecific.unixErrorFile()

                with open(errorFile, "w+") as errCodeFile:
                    errCodeFile.write(errors.errCodes.errCodes[33])

                logman.writeToLogFile(
                    f"{errors.errCodes.errCodes[33]}: This VM could not be exported. Please check its settings."
                    )

                dialog = ErrDialog(mainWin)
                dialog.exec()
    