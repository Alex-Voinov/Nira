import logging

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    COLORAMA = True
except ImportError:
    COLORAMA = False

class ColorFormatter(logging.Formatter):
    """Красивый цветной формат логов для консоли"""

    LEVEL_COLORS = {
        logging.DEBUG: Fore.CYAN,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.MAGENTA,
    }

    def format(self, record):
        if COLORAMA:
            color = self.LEVEL_COLORS.get(record.levelno, "")
            record.levelname = f"{color}{record.levelname}{Style.RESET_ALL}"
        return super().format(record)

def get_logger(name="app", level=logging.DEBUG):
    """Создает логгер с красивым форматированием"""
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = ColorFormatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger


# единый логгер по умолчанию
logger = get_logger()
