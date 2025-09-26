# disas_filter.py
import re

def filter_functions(objdump_output: str, func_names: list[str]) -> dict[str, str]:
    """
    objdump 출력에서 특정 함수들만 추출합니다.
    """
    func_pattern = re.compile(r"^[0-9a-fA-F]+ <(.+)>:$")
    filtered: dict[str, str] = {}

    current_func: str | None = None
    current_lines: list[str] = []

    for line in objdump_output.splitlines():
        if m := func_pattern.match(line):
            # 직전 함수 저장
            if current_func in func_names:
                filtered[current_func] = "\n".join(current_lines)
            current_func = m.group(1)
            current_lines = [line]
        elif current_func:
            current_lines.append(line)

    if current_func in func_names:
        filtered[current_func] = "\n".join(current_lines)

    return filtered
