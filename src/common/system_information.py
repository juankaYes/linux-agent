from commands.utils import run_command

class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]

class LinuxSystemInfo(metaclass=SingletonMeta):
    def __init__(self):
        info = run_command("lsb_release -a")
        self._distributor = self._parse_info(info, "Distributor ID") # re.search(r"Distributor ID:\s+(.*)", info).group(1)
        self._description = self._parse_info(info, "Description")
        self._release = self._parse_info(info, "Release")
        self._codename = self._parse_info(info, "Codename")
        self._kernel = run_command("uname -r").strip()
        
    def _parse_info(self, info: str, key: str) -> str:
        for line in info.splitlines():
            if line.startswith(key):
                return line.split(":")[1].strip()
        return "Unknown"
    
    def to_string(self):
        return (f"Distributor: {self._distributor}\n"
                f"Description: {self._description}\n"
                f"Release: {self._release}\n"
                f"Codename: {self._codename}\n"
                f"Kernel: {self._kernel}\n")
    
    def to_dict(self):
        return {
            "distributor": self._distributor,
            "description": self._description,
            "release": self._release,
            "codename": self._codename,
            "kernel": self._kernel
        }
    
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

LinuxSystemInfo()
HardwareInfo()