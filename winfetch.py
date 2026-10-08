import ctypes
import winreg

gpu_name_path = r"SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}\0000"
cpu_name_path = r"HARDWARE\DESCRIPTION\System\CentralProcessor\0"
windows_current_version_path = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion"

# CPU name
cpu_name_location = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, cpu_name_path)
cpu_name = winreg.QueryValueEx(cpu_name_location, "ProcessorNameString")
winreg.CloseKey(cpu_name_location)

windows_current_version_location = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, windows_current_version_path)

# Registered Owner's Name
registered_owner = winreg.QueryValueEx(windows_current_version_location, "RegisteredOwner")

# Build number
build_number = winreg.QueryValueEx(windows_current_version_location, "CurrentBuildNumber")
build_number_int = int(build_number[0])

# Display Version
display_version = winreg.QueryValueEx(windows_current_version_location, "DisplayVersion")

# Product Name
product_name = winreg.QueryValueEx(windows_current_version_location, "ProductName")

winreg.CloseKey(windows_current_version_location)

# GPU Name
gpu_name_location = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, gpu_name_path)
gpu_name = winreg.QueryValueEx(gpu_name_location, "HardwareInformation.AdapterString")
winreg.CloseKey(gpu_name_location)

# Resolution Scale
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()

width = user32.GetSystemMetrics(0)
height = user32.GetSystemMetrics(1)

resolution = f"{width}x{height}"

# Uptime Record
uptime_millisecond = ctypes.windll.kernel32.GetTickCount64()
uptime_second = (uptime_millisecond // 1000) % 60
uptime_minute = (uptime_millisecond // 1000 // 60) % 60
uptime_hour = (uptime_millisecond // 1000 // 60 // 60) % 24
uptime_day = (uptime_millisecond // 1000 // 60 // 60 // 24)

# Uptime checker
if uptime_day == 0:
    uptime_text = f"Uptime: {uptime_hour} hours {uptime_minute} minutes {uptime_second} seconds"
else:
    uptime_text = f"Uptime: {uptime_day} days {uptime_hour} hours {uptime_minute} minutes {uptime_second} seconds"

# RAM status
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

total_ram_gb = round(ram.ullTotalPhys / (1024**3), 2)
avaible_ram_gb = round(ram.ullAvailPhys / (1024**3), 2)
ram_usage = round(total_ram_gb - avaible_ram_gb, 2)

# Product name regulator
if build_number_int >= 22000:
    real_product_name = product_name[0].replace("Windows 10", "Windows 11")
else:
    real_product_name = product_name[0]

system_informations = [ 
    "",
    f"OS: {real_product_name}",
    f"Version: {display_version[0]}",
    f"Registered: {registered_owner[0]}",
    f"Resolution: {resolution}",
    f"CPU: {cpu_name[0]}",
    f"GPU: {gpu_name[0]}", 
    f"RAM Usage: {ram_usage}/{total_ram_gb} GB",
    uptime_text,
    "",
    "",
    "",
    "",
    "",
    ""
]

logo = [
"    ⠀⠀⠀⠀⣿⣿⠀⠀⠀⠀⠀ ⠀⠀",
"⠀⠀⠀⢀⣴⠇⠀ ⣿⣿ ⠀⠘⣦⡀⠀⠀⠀",
"⠀⠀⣰⣿⠃⠀⠀⠀⣿⣿⠀⠀⠀⠘⣿⣆⠀⠀",
"⠀⢾⣿⣇⠀⠀⠀⠀⣿⣿⠀⠀⠀⠀⣸⣿⣷⠄",
"⠀⠈⠻⣿⣷⣄⠀⠀⣿⣿⠀⠀⣠⣾⣿⠟⠁⠀",
"⠀⠀⠀⠀⠻⣿⣷⣄⣿⣿⣠⣾⣿⠟⠁⠀⠀⠀",
"⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀",
"⠀⠀⠀⠀⠀⢀⣴⣿⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀",
"⠀⠀⠀⢀⣴⣿⣿⠿⣿⣿⠿⣿⣿⣦⡀⠀⠀⠀",
"⠀⢀⣰⣿⣿⠟⠁⠀⣿⣿⠀⠈⠻⣿⣿⣦⡀⠀",
"⠰⣿⣿⣿⠁⠀⠀⠀⣿⣿⠀⠀⠀⠈⣻⣿⣿⠆",
"⠀⠀⠹⣿⣷⣄⠀⠀⣿⣿⠀⠀⣠⣾⣿⠟⠁⠀",
"⠀⠀⠀⠈⠻⣿⣷⣄⣿⣿⣠⣾⣿⠟⠁⠀⠀⠀",
"⠀⠀⠀⠀⠀⠈⠻⣿⣿⣿⣿⠟⠁⠀⠀⠀⠀⠀",
"⠀⠀⠀⠀⠀⠀⠀⠈⢻⡟⠁⠀⠀⠀⠀⠀⠀⠀"
]

for logo, system_informations in zip(logo, system_informations):
    print(f"{logo}                     {system_informations}")

