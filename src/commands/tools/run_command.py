from langchain.tools import tool
from commands.utils import run_command
from my_logging.config import get_logger

# Get Logger
logger = get_logger(__name__)

@tool
def run_command_tool(command: str) -> str:
    """Run a shell command and return its output."""
    return run_command(command)
