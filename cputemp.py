import subprocess

powershell_command = 'Start-Process "LibreHardwareMonitor-net472/LibreHardwareMonitor.exe" -WindowStyle Hidden'

subprocess.run(["powershell", "-Command", powershell_command])
