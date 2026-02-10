from commands.utils import run_command
from .base import SingletonMeta

    
class HardwareInfo(metaclass=SingletonMeta):
    def __init__(self):
        self._cpu = run_command("lscpu | grep 'Model name'").split(":")[1].strip()
        self._ram = run_command("cat /proc/meminfo | grep 'MemTotal'").split(":")[1].strip()
        self._disk = run_command("lsblk -d -o NAME,SIZE,TYPE | grep 'disk'").strip()
        self._gpu = run_command("lshw -C display").strip()
        self._architecture = run_command("uname -m").strip()

    def to_string(self):
        return (f"CPU: {self._cpu}\n"
                f"RAM: {self._ram}\n"
                f"Disk: {self._disk}\n"
                f"GPU: {self._gpu}\n"
                f"Architecture: {self._architecture}\n")
    
    def to_dict(self):
        return {
            "cpu": self._cpu,
            "ram": self._ram,
            "disk": self._disk,
            "gpu": self._gpu,
            "architecture": self._architecture
        }
