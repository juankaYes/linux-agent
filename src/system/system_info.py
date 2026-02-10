from commands.utils import run_command
from .base import SingletonMeta

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