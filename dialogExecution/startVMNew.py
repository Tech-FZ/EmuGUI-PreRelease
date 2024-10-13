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
    
    def startVirtualMachine(self):
        connection = self.connection
        cursor = connection.cursor()

        fda_file = self.vmdata.floppy
        cdrom_file = self.vmdata.cd1
        cdrom_file2 = self.vmdata.cd2
        bootfrom = self.vmdata.bootfrom
        dateTimeForVM = self.vmdata.timemgr

        print(fda_file)
        print(cdrom_file)
        print(bootfrom)
        print(dateTimeForVM)

        qemu_cmd = ""

        try:
            for architecture in self.architectures:
                if self.vmdata.arch == architecture:
                    sel_query = f"""
                    SELECT value FROM settings
                    WHERE name = 'qemu-system-{architecture}';
                    """

                    cursor.execute(sel_query)
                    connection.commit()
                    result = cursor.fetchall()
                    print(result)
                    break

            qemu_to_execute = result[0][0]

            qemu_cmd = f"\"{qemu_to_execute}\" -m {self.vmdata.ram} -smp {self.vmdata.cores} -k {self.vmdata.kbdlayout}"
            qemu_cmd_list = [qemu_to_execute, "-m", self.vmdata.ram, "-smp", self.vmdata.cores, "-k", self.vmdata.kbdlayout]

            if dateTimeForVM != "system":
                qemu_cmd = qemu_cmd + f" -rtc base=\"{dateTimeForVM}\",clock=vm"
                qemu_cmd_list.append("-rtc")
                qemu_cmd_list.append(f"base=\"{dateTimeForVM}\",clock=vm")

            if self.vmdata.hda != "NULL":
                if magic.from_file(self.vmSpecs[5]) == "block special":
                    qemu_cmd = qemu_cmd + f" -drive format=raw,file=\"{self.vmdata.hda}\""
                    qemu_cmd_list.append("-drive")
                    qemu_cmd_list.append(f"format=raw,file=\"{self.vmdata.hda}\"")

                else:
                    if self.vmdata.hda_control == "Let QEMU decide":
                        qemu_cmd = qemu_cmd + f" -hda \"{self.vmdata.hda}\""
                        qemu_cmd_list.append("-hda")
                        qemu_cmd_list.append(self.vmdata.hda)

                    else:
                        qemu_cmd = qemu_cmd + " -drive"
                        qemu_cmd_list.append("-drive")

                        if self.vmSpecs[26] == "IDE":
                            qemu_cmd = qemu_cmd + f" file=\"{self.vmdata.hda}\",if=ide,media=disk"
                            qemu_cmd_list.append(f"file=\"{self.vmdata.hda}\",if=ide,media=disk")

                        elif self.vmSpecs[26] == "VirtIO SCSI":
                            qemu_cmd = qemu_cmd + f" file=\"{self.vmdata.hda}\",if=none,discard=unmap,aio=native,cache=none,id=hd1 -device scsi-hd,drive=hd1,bus=scsi0.0"
                            qemu_cmd_list.append(f"file=\"{self.vmdata.hda}\",if=none,discard=unmap,aio=native,cache=none,id=hd1 -device scsi-hd,drive=hd1,bus=scsi0.0")

                        elif self.vmSpecs[26] == "AHCI":
                            qemu_cmd = qemu_cmd + f" file=\"{self.vmdata.hda}\",if=none -device ahci,id=ahci -device ide-hd,drive=disk,bus=ahci.0"
                            qemu_cmd_list.append(f"file=\"{self.vmdata.hda}\",if=none -device ahci,id=ahci -device ide-hd,drive=disk,bus=ahci.0")

            if self.vmdata.machine != "Let QEMU decide":
                qemu_cmd = qemu_cmd + f" -M {self.vmdata.machine}"

            if self.vmSpecs[3] != "Let QEMU decide":
                qemu_cmd = qemu_cmd + f" -cpu {self.vmSpecs[3]}"

            if self.vmSpecs[6] != "Let QEMU decide":
                if self.vmSpecs[6] == "std" or self.vmSpecs[6] == "qxl" or self.vmSpecs[6] == "cirrus" or self.vmSpecs[6] == "cg3" or self.vmSpecs[6] == "tcx":
                    qemu_cmd = qemu_cmd + f" -vga {self.vmSpecs[6]}"

                else:
                    qemu_cmd = qemu_cmd + f" -device {self.vmSpecs[6]}"

            if self.vmSpecs[7] != "none":
                if self.vmSpecs[1] == "i386" or self.vmSpecs[1] == "x86_64" or self.vmSpecs[1] == "ppc" or self.vmSpecs[1] == "ppc64" or self.vmSpecs[1] == "sparc" or self.vmSpecs[1] == "sparc64":
                    qemu_cmd = qemu_cmd + f" -net nic,model={self.vmSpecs[7]} -net user"

                if self.vmSpecs[1] == "riscv32" or self.vmSpecs[1] == "riscv64" or self.vmSpecs[1] == "alpha":
                    qemu_cmd = qemu_cmd + f" -net nic,model={self.vmSpecs[7]} -net user"

                elif self.vmSpecs[1] == "mips64el" or self.vmSpecs[1] == "mipsel":
                    qemu_cmd = qemu_cmd + f" -nic user,model={self.vmSpecs[7]}"

                elif self.vmSpecs[1] == "aarch64" or self.vmSpecs[1] == "arm":
                    # Due to the circumstances here, for the VM, a random MAC address is
                    # generated at runtime. Due to that, the MAC changes every time you
                    # start your virtual machine.

                    mac_possible_chars = "0123456789abcdef"

                    mac_gen = []
                    i = 0

                    while i < 6:
                        firstLetter = mac_possible_chars[randint(0, 15)]
                        secondLetter = mac_possible_chars[randint(0, 15)]
                        mac_part = firstLetter + secondLetter
                        mac_gen.append(mac_part)
                        i += 1

                    mac_to_use = f"{mac_gen[0]}:{mac_gen[1]}:{mac_gen[2]}:{mac_gen[3]}:{mac_gen[4]}:{mac_gen[5]}"
                    qemu_cmd = qemu_cmd + f" -device {self.vmSpecs[7]},netdev=hostnet0,mac={mac_to_use} -netdev user,id=hostnet0"

            if self.vmSpecs[20] == "1":
                qemu_cmd = qemu_cmd + f" -usb -device {self.vmSpecs[21]}"
            
            """ if self.vmSpecs[7] == "1":
                print("WARNING: Using the checkbox for the USB tablet is depreciated.")
                print("This feature is going to be removed in a future update.")
                print("Please use the combo box for this task instead.")
                qemu_cmd = qemu_cmd + " -usbdevice tablet" """

            if self.vmSpecs[8] == "1" and self.vmSpecs[0] == "i386":
                qemu_cmd = qemu_cmd + " -win2k-hack"

            if fda_file != "":
                qemu_cmd = qemu_cmd + f" -drive format=raw,file=\"{fda_file}\",index=0,if=floppy"
                qemu_cmd_list.append("-drive")
                qemu_cmd_list.append(f"format=raw,file=\"{fda_file}\",index=0,if=floppy")

            if cdrom_file != "":
                if self.vmSpecs[24] == "Let QEMU decide":
                    qemu_cmd = qemu_cmd + f" -cdrom \"{cdrom_file}\""
                    qemu_cmd_list.append(f"-cdrom \"{cdrom_file}\"")

                else:
                    if self.vmSpecs[24] == "IDE":
                        qemu_cmd = qemu_cmd + f" -drive file=\"{cdrom_file}\",if=ide,media=cdrom"
                        qemu_cmd_list.append(f"-drive file=\"{cdrom_file}\",if=ide,media=cdrom")

                    elif self.vmSpecs[24] == "SCSI":
                        qemu_cmd = qemu_cmd + f" -drive file=\"{cdrom_file}\",if=scsi,media=cdrom"
                        qemu_cmd_list.append(f"-drive file=\"{cdrom_file}\",if=scsi,media=cdrom")

                    elif self.vmSpecs[24] == "Virtio":
                        qemu_cmd = qemu_cmd + f" -drive file=\"{cdrom_file}\",if=virtio,media=cdrom"
                        qemu_cmd_list.append(f"-drive file=\"{cdrom_file}\",if=virtio,media=cdrom")

            if cdrom_file2 != "":
                if self.vmSpecs[25] == "Let QEMU decide":
                    qemu_cmd = qemu_cmd + f" -cdrom \"{cdrom_file2}\""
                    qemu_cmd_list.append(f"-cdrom \"{cdrom_file2}\"")

                else:
                    if self.vmSpecs[25] == "IDE":
                        qemu_cmd = qemu_cmd + f" -drive file={cdrom_file2},if=ide,media=cdrom"
                        qemu_cmd_list.append(f"-drive file=\"{cdrom_file2}\",if=ide,media=cdrom")

                    elif self.vmSpecs[25] == "SCSI":
                        qemu_cmd = qemu_cmd + f" -drive file={cdrom_file2},if=scsi,media=cdrom"
                        qemu_cmd_list.append(f"-drive file=\"{cdrom_file2}\",if=scsi,media=cdrom")

                    elif self.vmSpecs[25] == "Virtio":
                        qemu_cmd = qemu_cmd + f" -drive file={cdrom_file2},if=virtio,media=cdrom"
                        qemu_cmd_list.append(f"-drive file=\"{cdrom_file2}\",if=virtio,media=cdrom")

            if bootfrom == "c" or bootfrom == "a" and fda_file == "" or bootfrom == "d" and cdrom_file == "":
                qemu_cmd = qemu_cmd + " -boot c"
                qemu_cmd_list.append("-boot c")

            elif bootfrom == "a" and fda_file != "":
                qemu_cmd = qemu_cmd + " -boot a"
                qemu_cmd_list.append("-boot a")
            
            elif bootfrom == "d" and cdrom_file != "":
                qemu_cmd = qemu_cmd + " -boot d"
                qemu_cmd_list.append("-boot d")

            if self.vmSpecs[10] != "":
                qemu_cmd = qemu_cmd + f" -L {self.vmSpecs[10]}"
                qemu_cmd_list.append(f"-L {self.vmSpecs[10]}")

            if self.vmSpecs[12] != "none":
                qemu_cmd = qemu_cmd + f" -device {self.vmSpecs[12]}"
                qemu_cmd_list.append(f"-device {self.vmSpecs[12]}")

                if self.vmSpecs[12] == "intel-hda":
                    qemu_cmd = qemu_cmd + " -device hda-duplex"
                    qemu_cmd_list.append(f"-device hda-duplex")

            if self.vmSpecs[13] != "":
                qemu_cmd = qemu_cmd + f" -kernel \"{self.vmSpecs[13]}\""
                qemu_cmd_list.append(f"-kernel \"{self.vmSpecs[13]}\"")

            if self.vmSpecs[14] != "":
                qemu_cmd = qemu_cmd + f" -initrd \"{self.vmSpecs[14]}\""
                qemu_cmd_list.append(f"-initrd \"{self.vmSpecs[14]}\"")

            if self.vmSpecs[15] != "":
                qemu_cmd = qemu_cmd + f" -append \"{self.vmSpecs[15]}\""
                qemu_cmd_list.append(f"-append \"{self.vmSpecs[15]}\"")

            if self.vmSpecs[16] == "USB Mouse" and self.vmSpecs[7] == "0":
                if self.vmSpecs[1] == "aarch64" or self.vmSpecs[1] == "arm":
                    qemu_cmd = qemu_cmd + " -device usb-mouse"
                    qemu_cmd_list.append("-device usb-mouse")

                else:
                    qemu_cmd = qemu_cmd + " -usbdevice mouse"
                    qemu_cmd_list.append("-usbdevice mouse")

            if self.vmSpecs[16] == "USB Tablet Device" and self.vmSpecs[7] == "0":
                if self.vmSpecs[1] == "aarch64" or self.vmSpecs[1] == "arm":
                    qemu_cmd = qemu_cmd + " -device usb-tablet"
                    qemu_cmd_list.append("-device usb-tablet")

                else:
                    qemu_cmd = qemu_cmd + " -usbdevice tablet"
                    qemu_cmd_list.append("-usbdevice tablet")

            if self.vmSpecs[18] != "" and self.vmSpecs[18] != None and self.vmSpecs[18] != "None":
                qemu_cmd = qemu_cmd + f" -bios \"{self.vmSpecs[18]}\""
                qemu_cmd_list.append(f"-bios \"{self.vmSpecs[18]}\"")

            if self.vmSpecs[19] == "USB Keyboard":
                qemu_cmd = qemu_cmd + " -device usb-kbd"
                qemu_cmd_list.append("-device usb-kbd")

            if self.vmSpecs[11] != "":
                qemu_cmd = qemu_cmd + f" {self.vmSpecs[11]}"
                qemu_cmd_list.append(self.vmSpecs[11])

            if self.vmSpecs[23] == "TCG":
                qemu_cmd = qemu_cmd + " -accel tcg"
                qemu_cmd_list.append("-accel tcg")

            elif self.vmSpecs[23] == "HAXM":
                qemu_cmd = qemu_cmd + " -accel hax"
                qemu_cmd_list.append("-accel hax")

            elif self.vmSpecs[23] == "WHPX":
                qemu_cmd = qemu_cmd + " -accel whpx"
                qemu_cmd_list.append("-accel whpx")

            elif self.vmSpecs[23] == "WHPX (kernel-irqchip off)":
                qemu_cmd = qemu_cmd + " -accel whpx,kernel-irqchip=off"
                qemu_cmd_list.append("-accel whpx,kernel-irqchip=off")

            elif self.vmSpecs[23] == "KVM":
                qemu_cmd = qemu_cmd + " -enable-kvm"
                qemu_cmd_list.append("-enable-kvm")

            if self.lineEdit_3.text() != "":
                if self.vmSpecs[1] == "x86_64":
                    qemu_cmd = qemu_cmd + f" -chardev socket,id=chrtpm,path={self.lineEdit_3.text()}/swtpm-sock -tpmdev emulator,id=tpm0,chardev=chrtpm -device tpm-tis,tpmdev=tpm0"
                    qemu_cmd_list.append(f"-chardev socket,id=chrtpm,path={self.lineEdit_3.text()}/swtpm-sock -tpmdev emulator,id=tpm0,chardev=chrtpm -device tpm-tis,tpmdev=tpm0")

                elif self.vmSpecs[1] == "aarch64":
                    qemu_cmd = qemu_cmd + f" -chardev socket,id=chrtpm,path={self.lineEdit_3.text()}/swtpm-sock -tpmdev emulator,id=tpm0,chardev=chrtpm -device tpm-tis-device,tpmdev=tpm0"
                    qemu_cmd_list.append(f"-chardev socket,id=chrtpm,path={self.lineEdit_3.text()}/swtpm-sock -tpmdev emulator,id=tpm0,chardev=chrtpm -device tpm-tis-device,tpmdev=tpm0")

                elif self.vmSpecs[1] == "ppc64":
                    qemu_cmd = qemu_cmd + f" -chardev socket,id=chrtpm,path={self.lineEdit_3.text()}/swtpm-sock -tpmdev emulator,id=tpm0,chardev=chrtpm -device tpm-spapr,tpmdev=tpm0"
                    qemu_cmd_list.append(f"-chardev socket,id=chrtpm,path={self.lineEdit_3.text()}/swtpm-sock -tpmdev emulator,id=tpm0,chardev=chrtpm -device tpm-spapr,tpmdev=tpm0")

            subprocess.Popen(qemu_cmd)

        except sqlite3.Error as e:
            print(f"The SQLite module encountered an error: {e}.")
        
        except:
            print("Qemu couldn't be executed. Trying subprocess.run")

            try:
                subprocess.run(shlex.split(qemu_cmd))
            
            except:
                print("Qemu couldn't be executed. Trying subprocess.call.")

                try:
                    if platform.system() == "Windows":
                        subprocess.call(qemu_cmd)

                    else:
                        subprocess.call(shlex.split(qemu_cmd))

                except:
                    print("Qemu couldn't be executed. Please check if the settings of your VM and/or the QEMU paths are correct.")
        
        self.close()