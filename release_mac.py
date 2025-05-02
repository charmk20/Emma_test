import subprocess
import locale
import shutil
from pathlib import Path

def run_shell_command(command):
    try:
        result = subprocess.run(
            command,
            text=True,
            shell=True,
            encoding=locale.getpreferredencoding(),
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
    release_command = 'pyinstaller --clean -F --console --add-data "emmc_test.ui:." emmc_test.py'
    build_output = run_shell_command(release_command)
    if build_output is None:
        print("[FATAL] 빌드 실패. 종료합니다.")
        return
    
    # fallback copy 방식
    safe_copy("emmc_test.ui", "dist")
    safe_copy("pop_window.ui", "dist")
    
    shutil.make_archive("emmc_test_package", 'zip', 'dist')

if __name__ == "__main__":
    print("====> Start installing exe package <====")
    install_exe_package()
