from loguru import logger
import sys
import logging

# Remove default handlers to prevent duplicate logs
logger.remove()

# Console Logging (With Colors)
logger.add(sys.stdout, format="{time} - {level} - {message}", level="DEBUG", colorize=True)

# File Logging (Rotating Logs: Max 5MB, Keep Last 5 Logs)
logger.add("debug_log.log", rotation="5 MB", retention=5, level="DEBUG", enqueue=True)

# Redirect Uvicorn Logs to Loguru
class InterceptHandler(logging.Handler):
    def emit(self, record):
        logger_opt = logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelname, record.getMessage())

logging.getLogger("uvicorn.access").handlers = [InterceptHandler()]
logging.getLogger("uvicorn.error").handlers = [InterceptHandler()]
logging.getLogger("uvicorn").handlers = [InterceptHandler()]

logger.info("🚀 Loguru is initialized globally!")


