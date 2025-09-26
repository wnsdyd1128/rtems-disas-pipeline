# utils.py
from loguru import logger

# 기본 설정: stderr 출력 + 로그 포맷
logger.remove()  # 기본 핸들러 제거
logger.add(
    sink=lambda msg: print(msg, end=""),  # stderr에 바로 출력
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
           "<level>{level: <8}</level> | "
           "<cyan>{name}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="DEBUG"
)

def get_logger():
    return logger
