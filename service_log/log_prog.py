import logging
from pathlib import Path

def setup_logger():
    documents_dir = Path.home() / "Documents"

    project_dir = documents_dir / "Pr_os_15_farm"
    project_dir.mkdir(parents=True, exist_ok=True)

    log_file = project_dir / "farm.log"

    logger = logging.getLogger("farm_logger")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)

    if not logger.hasHandlers():
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    logger.info("=== Программа Pr_os_15_farm запущена ===")
    return logger