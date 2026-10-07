import ctypes
import winreg


cpu_name_path = r"HARDWARE\DESCRIPTION\System\CentralProcessor\0"

cpu_name_location = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, cpu_name_path)
cpu_name = winreg.QueryValueEx(cpu_name_location, "ProcessorNameString")

print(cpu_name[0])

winreg.CloseKey(cpu_name_location)



class MemoryStatusEx(ctypes.Structure):
    _fields_ = [
        ("dwLength", ctypes.c_ulong),
        ("dwMemoryLoad", ctypes.c_ulong),
        ("ullTotalPhys", ctypes.c_ulonglong),
        ("ullAvailPhys", ctypes.c_ulonglong),
        ("ullTotalPageFile", ctypes.c_ulonglong),
        ("ullAvailPageFile", ctypes.c_ulonglong),
        ("ullTotalVirtual", ctypes.c_ulonglong),
        ("ullAvailVirtual", ctypes.c_ulonglong),
        ("ullAvailExtendedVirtual", ctypes.c_ulonglong)
    ]

ram = MemoryStatusEx()
ram.dwLength = ctypes.sizeof(ram)
ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(ram))
print(ram.ullTotalPhys)