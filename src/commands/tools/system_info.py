from system.hardware_info import HardwareInfo
from system.system_info import LinuxSystemInfo
from langchain.tools import tool

@tool
def get_system_info_tool() -> str:
    """Get detailed system information about hardware and software.
    Returns:
        Information about the Linux system:
            "distributor"
            "description"  
            "release"  
            "codename"
            "kernel"
        Information about the hardware:
            "cpu"
            "ram"
            "disk"
            "gpu"
            "architecture"
    """
    linux_info = LinuxSystemInfo().to_string()
    hardware_info = HardwareInfo().to_string()
    return f"{linux_info}\n{hardware_info}"

