import os
import platform
import subprocess
import json
import time
import requests
from hashlib import sha256

# Configuration
CHECK_INTERVAL = 1800  # 30 minutes
API_ENDPOINT = "http://localhost:5000/api/report"
MACHINE_ID = sha256(platform.node().encode()).hexdigest()

def is_disk_encrypted():
    try:
        system = platform.system()
        if system == "Windows":
            output = subprocess.check_output("manage-bde -status", shell=True).decode()
            return "Percentage Encrypted: 100%" in output
        elif system == "Darwin":
            output = subprocess.check_output("fdesetup status", shell=True).decode()
            return "FileVault is On." in output
        elif system == "Linux":
            output = subprocess.getoutput("lsblk -o NAME,TYPE,FSTYPE | grep crypt")
            return bool(output)
    except Exception as e:
        return False


def is_os_updated():
    try:
        system = platform.system()
        if system == "Windows":
            output = subprocess.getoutput("powershell UsoClient ScanInstallWait")
            # You can't actually check if updates are pending without admin permission or third-party tools.
            # So we'll use Windows Update Status service (simplified)
            history = subprocess.getoutput("powershell Get-WindowsUpdateLog")
            return "No updates available" in history or "No applicable updates found" in history
        elif system == "Darwin":
            output = subprocess.getoutput("softwareupdate -l")
            return "No new software available" in output
        elif system == "Linux":
            output = subprocess.getoutput("apt list --upgradable 2>/dev/null")
            return "upgradable" not in output
    except Exception as e:
        return False


def is_antivirus_installed():
    try:
        system = platform.system()
        if system == "Windows":
            output = subprocess.getoutput('powershell "Get-MpComputerStatus"')
            return "RealTimeProtectionEnabled" in output
        elif system == "Darwin":
            return False  # macOS doesn't come with default AV
        elif system == "Linux":
            output = subprocess.getoutput("systemctl status clamav-daemon")
            return "active (running)" in output
    except Exception:
        return False

def is_sleep_configured():
    try:
        system = platform.system()
        if system == "Windows":
            output = subprocess.getoutput('powercfg -query SCHEME_CURRENT SUB_SLEEP')
            return "0x0000000a" in output.lower()
        elif system == "Darwin":
            output = subprocess.getoutput("pmset -g | grep sleep")
            return "sleep" in output and int(output.split()[-1]) <= 10
        elif system == "Linux":
            output = subprocess.getoutput("gsettings get org.gnome.settings-daemon.plugins.power sleep-inactive-ac-timeout")
            return int(output.strip()) <= 600
    except Exception:
        return False

def get_system_status():
    return {
        "machine_id": MACHINE_ID,
        "os": platform.system(),
        "disk_encrypted": is_disk_encrypted(),
        "os_updated": is_os_updated(),
        "antivirus_present": is_antivirus_installed(),
        "sleep_configured": is_sleep_configured(),
    }

def send_to_server(data):
    try:
        response = requests.post(API_ENDPOINT, json=data)
        print("Sent to server:", response.status_code)
    except Exception as e:
        print("Error sending to server:", str(e))

def run_daemon():
    last_status = {}
    while True:
        current_status = get_system_status()
        if current_status != last_status:
            send_to_server(current_status)
            last_status = current_status
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    run_daemon()
