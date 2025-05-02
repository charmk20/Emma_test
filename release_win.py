import subprocess
import locale
import shutil
from pathlib import Path
from datetime import datetime
import sys
import os

def run_shell_command(command):
    try:
        result = subprocess.run(
            command,
            text=True,
            shell=True,
            encoding=locale.getpreferredencoding(False),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print(result.stdout)
        if result.returncode != 0:
            print(f"[ERROR] {result.stderr}")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Failed to run command '{command}' : {e}")
        return None

def safe_copy(src, dst_folder):
    src_path = Path(src)
    dst_path = Path(dst_folder) / src_path.name
    if src_path.exists():
        shutil.copy(src_path, dst_path)
        print(f"[OK] {src_path} -> {dst_path}")
    else:
        print(f"[WARN] 파일 없음: {src_path}")

def install_exe_package():
    print("====> Windows용 EXE 패키지 빌드 시작 <====")

    # Windows에서는 --add-data 구분자를 ; 로 변경
    if sys.platform.startswith("win"):
        add_data_option = '--add-data "emmc_test.ui;."'
    else:
        add_data_option = '--add-data "emmc_test.ui:."'

    release_command = f'pyinstaller --clean -F --console {add_data_option} emmc_test.py'
    build_output = run_shell_command(release_command)

    if build_output is None:
        print("[FATAL] 빌드 실패. 종료합니다.")
        return

    # UI 파일 백업 복사 (필요할 경우)
    safe_copy("emmc_test.ui", "dist")
    safe_copy("pop_window.ui", "dist")

    # 결과 zip 압축 파일 생성
    zip_name = f"emmc_test_package_{datetime.now():%Y%m%d_%H%M%S}"
    archive_path = shutil.make_archive(zip_name, 'zip', 'dist')
    print(f"[OK] 압축 파일 생성됨: {archive_path}")

if __name__ == "__main__":
    install_exe_package()