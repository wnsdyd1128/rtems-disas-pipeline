# nm_parser.py
from pathlib import Path
import subprocess

def cfiles_to_objects(c_files: str, build_dir: str | Path) -> list[Path]:
    """
    C 파일 리스트를 대응하는 .o 파일 경로로 변환합니다.
    APP_C_FILES에 있는 경로는 소스 상대 경로이므로,
    build_dir과 합쳐서 object 파일 경로를 생성합니다.
    """
    build_dir = Path(build_dir)
    return [build_dir / (Path(cfile).with_suffix(".o").name) for cfile in c_files.split()]

def extract_defined_functions(obj_file: str | Path) -> list[str]:
    """
    nm 실행 결과에서 사용자 정의 함수 심볼만 추출
    """
    obj = Path(obj_file)
    if not obj.exists():
        raise FileNotFoundError(f"Object file not found: {obj}")

    try:
        result = subprocess.run(
            ["sparc-rtems6-nm", str(obj)],
            capture_output=True,
            text=True,
            check=True
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"nm 실행 실패: {obj}\nstdout:\n{e.stdout}\nstderr:\n{e.stderr}"
        ) from e

    funcs: list[str] = []
    for line in result.stdout.splitlines():
        parts = line.strip().split(maxsplit=2)
        if len(parts) == 3:
            _, sym_type, name = parts
            if sym_type in {"T", "t"}:
                funcs.append(name)
    return funcs
