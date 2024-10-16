import logging  
from datetime import datetime
from logging.handlers import RotatingFileHandler
from pathlib import Path
from rich.console import Console
from rich.logging import RichHandler
from platformdirs import user_log_dir

# Setup console with rich for fancy printing
console = Console()

def setup_logging(app_name: str):
    # Log file name
    log_dir = user_log_dir(app_name)
    log_path = Path(log_dir) / f"{app_name}.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Create a custom formatter for the file handler with milliseconds
    file_formatter = logging.Formatter(
        '%(asctime)s.%(msecs)03d - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Create a rotating file handler
    file_handler = RotatingFileHandler(str(log_path), maxBytes=2000000, backupCount=5)
    file_handler.setFormatter(file_formatter)

    # Create a rich handler for terminal output with milliseconds
    rich_handler = RichHandler(
        console=console,
        show_time=True,
        rich_tracebacks=True,
        omit_repeated_times=False,
        log_time_format="[%X.%f]"  # Set format to include milliseconds
    )

    # Set a custom format for the RichHandler to exclude logger name
    console_formatter = logging.Formatter(
        "%(message)s"  # Only display the message, omitting 'root' or any logger name
    )
    rich_handler.setFormatter(console_formatter)

    # Setup the root logger
    logging.basicConfig(
        level=logging.DEBUG,  # Capture all log levels
        handlers=[
            rich_handler,     # RichHandler for console
            file_handler      # File handler for saving logs
        ]
    )


def get_current_time():
    """Get the current time formatted as a string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def log_info(message: str):
    """Log an informational message to the console and log file."""
    logging.info(message)

def log_warning(message: str):
    """Log a warning message to the console and log file."""
    logging.warning(message)

def log_error(message: str):
    """Log an error message to the console and log file."""
    logging.error(message)

def log_debug(message: str):
    """Log a debug message to the console and log file."""
    logging.debug(message)

def log_critical(message: str):
    """Log a critical error message to the console and log file."""
    logging.critical(message)

def log_success(message: str):
    """Log a success message to the console and log file."""
    logging.info(f"SUCCESS: {message}")

# ANSI escape codes for color
RESET = "\033[0m"
ORANGE_BOLD = "\033[1;33m"
WHITE_BOLD = "\033[1;37m"
GREEN = "\033[32m"
GREEN_BOLD = "\033[1;32m"
RED = "\033[31m"
RED_BOLD = "\033[1;31m"
YELLOW_BOLD = "\033[1;33m"

def log_step(step_nb, end, name, status_code=0, issues_count=0, warnings_count=0, duration=None):
    bar = "|||||||||||||||||||||||||||||||||||||||||||||||||||||||"
    separator = f"{RED_BOLD}======================================================={RESET}"

    # Determine status message and color
    if status_code == 0:
        status_msg = "Success"
        status_color = GREEN_BOLD
    elif status_code == 1:
        status_msg = "Error"
        status_color = RED_BOLD
    else:
        status_msg = "Unknown Status"
        status_color = YELLOW_BOLD

    if end == 0:
        logging.info(f"{ORANGE_BOLD}{bar}{RESET}")
        logging.info(f"{ORANGE_BOLD}STEP #{step_nb} | {WHITE_BOLD}{name}{RESET} | {GREEN}Starting{RESET}")
        logging.info(f"{ORANGE_BOLD}{bar}{RESET}")
    elif end == 1:
        logging.info(f"{separator}")
        logging.info(f"{RED_BOLD}END of STEP #{step_nb} | {WHITE_BOLD}{name}{RESET}")
        logging.info(f"{separator}")
        
        # Final status and additional information
        logging.info(f"{ORANGE_BOLD}Status: {status_color}{status_msg}{RESET}")
        logging.info(f"{ORANGE_BOLD}Issues: {WHITE_BOLD}{issues_count}{RESET}, Warnings: {YELLOW_BOLD}{warnings_count}{RESET}")
        
        # Optional: Show duration if provided
        if duration is not None:
            logging.info(f"{ORANGE_BOLD}Duration: {WHITE_BOLD}{duration}s{RESET}")
        
        logging.info(f"{separator}")
    else:
        logging.error(f"{RED}Invalid 'end' parameter. Use 0 for start and 1 for end.{RESET}")
