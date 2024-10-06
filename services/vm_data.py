class VirtualMachineData:
    def __init__(
        self,
        vm_name,
        arch,
        machine,
        cpu,
        cores,
        ram,
        vga,
        net,
        biosdir,
        biosfile,
        sound,
        kernel,
        initrd,
        linuxcmd,
        mouse,
        kbd,
        kbdlayout,
        usb_support,
        usb_controller,
        hwaccel,
        cd_control1,
        cd_control2,
        hda_control,
        cd1,
        cd2,
        floppy,
        timemgr,
        bootfrom,
        hda
    ):
        self.vm_name = vm_name
        self.arch = arch
        self.machine = machine
        self.cpu = cpu
        self.cores = cores
        self.ram = ram
        self.vga = vga
        self.net = net
        self.biosdir = biosdir
        self.biosfile = biosfile
        self.sound = sound
        self.kernel = kernel
        self.initrd = initrd
        self.linuxcmd = linuxcmd
        self.mouse = mouse
        self.kbd = kbd
        self.kbdlayout = kbdlayout
        self.usb_support = usb_support
        self.usb_controller = usb_controller
        self.hwaccel = hwaccel
        self.cd_control1 = cd_control1
        self.cd_control2 = cd_control2
        self.hda_control = hda_control
        self.cd1 = cd1
        self.cd2 = cd2
        self.floppy = floppy
        self.timemgr = timemgr
        self.bootfrom = bootfrom
        self.hda = hda
    
