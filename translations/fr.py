from translations.systemdefaultset import *

def translateMainFR(window):
    # Tab group 1
    window.tabWidget.setTabText(0, "Principal") # Main
    window.tabWidget.setTabText(1, "Paramètres") # Settings

    # Main tab
    window.pushButton_8.setText("New virtual machine") # New virtual machine
    window.pushButton_9.setText("Start virtual machine") # Start virtual machine
    window.pushButton_10.setText("Edit selected virtual machine") # Edit selected virtual machine
    window.pushButton_11.setText("Delete selected virtual machine") # Delete selected virtual machine
    window.pushButton_22.setText("Export selected virtual machine") # Export selected virtual machine
    window.pushButton_23.setText("Import virtual machine") # Import virtual machine

    # Settings tabs
    window.tabWidget_2.setTabText(0, "Général") # General
    window.tabWidget_2.setTabText(3, "About EmuGUI") # About EmuGUI

    # General tab
    window.label_15.setText("Langue") # Language
    window.pushButton_15.setText("Appliquer") # Apply

    # Combo box for languages
    i = 0

    while i < window.comboBox_4.count():
        sysDefSet("System default", window.comboBox_4, i) # System default

        i += 1

    # Combo box for themes
    i = 0

    while i < window.comboBox_5.count():
        sysDefSet("System default", window.comboBox_5, i) # System default

        i += 1

    # QEMU tab
    window.label.setText("qemu-img Path") # qemu-img Path
    window.label_2.setText("qemu-system-i386 Path") # qemu-system-i386 Path
    window.label_3.setText("qemu-system-x86_64 Path") # qemu-system-x86_64 Path
    window.label_4.setText("qemu-system-ppc Path") # qemu-system-ppc Path
    window.label_5.setText("qemu-system-mips64el Path") # qemu-system-mips64el Path
    window.label_9.setText("qemu-system-aarch64 Path") # qemu-system-aarch64 Path
    window.label_11.setText("qemu-system-arm Path") # qemu-system-arm Path
    window.label_16.setText("qemu-system-ppc64 Path") # qemu-system-ppc64 Path
    window.label_17.setText("qemu-system-mipsel Path") # qemu-system-mipsel Path
    window.label_18.setText("qemu-system-mips Path") # qemu-system-mips Path
    window.label_19.setText("qemu-system-mips64 Path") # qemu-system-mips64 Path
    window.label_12.setText("qemu-system-sparc Path") # qemu-system-sparc Path
    window.label_13.setText("qemu-system-sparc64 Path") # qemu-system-sparc64 Path
    window.lbl_alpha.setText("qemu-system-alpha Path") # qemu-system-alpha Path
    window.lbl_riscv32.setText("qemu-system-riscv32 Path") # qemu-system-riscv32 Path
    window.lbl_riscv64.setText("qemu-system-riscv64 Path") # qemu-system-riscv64 Path

    window.pushButton.setText("Naviguer") # Browse
    window.pushButton_2.setText("Naviguer") # Browse
    window.pushButton_3.setText("Naviguer") # Browse
    window.pushButton_4.setText("Naviguer") # Browse
    window.pushButton_5.setText("Naviguer") # Browse
    window.pushButton_7.setText("Naviguer") # Browse
    window.pushButton_12.setText("Naviguer") # Browse
    window.pushButton_16.setText("Naviguer") # Browse
    window.pushButton_17.setText("Naviguer") # Browse
    window.pushButton_18.setText("Naviguer") # Browse
    window.pushButton_19.setText("Naviguer") # Browse
    window.pushButton_13.setText("Naviguer") # Browse
    window.pushButton_14.setText("Naviguer") # Browse
    window.btn_alpha.setText("Naviguer") # Browse
    window.btn_riscv32.setText("Naviguer") # Browse
    window.btn_riscv64.setText("Naviguer") # Browse
    window.pushButton_6.setText("Appliquer") # Apply
    window.btn_apply_qemu2.setText("Appliquer") # Apply

    # About tab
    # label_7 = Built on Python and PyQt technology, licensed under GNU General Public License 3.0
    window.label_7.setText("Built on Python and PyQt technology, licensed under GNU General Public License 3.0")

    window.label_10.setText(
        """
        WARNING: This program comes with ABSOLUTELY NO WARRANTY under applicable law. Please see the GNU GPL license for details.
        """
        ) # WARNING: This program comes with ABSOLUTELY NO WARRANTY under applicable law. Please see the GNU GPL license for details.

    window.label_14.setText("Banner made by Tech-FZ.") # Banner made by (insert author of current banner here).

    window.label_21.setText("EmuGUI on social media (in English)") # EmuGUI on social media (in English)

