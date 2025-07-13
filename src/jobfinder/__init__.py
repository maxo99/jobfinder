__version__ = "0.9.0"

import os
import sys
import logging
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT.joinpath("data")
RAW_DATA_DIR = DATA_DIR.joinpath("raw")
JOBS_DATA_FILE = DATA_DIR.joinpath("jobs_data.csv")
if not DATA_DIR.exists():
    DATA_DIR.mkdir(parents=True, exist_ok=True)
if not RAW_DATA_DIR.exists():
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)





def _setup_logging():
    _lvl_string = os.environ.get("LOG_LEVEL", "INFO")
    _level = getattr(logging, _lvl_string)
    _log_formatter = logging.Formatter(
        fmt="%(asctime)s %(levelname)s [%(name)-12s]:%(message)s", datefmt="%m-%d %H:%M"
    )
    _handlers = []
    _file_handler = logging.FileHandler(DATA_DIR.joinpath("out.log"))
    _file_handler.setFormatter(_log_formatter)
    _handlers.append(_file_handler)
    _console_handler = logging.StreamHandler(sys.stdout)
    _console_handler.setFormatter(_log_formatter)
    _handlers.append(_console_handler)
    _handlers.extend(
        [_file_handler, _console_handler]
    )

    if os.environ.get("AWS_ACCESS_KEY_ID", "") and os.environ.get(
        "AWS_SECRET_ACCESS_KEY", ""
    ):
        import watchtower

        # If AWS credentials are set, we can use CloudWatch logging
        _handlers.append(watchtower.CloudWatchLogHandler())

    logging.basicConfig(level=_level, handlers=_handlers)






__all__ = (
    "PROJECT_ROOT",
    "DATA_DIR",
)
