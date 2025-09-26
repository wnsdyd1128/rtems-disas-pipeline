# objdump_runner.py
import subprocess
from utils import get_logger
from pathlib import Path

logger = get_logger()
def run_objdump(binary_path: str | Path) -> str:
    """
    objdump -d 실행 결과를 문자열로 반환합니다.
    """
    binary = Path(binary_path)
    logger.debug(f'Executable: {binary}')
    try:
        result = subprocess.run(
            ["sparc-rtems6-objdump", "-d", str(binary)],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"objdump 실행 실패: {binary}") from e