def translateNewVmFR(window):
    window.setWindowTitle("EmuGUI - Create new VM")

    # First page
    window.lbl_vmname.setText("Nom") # Name
    window.lbl_arch.setText("Architecture") # Architecture
    window.cb_arch.setPlaceholderText("Please choose an architecture") # Please choose an architecture

    window.btn_next1.setText("Suivant >") # Next >
    window.btn_cancel1.setText("Annuler") # Cancel

    # Second page
    window.lbl_machine.setText("Machine") # Machine
    window.lbl_cpu.setText("Unité centrale") # CPU
    window.lbl_ram.setText("RAM in MB") # RAM in MB

    window.cb_machine.setPlaceholderText("Please select a machine") # Please select a machine
    window.cb_cpu.setPlaceholderText("Please select a processor") # Please select a processor

    window.pb_prev2.setText("< Antérieur") # < Previous
    window.pb_next2.setText("Suivant >") # Next >
    window.pb_cancel2.setText("Annuler") # Cancel

    # Combo boxes on second page
    i = 0

    while i < window.cb_machine.count():
        if window.cb_machine.itemText(i) == "Let QEMU decide" or window.cb_machine.itemText(i) == "QEMU überlassen":
            window.cb_machine.setItemText(i, "Let QEMU decide") # Let QEMU decide
            break

        i += 1

    i = 0

    while i < window.cb_cpu.count():
        if window.cb_cpu.itemText(i) == "Let QEMU decide" or window.cb_cpu.itemText(i) == "QEMU überlassen":
            window.cb_cpu.setItemText(i, "Let QEMU decide") # Let QEMU decide
            break

        i += 1

    # Third page
    window.lbl_vhdU.setText("VHD usage") # VHD usage

    # Combobox for VHD usage
    i = 0

    while i < window.cb_vhdU.count():
        if window.cb_vhdU.itemText(i) == "Create a new virtual hard drive":
            window.cb_vhdU.setItemText(i, "Create a new virtual hard drive") # Create a new virtual hard drive
            break

        i += 1

    i = 0

    while i < window.cb_vhdU.count():
        if window.cb_vhdU.itemText(i) == "Add an existing virtual hard drive":
            window.cb_vhdU.setItemText(i, "Add an existing virtual hard drive") # Add an existing virtual hard drive
            break

        i += 1

    i = 0

    while i < window.cb_vhdU.count():
        if window.cb_vhdU.itemText(i) == "Don't add a virtual hard drive":
            window.cb_vhdU.setItemText(i, "Don't add a virtual hard drive") # Don't add a virtual hard drive
            break

        i += 1

    window.lbl_vhdP.setText("VHD path") # VHD path
    window.lbl_vhdF.setText("VHD file format") # VHD file format
    window.lbl_maxsize.setText("Maximum size") # Maximum size
    window.lbl_hddC.setText("HDD controller") # HDD controller

    i = 0

    while i < window.cb_hddC.count():
        if window.cb_hddC.itemText(i) == "Let QEMU decide" or window.cb_hddC.itemText(i) == "QEMU überlassen":
            window.cb_hddC.setItemText(i, "Let QEMU decide") # Let QEMU decide
            break

        i += 1

    window.cb_vhdF.setPlaceholderText("(Please select a file format)") # (Please select a file format)

    window.btn_vhdP.setText("Naviguer") # Browse
    window.btn_prev3.setText("< Antérieur") # < Previous
    window.btn_next3.setText("Suivant >") # Next >
    window.btn_cancel3.setText("Annuler") # Cancel

    # Fourth page
    window.lbl_vga.setText("VGA") # VGA

    i = 0

    while i < window.cb_vga.count():
        if window.cb_vga.itemText(i) == "Let QEMU decide" or window.cb_vga.itemText(i) == "QEMU überlassen":
            window.cb_vga.setItemText(i, "Let QEMU decide") # Let QEMU decide
            break

        i += 1

    window.lbl_net.setText("Réseau") # Network
    window.lbl_mouse.setText("Souris") # Mouse

    window.cb_vga.setPlaceholderText("(Please select a graphics adapter)") # (Please select a graphics adapter)
    window.cb_net.setPlaceholderText("(Please select a network adapter)") # (Please select a network adapter)

    window.btn_prev4.setText("< Antérieur") # < Previous
    window.btn_next4.setText("Suivant >") # Next >
    window.btn_cancel4.setText("Annuler") # Cancel

    # Fifth page
    window.lbl_biosLoc.setText(
        "Location of external\nBIOS file (Leave\nempty to use the\ndefault BIOS)"
        ) # Location of external\nBIOS file (Leave\nempty to use the\ndefault BIOS)

    window.lbl_biosF.setText("External BIOS file") # External BIOS file
    window.chb_rtc.setText("Use RTC option") # Use RTC option
    window.lbl_floppy.setText("Floppy disk") # Floppy disk

    window.btn_biosF.setText("Naviguer") # Browse
    window.btn_floppy.setText("Naviguer") # Browse
    window.btn_prev5.setText("< Antérieur") # < Previous
    window.btn_next5.setText("Suivant >") # Next >
    window.btn_cancel5.setText("Annuler") # Cancel

    # Sixth page
    window.lbl_sound.setText("Carte son") # Sound card
    window.lbl_cores.setText("CPU cores")# CPU cores
    window.lbl_kbd.setText("Clavier") # Keyboard
    window.lbl_kbdlayout.setText("Keyboard layout") # Keyboard layout

    window.btn_prev6.setText("< Antérieur") # < Previous
    window.btn_next6.setText("Suivant >") # Next >
    window.btn_cancel6.setText("Annuler") # Cancel

    # Seventh page
    window.lbl_kernel.setText("Linux kernel") # Linux kernel
    window.lbl_initrd.setText("Linux initrd image") # Linux initrd image
    window.lbl_cmd.setText("Linux cmd args") # Linux cmd args

    window.btn_kernel.setText("Naviguer") # Browse
    window.btn_initrd.setText("Naviguer") # Browse
    window.btn_prev7.setText("< Antérieur") # < Previous
    window.btn_next7.setText("Suivant >") # Next >
    window.btn_cancel7.setText("Annuler") # Cancel

    # Eighth page
    window.lbl_accel.setText("Accélération") # Acceleration
    window.lbl_cdc1.setText("CD controller 1") # CD controller 1
    window.lbl_cdc2.setText("CD controller 2") # CD controller 2

    i = 0

    while i < window.cb_cdc1.count():
        if window.cb_cdc1.itemText(i) == "Let QEMU decide" or window.cb_cdc1.itemText(i) == "QEMU überlassen":
            window.cb_cdc1.setItemText(i, "Let QEMU decide") # Let QEMU decide
            break

        i += 1

    i = 0

    while i < window.cb_cdc2.count():
        if window.cb_cdc2.itemText(i) == "Let QEMU decide" or window.cb_cdc2.itemText(i) == "QEMU überlassen":
            window.cb_cdc2.setItemText(i, "Let QEMU decide") # Let QEMU decide
            break

        i += 1

    window.btn_prev8.setText("< Antérieur") # < Previous
    window.btn_next8.setText("Suivant >") # Next >
    window.btn_cancel8.setText("Annuler") # Cancel

    # Ninth page
    window.lbl_addargs.setText("Additional arguments (if needed)") # Additional arguments (if needed)

    window.checkBox_2.setText("I want to install Windows 2000\n(depreciated)") # I want to install Windows 2000\n(depreciated)
    window.chb_usb.setText("Add USB support") # Add USB support

    window.btn_prev9.setText("< Antérieur") # < Previous
    window.btn_finish.setText("Finir") # Finish
    window.btn_cancel9.setText("Annuler") # Cancel

