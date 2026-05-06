import logging
import os
from datetime import datetime

LOG_FILE=f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
# Use /tmp on Linux (EB) since it's always writable, otherwise use project-relative logs/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if os.name == 'nt':  # Windows (local dev)
    LOG_DIR = os.path.join(BASE_DIR, "logs")
else:  # Linux (EB production)
    LOG_DIR = os.path.join("/tmp", "logs")
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE_PATH=os.path.join(LOG_DIR,LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)