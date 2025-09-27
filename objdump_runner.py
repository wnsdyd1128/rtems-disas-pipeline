# objdump_runner.py
import subprocess
from pathlib import Path

def run_objdump(binary: Path) -> str:
    """
    objdump -d 실행 결과 문자열로 반환
    """
    if not binary.exists():
        raise FileNotFoundError(f"Binary not found: {binary}")

    try:
        result = subprocess.run(
            ["sparc-rtems6-objdump", "-d", str(binary)],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"objdump 실행 실패: {binary}") from e
