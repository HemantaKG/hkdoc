# Executive Disable Bit (XD)
- Execute Disable Bit (EDB) is an Intel hardware-based security feature that can help reduce system exposure to viruses and malicious code. EDB allows the processor to classify areas in memory where application code can or cannot execute.
# Protected Processor Inventory Number (PPIN)
- A solution for inventory management available on Intel Xeon processor E5 product families for use in server platforms. PPIN defaults to disabled and follows an 'opt-in' model to enable it. Once PPIN is enabled, a reboot is necessary to make it available to privileged software, such as the OS or VMM and another ring 0 applications.
# Advanced Programmable Interrupt Controller (X2APIC)
- APIC is a family of interrupt controllers. As its name suggests, the APIC is more advanced than Intel's 8259 Programmable Interrupt Controller (PIC), particularly enabling the construction of multiprocessor systems. It is one of the several architectural designs intended to solve interrupt routeing efficiency issues in multiprocessor computer systems. The xAPIC was introduced with the Pentium 4, while the x2APIC is the most recent generation of the Intel's programmable interrupt controller, introduced with the Nehalem microarchitecture. The major improvements of the x2APIC address the number of supported CPUs and performance of the interface.
# Intel Advanced Encryption Standard New Instructions (AES-NI)
- Advanced Encryption Standard Instruction Set (or the Intel Advanced Encryption Standard New Instructions; AES-NI) is an extension to the x86 instruction set architecture for microprocessors from Intel and AMD proposed by Intel in March 2008.[1] The purpose of the instruction set is to improve the speed of applications performing encryption and decryption using the Advanced Encryption Standard (AES). Most modern compilers can emit AES instructions. Much security and cryptography software supports the AES instruction set, including Cryptography API: Next Generation (CNG), Linux's Crypto API, Java 7 HotSpot, Network Security Services (NSS) version >=3.13 (used by Firefox and Google Chrome), Solaris Cryptographic Framework[30] on Solaris >=10, FreeBSD's OpenCrypto API, OpenSSL >=1.0.1, FLAM/FLUC >=5.1.08
# System Management Mode (SMM) and System Management Interrupt (SMI)
- System Management Mode (SMM) sometimes called ring-2, is an operating mode of x86 central processor units (CPUs) in which all normal execution, including the operating system, is suspended. A special separate software, which is usually part of the firmware or a hardware-assisted debugger, is then executed with high privileges. SMM is a special-purpose operating mode provided for handling system-wide functions like power management, system hardware control, or proprietary OEM designed code. SMM is entered via the SMI (system management interrupt), which is caused by:
  * Motherboard hardware or chipset signaling via a designated pin SMI# of the processor chip. This signal can be an independent event.
  * Software SMI triggered by the system software via an I/O access to a location considered special by the motherboard logic (port 0B2h is common).
  * An I/O write to a location which the firmware has requested that the processor chip act on.
# Intel I/O Acceleration Technology (I/OAT) and Direct Cache Access (DCA)
- I/OAT is the name for a collection of techniques by Intel to improve network throughput. The most significant of these is the DMA engine. The DMA engine is meant to offload from the CPU the copying of [socket buffer] data to the user buffer. This is not a zero-copy receive, but does allow the CPU to do other work while the copy operations are performed by the DMA engine.
# DRAM RAPL Baseline
- Running Average Power Limit (RAPL) interface, which among things provides estimated energy measurrements for the CPUs, integrated GPU, and DRAM. These measurements are easily accessible by the user and can be gathered by a wide variety of tools, including the Linux 'perf_event' interface.
# xHCI
- eXtensible Host Controller Interface (xHCI) is a computer interface specification that defines a register-level description of a host controller for Universal Serial Bus (USB), which is capable of interfacing with USB 1.x, 2.0, and 3.x compatible devices.
# EHCI
- Enhanced Host Controller Interface (EHCI) is a high-speed controller standard applicable to USB 2.0. UHCI- and OHCI-based systems, as existed previously, entailed greater complexity and costs than necessary.
# AHCI
- AHCI stand for Advance Host Controller Interface. AHCI is a hardware mechanism that allows software to communicate with Serial ATA (SATA) devices that are designed to offer features not offered by Parallel ATA (PATA) controllers, such as hot-plugging and native command queuing (NCQ).
# PCIe
- Peripheral Component Interconnect Express (PCIe or PCI-E) is a serial expansion bus standard for connecting a computer to one or more peripheral devices.
# PCI
- Short for Peripheral Component Interconnect, a local bus standard developed by Intel Corporation. Most modern PCs include a PCI bus in addition to a more general ISA expansion bus. PCI is also used on some versions of the Macintosh computer. PCI is a 64-bit bus, though it is usually implemented as a 32-bit bus.
# WHEA Support
- This feature Enables the Windows Hardware Error Architecture (WHEA) support for the Windows 2008 (or a later vision) operating system.
# ACPI
- ACPI (Advanced Configuration and Power Interface) is an industry specification for the efficient handling of power consumption in desktop and mobile computers. ACPI specifies how a computer's basic input/output system, operating system, and peripheral devices communicate with each other about power usage.
# iSCSI
- iSCSI is an acronym for Internet Small Computer Systems Interface, an Internet Protocol (IP)-based storage networking standard for linking data storage facilities. It provides block-level access to storage devices by carrying SCSI commands over a TCP/IP network.
