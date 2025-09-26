# makevars.py
import subprocess
from pathlib import Path
from typing import Iterable

def get_make_vars(makefile_path: str | Path, keys: Iterable[str]) -> dict[str, str]:
    makefile = Path(makefile_path)
    result = subprocess.run(
        ["make", "-pn", "-f", str(makefile)],
        capture_output=True,
        text=True,
        check=False
    )

    # stdout에서 모든 변수 수집
    raw_vars: dict[str, str] = {}
    for line in result.stdout.splitlines():
        if " = " in line:
            try:
                key, val = line.split("=", 1)
                raw_vars[key.strip()] = val.strip()
            except ValueError:
                continue

    # --- 재귀 치환 함수 ---
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

    expanded = {k: expand(v) for k, v in raw_vars.items() if k in keys}
    return expanded
