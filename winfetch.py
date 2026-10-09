import os
import ctypes
import winreg
from ctypes import wintypes

gpu_name_path = r"SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}\0000"
cpu_name_path = r"HARDWARE\DESCRIPTION\System\CentralProcessor\0"
host_name_path = r"HARDWARE\DESCRIPTION\System\BIOS"
windows_current_version_path = r"SOFTWARE\Microsoft\Windows NT\CurrentVersion"

# Desktop name
computer_name = os.environ.get("COMPUTERNAME")
user_name = os.environ.get("USERNAME")

# OS Informations
with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, windows_current_version_path) as windows_current_version_location:
    build_number = int(winreg.QueryValueEx(windows_current_version_location, "CurrentBuildNumber")[0])
    display_version = winreg.QueryValueEx(windows_current_version_location, "DisplayVersion")[0]
    product_name = winreg.QueryValueEx(windows_current_version_location, "ProductName")[0]

# CPU name
with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, cpu_name_path) as cpu_name_location:
    cpu_name = winreg.QueryValueEx(cpu_name_location, "ProcessorNameString")[0]

# GPU Name
with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, gpu_name_path) as gpu_name_location:
    gpu_name = winreg.QueryValueEx(gpu_name_location, "HardwareInformation.AdapterString")[0]

# Host Name
with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, host_name_path) as host_name_location:
    host_name = winreg.QueryValueEx(host_name_location, "SystemProductName")[0]

# Terminal name
if "PROMPT" in os.environ:
    shell_name = "CMD"
elif "PSModulePath" in os.environ:
    shell_name = "PowerShell"
else:
    shell_name = "unknown shell"

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

if uptime_day == 0:
    uptime_text = f"Uptime: {uptime_hour} hours {uptime_minute} minutes {uptime_second} seconds"
else:
    uptime_text = f"Uptime: {uptime_day} days {uptime_hour} hours {uptime_minute} minutes {uptime_second} seconds"

# Disk status
free_bytes_available = wintypes.ULARGE_INTEGER()
total_number_of_bytes = wintypes.ULARGE_INTEGER()
total_number_of_free_bytes = wintypes.ULARGE_INTEGER()

disk_path_buffer = ctypes.create_unicode_buffer(100)
ctypes.windll.kernel32.GetLogicalDriveStringsW(100, disk_path_buffer)
disk_paths = [disk for disk in disk_path_buffer[:].split('\x00') if disk]

disk_info_list = []

for disk in disk_paths:
    disk_report = ctypes.windll.kernel32.GetDiskFreeSpaceExW(
        ctypes.c_wchar_p(disk),
        ctypes.byref(free_bytes_available),
        ctypes.byref(total_number_of_bytes),
        ctypes.byref(total_number_of_free_bytes)
    )

    if disk_report:
        disk_size = total_number_of_bytes.value / (1024 ** 3)
        disk_usage = disk_size - (total_number_of_free_bytes.value / (1024 ** 3))
        disk_info_list.append(f"{disk} {round(disk_usage, 2)}/{round(disk_size, 2)} GB")

disk_info_text = " | ".join(disk_info_list)

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
if build_number >= 22000:
    real_product_name = product_name.replace("Windows 10", "Windows 11")
else:
    real_product_name = product_name

system_informations = [ 
    "",
    f"{user_name}@{computer_name}",
    "-----------------------------------",
    f"OS: {real_product_name}",
    f"Version: {display_version}",
    f"Kernel: {build_number}",
    f"Terminal: {shell_name}",
    f"Host: {host_name}",
    f"Resolution: {resolution}",
    f"CPU: {cpu_name}",
    f"GPU: {gpu_name}", 
    f"RAM Usage: {ram_usage}/{total_ram_gb} GB",
    f"Disk Usage: {disk_info_text}",
    uptime_text,
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

for logo_line, info_line in zip(logo, system_informations):
    print(f"{logo_line}                 {info_line}")
