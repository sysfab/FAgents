import logging
import sys


class Formatter(logging.Formatter):
    COLORS = {
        logging.DEBUG: "\x1b[90m",
        logging.INFO: "\x1b[97m",
        logging.WARNING: "\x1b[93m",
        logging.ERROR: "\x1b[91m",
        logging.CRITICAL: "\x1b[95m",
    }

    RESET = "\x1b[0m"

    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelno, "")

        level = f"{('[' + record.levelname + ']'):<9}"
        name = f"{record.name:<24}"

        time = self.formatTime(record, "%H:%M:%S")

        msg = record.getMessage()

        return f"{color}[{time}] {level} {name} {msg}{self.RESET}"


def setup_logger(level=logging.INFO):
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(Formatter())

    root = logging.getLogger()
    root.setLevel(level)
    root.handlers.clear()
    root.addHandler(handler)
