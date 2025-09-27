# makevars.py
import subprocess
from pathlib import Path
from typing import Iterable

def get_make_vars(makefile_path: str | Path, keys: Iterable[str]) -> dict[str, str]:
    """
    GNU Make로부터 변수 목록을 가져오고,
    include 파일을 재귀적으로 파싱하여 전체 확장된 값을 반환합니다.
    """
    makefile_path = Path(makefile_path).resolve()
    all_files = resolve_includes(makefile_path)

    cmd = ["make", "-pn"]
    for f in all_files:
        cmd.extend(["-f", str(f)])

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=False,
    )

    # 1️⃣ 전체 변수 파싱
    raw_vars: dict[str, str] = {}
    for line in result.stdout.splitlines():
        if " = " in line:
            try:
                key, val = line.split("=", 1)
                raw_vars[key.strip()] = val.strip()
            except ValueError:
                continue

    # 2️⃣ 재귀 치환
    def expand(val: str) -> str:
        changed = True
        while changed:
            changed = False
            for k, v in raw_vars.items():
                token = f"$({k})"
                if token in val:
                    val = val.replace(token, v)
                    changed = True
        return val

    # 3️⃣ 요청된 키만 반환
    expanded = {k: expand(v) for k, v in raw_vars.items() if k in keys}
    return expanded


def resolve_includes(makefile: Path) -> list[Path]:
    """
    include 지시어를 재귀적으로 추적하여 전체 Makefile 경로 리스트 반환.
    """
    visited: set[Path] = set()
    resolved: list[Path] = []

    def _parse(file: Path):
        if not file.exists() or file in visited:
            return
        visited.add(file)
        resolved.append(file)

        for line in file.read_text().splitlines():
            line = line.strip()
            if line.startswith("include "):
                inc_path = line.split("include", 1)[1].strip()
                inc_file = (file.parent / inc_path).resolve()
                _parse(inc_file)

    _parse(makefile)
    return resolved
