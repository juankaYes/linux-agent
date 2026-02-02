import subprocess
from my_logging.config import get_logger

# Configure logging
logger = get_logger(__name__)

def run_command(command: str) -> str:
    """Run a shell command and return its output."""
    logger.info(f"Executing command: {command}")
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            check=True,
        )
        logger.info(f"Command executed successfully: {command}")
        return result.stdout
    except subprocess.CalledProcessError as e:
        logger.error(f"Command failed: {command}\nError: {e}")
        return f"Error executing command '{command}': {e}"


if __name__ == "__main__":
    # Example usage
    print(run_command("uname -a"))