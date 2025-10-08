import sys


class Logger:

    def __init__(self, logs_file_path: str):
        from loguru import logger
        logger.remove()

        logger.add(
            sys.stdout,
            format=(
                "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                "<level>{level: <8}</level> | "
                "<cyan>{module}</cyan>.<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
                "<level>{message}</level>"
            ),
            level="INFO",
            colorize=True
        )

        logger.add(
            logs_file_path,
            format=(
                "{time:YYYY-MM-DD HH:mm:ss} | "
                "{level: <8} | "
                "{module}.{function}:{line} | "
                "{message}"
            ),
            level="DEBUG",
            retention="30 days",
            compression=None,
            enqueue=True  # asyncio write
        )
        self.logger = logger