def translateStartVmFR(window, vmname):
    window.setWindowTitle(f"EmuGUI - Start {vmname}")
    window.label_4.setText("Date & heure") # Date & Time
    window.label_3.setText("Boot from") # Boot from
    window.label_6.setText("TPM path (Linux only)") # TPM path (Linux only)
    window.label_7.setText("Create the TPM from the terminal!") # Create the TPM from the terminal!

    window.label_5.setText("""
    Note: If the VM doesn't start within five minutes, then you should check the VM and QEMU settings.
    """) # Note: If the VM doesn't start within five minutes, then you should check the VM and QEMU settings.

    window.pushButton.setText("Naviguer") # Browse
    window.pushButton_2.setText("Naviguer") # Browse
    window.pushButton_6.setText("Naviguer") # Browse
    window.pushButton_5.setText("Set to system") # Set to system
    window.pushButton_3.setText("Start VM") # Start VM
    window.pushButton_4.setText("Annuler") # Cancel
    window.checkBox.setText("Use RTC option") # Use RTC option

    # Combo box for boot
    i = 0

    while i < window.comboBox.count():
        if window.comboBox.itemText(i) == "Let QEMU decide" or window.comboBox.itemText(i) == "QEMU überlassen":
            window.comboBox.setItemText(i, "Let QEMU decide") # Let QEMU decide
            break

        i += 1

