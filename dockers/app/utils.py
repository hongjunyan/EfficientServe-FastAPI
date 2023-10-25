from pathlib import Path
from loguru import logger


def create_dir(dir_path: [str, Path]) -> Path:
    dir_path = Path(dir_path).expanduser().absolute()
    if not dir_path.exists():
        dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def create_logger(task: str, log_dir: str) -> logger:
    task_logger = logger.bind(task=task)
    log_dir = create_dir(log_dir)
    log_file = str(log_dir.joinpath(f"{task}.log"))
    task_logger.add(log_file, format="{time:YYYY-MM-DD HH:mm:ss}|{name}.{function}.{line}|{level}|{message}",
                    rotation="50 MB", enqueue=True, encoding="utf8",
                    filter=lambda record: record["extra"]["task"] == task)
    return task_logger
