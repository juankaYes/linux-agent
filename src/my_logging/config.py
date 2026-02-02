import logging
from pathlib import Path

LOGS_PATH = "./logs"
Path(LOGS_PATH).mkdir(exist_ok=True)
LOGFILE_PATH = Path(LOGS_PATH) / 'app.log'

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOGFILE_PATH),
        # logging.StreamHandler()
    ]
)

# Function to get a logger for a specific module
def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