def translateVmExistsFR(window):
    window.label.setText(
        "Sorry, but a VM with this name already exists."
        ) # Sorry, but a VM with this name already exists.

    window.label_2.setText(
        "Please consider either deleting that VM or thinking of a new name."
        ) # Please consider either deleting that VM or thinking of a new name.

    window.pushButton.setText("Accord") # OK

def translateVhdExistsFR(window):
    # The dialog which used to use this translation function is no longer in use.
    window.label.setText(
        "Sorry, but the disk you want to create is already existant."
        ) # Sorry, but the disk you want to create is already existant.

    window.label_2.setText("Do you want to keep or overwrite it?") # Do you want to keep or overwrite it?

    window.pushButton.setText("Overwrite") # Overwrite
    window.pushButton_2.setText("Keep") # Keep

def translateSettingsPendingFR(window):
    # The dialog which used to use this translation function is no longer in use.
    window.label.setText("You didn't setup the QEMU paths.")
    window.label_2.setText("Please go to settings to do that and try again afterwards.")

    window.pushButton.setText("Accord") # OK

def translateVmTooNewFR(window):
    window.label.setText(
        "This VM is made with a version of EmuGUI that is too new. Please use a later version!"
        ) # This VM is made with a version of EmuGUI that is too new. Please use a later version!

    window.pushButton.setText("Accord") # OK

def translateQemuSysMissingFR(window, arch):
    window.label.setText(
        f"Sorry but EmuGUI is not configured for using \"qemu-system-{arch}\" yet.\nThis component however is necessary to start this virtual machine.\nPlease go to Settings/QEMU to solve this issue."
        ) # Sorry but EmuGUI is not configured for using \"qemu-system-{arch}\" yet.\nThis component however is necessary to start this virtual machine.\nPlease go to Settings/QEMU to solve this issue.

    window.pushButton.setText("Accord") # OK

def translateQemuImgMissingFR(window):
    window.label.setText(
        "Sorry but EmuGUI is not configured for using \"qemu-img\" yet.\nThis component however is necessary to create or edit virtual machines.\nPlease go to Settings/QEMU to solve this issue."
        ) # Sorry but EmuGUI is not configured for using \"qemu-img\" yet.\nThis component however is necessary to create or edit virtual machines.\nPlease go to Settings/QEMU to solve this issue.

    window.pushButton.setText("Accord") # OK

