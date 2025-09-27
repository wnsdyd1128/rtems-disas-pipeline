# nm_parser.py
import subprocess
from pathlib import Path
from loguru import logger

def extract_defined_functions(obj: Path) -> list[str]:
    """
    nm으로부터 정의된 함수(T symbol) 이름만 추출.
    """
    if not obj.exists():
        raise FileNotFoundError(f"Object file not found: {obj}")

    try:
        result = subprocess.run(
            ["sparc-rtems6-nm", str(obj)],
            capture_output=True,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"nm 실행 실패: {obj}") from e

    funcs = []
    for line in result.stdout.splitlines():
        parts = line.split()
        if len(parts) == 3 and parts[1].lower() == "t":  # T = text section
            funcs.append(parts[2])
    return funcs


def cfiles_to_objects(c_files: str, build_dir: Path) -> list[Path]:
    """
    C 파일명 → 대응하는 오브젝트 파일 경로 변환
    """
    if not c_files:
        return []
    return [
        build_dir / (Path(c).with_suffix(".o").name)
        for c in c_files.split()
    ]
