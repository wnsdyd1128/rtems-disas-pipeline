# main.py
import argparse
from pathlib import Path
from makevars import get_make_vars
from objdump_runner import run_objdump
from disas_filter import filter_functions
from nm_parser import cfiles_to_objects, extract_defined_functions
from utils import get_logger

logger = get_logger()

def main():
    parser = argparse.ArgumentParser(description="RTEMS Makefile 기반 함수 디스어셈블러")
    parser.add_argument("--makefile", required=True, help="Makefile 경로")
    parser.add_argument("--out", default="disasm_report.md", help="출력 파일 (기본: disasm_report.md)")
    args = parser.parse_args()

    makefile_path = Path(args.makefile).resolve()
    make_dir = makefile_path.parent   # Makefile 위치

    # 1. Makefile 변수 읽기
    makevars = get_make_vars(
        makefile_path, keys=("APP", "APP_C_FILES", "BUILDDIR", "EXEEXT")
    )

    # 2. 실행파일 경로 (EXEEXT 포함)
    app_binary = make_dir / makevars.get("APP", "")
    exe_ext = makevars.get("EXEEXT", "")
    if exe_ext and not str(app_binary).endswith(exe_ext):
        app_binary = Path(str(app_binary) + exe_ext)

    # 3. 빌드 디렉토리, 소스 파일
    build_dir = make_dir / makevars.get("BUILDDIR", ".")
    c_files = makevars.get("APP_C_FILES", "")

    logger.info(f"APP = {app_binary}")
    logger.info(f"BUILDDIR = {build_dir}")
    logger.info(f"APP_C_FILES = {c_files}")

    # 4. 오브젝트 파일 경로 생성
    object_files = cfiles_to_objects(c_files, build_dir)
    logger.debug(f"Object files: {object_files}")

    # 5. nm으로 함수 심볼 추출
    all_funcs: list[str] = []
    for obj in object_files:
        funcs = extract_defined_functions(obj)
        logger.debug(f"{obj} → {funcs}")
        all_funcs.extend(funcs)

    if not all_funcs:
        logger.warning("No functions extracted from object files.")
        return

    # 6. objdump 실행
    objdump_out = run_objdump(app_binary)

    # 7. 함수별 디스어셈블
    filtered = filter_functions(objdump_out, all_funcs)

    # 8. 터미널 출력 + 파일 저장
    out_path = Path('./logs') / Path(args.out)
    with out_path.open("w", encoding="utf-8") as f:
        f.write(f"# Disassembly Report\n\n")
        f.write(f"**Binary:** `{app_binary}`\n\n")
        f.write(f"**Functions Extracted:** {', '.join(all_funcs)}\n\n")

        for fname, disasm in filtered.items():
            section = f"\n## {fname}\n```\n{disasm}\n```\n"
            print(section)   # 터미널 출력
            f.write(section)

    logger.info(f"Disassembly exported to {out_path}")

if __name__ == "__main__":
    main()