def translateEditVMFR(window, vmname):
    window.setWindowTitle(f"EmuGUI - Edit {vmname}")

    # Buttons on all tabs
    window.btn_cancel.setText("Annuler") # Cancel
    window.btn_ok.setText("Accord") # OK

    # Tab names
    window.tabWidget.setTabText(0, "Général") # General
    window.tabWidget.setTabText(1, "Machine") # Machine
    window.tabWidget.setTabText(2, "Virtual hard disks") # Virtual hard disks
    window.tabWidget.setTabText(3, "Périphériques") # Peripherals
    window.tabWidget.setTabText(4, "BIOS") # BIOS
    window.tabWidget.setTabText(6, "Additional components") # Additional components

    # Translations for General tab
    window.lbl_name.setText("Nom") # Name
    window.lbl_arch.setText("Architecture") # Architecture

    # Translations for Machine tab
    window.lbl_cpu.setText("Unité centrale") # CPU
    window.lbl_machine.setText("Machine") # Machine
    window.lbl_ram.setText("RAM in MB") # RAM in MB

    i = 0

    while i < window.cb_cpu.count():
        if window.cb_cpu.itemText(i) == "Let QEMU decide" or window.cb_cpu.itemText(i) == "QEMU überlassen":
            window.cb_cpu.setItemText(i, "Let QEMU decide") # Let QEMU decide
            break

        i += 1

    i = 0

    while i < window.cb_machine.count():
        if window.cb_machine.itemText(i) == "Let QEMU decide" or window.cb_machine.itemText(i) == "QEMU überlassen":
            window.cb_machine.setItemText(i, "Let QEMU decide") # Let QEMU decide
            break

        i += 1

    # Translations for VHD tab
    window.lbl_vhdu.setText("VHD usage") # VHD usage
    window.lbl_vhdp.setText("VHD path") # VHD path
    window.lbl_vhdf.setText("VHD file format") # VHD file format
    window.lbl_maxsize.setText("Maximum size") # Maximum size
    window.btn_vhdp.setText("Browse") # Browse
    
    # Combobox for VHD usage
    i = 0

    while i < window.cb_vhdu.count():
        if window.cb_vhdu.itemText(i) == "Create a new virtual hard drive":
            window.cb_vhdu.setItemText(i, "Create a new virtual hard drive") # Create a new virtual hard drive
            break

        i += 1

    i = 0

    while i < window.cb_vhdu.count():
        if window.cb_vhdu.itemText(i) == "Add an existing virtual hard drive":
            window.cb_vhdu.setItemText(i, "Add an existing virtual hard drive") # Add an existing virtual hard drive
            break

        i += 1

    i = 0

    while i < window.cb_vhdu.count():
        if window.cb_vhdu.itemText(i) == "Don't add a virtual hard drive":
            window.cb_vhdu.setItemText(i, "Don't add a virtual hard drive") # Don't add a virtual hard drive
            break

        i += 1

    window.lbl_cdc1.setText("CD controller 1") # CD controller 1
    window.lbl_cdc2.setText("CD controller 2") # CD controller 2

    i = 0

    while i < window.cb_cdc1.count():
        if window.cb_cdc1.itemText(i) == "Let QEMU decide" or window.cb_cdc1.itemText(i) == "QEMU überlassen":
            window.cb_cdc1.setItemText(i, "Let QEMU decide") # Let QEMU decide
            break

        i += 1

    i = 0

    while i < window.cb_cdc2.count():
        if window.cb_cdc2.itemText(i) == "Let QEMU decide" or window.cb_cdc2.itemText(i) == "QEMU überlassen":
            window.cb_cdc2.setItemText(i, "Let QEMU decide") # Let QEMU decide
            break

        i += 1

    window.lbl_hddc.setText("HDD controller") # HDD controller

    i = 0

    while i < window.cb_hddc.count():
        if window.cb_hddc.itemText(i) == "Let QEMU decide" or window.cb_hddc.itemText(i) == "QEMU überlassen":
            window.cb_hddc.setItemText(i, "Let QEMU decide") # Let QEMU decide
            break

        i += 1

    # Translations for Peripherals tab
    window.lbl_mouse.setText("Souris") # Mouse type
    window.lbl_kbdtype.setText("Clavier") # Keyboard type
    
    # Translations for BIOS tab
    # Location of external BIOS file (Leave empty to use the default BIOS)
    window.lbl_biosloc.setText("Location of external BIOS file (Leave empty to use the default BIOS)")
    window.lbl_biosf.setText("External BIOS file") # External BIOS file
    window.btn_biosf.setText("Browse") # Browse

    # Translations for Linux tab
    window.lbl_kernel.setText("Linux kernel") # Linux kernel
    window.lbl_initrd.setText("Linux initrd image") # Linux initrd image
    window.lbl_cmd.setText("Linux cmd arguments") # Linux cmd arguments
    window.btn_kernel.setText("Browse") # Browse
    window.btn_initrd.setText("Browse") # Browse

    # Translations for Additional components tab
    window.lbl_vga.setText("VGA") # VGA
    window.lbl_net.setText("Réseau") # Network adapter
    window.lbl_sound.setText("Carte son") # Sound card
    window.lbl_addargs.setText("Additional arguments (if necessary)") # Additional arguments (if necessary)
    window.lbl_cpuc.setText("CPU cores") # CPU cores
    window.chb_usb.setText("Add USB support") # Add USB support
    window.lbl_accel.setText("Accélération") # Acceleration

def translateErrDialogFR(window, errcode):
    window.setWindowTitle(f"EmuGUI - Error")
    
    if errcode.startswith("C"):
        window.label.setText("EmuGUI encountered a critical error and needs to be closed.") # EmuGUI encountered a critical error and needs to be closed.

    elif errcode.startswith("E"):
        window.label.setText("EmuGUI encountered an error.") # EmuGUI encountered an error.

    elif errcode.startswith("W"):
        window.label.setText("EmuGUI has to warn you.") # EmuGUI has to warn you.

    else:
        window.label.setText("EmuGUI has something to say.") # EmuGUI has something to say.

    window.label_2.setText("Error Code: " + errcode) # Error Code:

    window.label_3.setText(
        "If this error occurs multiple times, contact your administrator and/or ask for help on the EmuGUI Discord Server or on its GitHub repository."
        ) # If this error occurs multiple times, contact your administrator and/or ask for help on the EmuGUI Discord Server or on its GitHub repository.
    
    window.pushButton.setText("Accord") # OK