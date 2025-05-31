import subprocess
import time
from  pathlib import Path
import sys, os
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QFile, QIODevice, Qt, QSize, pyqtSignal
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QDialog, QListWidget
from ppadb.client import Client as AdbClient
import ipaddress, threading
import pop_window
import winreg

# 설정 부분
TARGET_PARTITION = "/dev/block/factory"  # 타겟 파티션
PARTITION_SIZE = 1024 * 4096  # 1MB 예시 (필요시 수정)
BLOCK_SIZE = 4096  # KB
PATTERN_BYTE = b'\xAA'  # 반복해서 쓸 데이터 패턴
ADB_PATH = "adb"  # adb 경로

class MainWindow(QMainWindow):

    # 시스널 정의 
    noti_signal = pyqtSignal(str, str) 

    def __init__(self):
        super(MainWindow, self).__init__()
        current_directory = os.getcwd()
        ui_path = os.path.join(os.path.dirname(__file__), "emmc_test.ui")
        
        try:
            uic.loadUi(ui_path,self)
        except:
            print(f'load emmc_test.ui ========> {current_directory}')

        self.noti_signal.connect(self.noti_signal_handler)

        self.setFixedSize(720, 576)  # 크기 고정

        self.adb_client = AdbClient(host="127.0.0.1", port=5037)
        self.device1 = None
        self.device2 = None
        self.device3 = None

        self.thread_dev1 = None
        self.thread_dev2 = None
        self.thread_dev3 = None

        self.thread_dev1_stop = False
        self.thread_dev2_stop = False
        self.thread_dev3_stop = False

        self.setEventHandler()

    # 시그널 핸들러 정의
    def noti_signal_handler(self, dev, message):
        if dev == "dev1":        
            self.textEdit_dev1_status.setText(message)
        elif dev == "dev2": 
            self.textEdit_dev2_status.setText(message)
        elif dev == "dev3" :
            self.textEdit_dev3_status.setText(message)
        else :     
            print ("Invalid noti Signal")

    def setEventHandler(self): 
        print("Start connect eventhandler")
        self.pushButton_dev1_connect.clicked.connect(self.pushButton_dev1_connect_clicked)
        self.pushButton_dev2_connect.clicked.connect(self.pushButton_dev2_connect_clicked)
        self.pushButton_dev3_connect.clicked.connect(self.pushButton_dev3_connect_clicked)

        self.pushButton_dev1_disconnect.clicked.connect(self.pushButton_dev1_disconnect_clicked)
        self.pushButton_dev2_disconnect.clicked.connect(self.pushButton_dev2_disconnect_clicked)
        self.pushButton_dev3_disconnect.clicked.connect(self.pushButton_dev3_disconnect_clicked)

        self.pushButton_start_1.clicked.connect(self.pushButton_start_1_connect_clicked)
        self.pushButton_start_2.clicked.connect(self.pushButton_start_2_connect_clicked)
        self.pushButton_start_3.clicked.connect(self.pushButton_start_3_connect_clicked)
        
    def pushButton_start_1_connect_clicked(self):
        if self.device1 != None:    
            if getattr(self, "thread_dev1", None) and self.thread_dev1.is_alive():
                self.thread_dev1_stop = True    
                self.thread_dev1.join()
                self.pushButton_start_1.setText("테스트시작")
            else:
                self.thread_dev1_stop = False
                self.thread_dev1 = threading.Thread(target=self.endurance_test, args=("dev1",))
                self.thread_dev1.start()
                self.pushButton_start_1.setText("테스트중지")
        else:
            pop_window.display_critical_popup("디바이스가 연결되지 않았습니다. 디바이스를 연결해 주세요")


    def pushButton_start_2_connect_clicked(self):
        if self.device2 != None:
            if getattr(self, "thread_dev2", None) and self.thread_dev2.is_alive():
                self.thread_dev2_stop = True 
                self.thread_dev2.join()
                self.pushButton_start_2.setText("테스트시작")
            else:
                self.thread_dev2_stop = False
                self.thread_dev2 = threading.Thread(target=self.endurance_test, args=("dev2",))
                self.thread_dev2.start()
                self.pushButton_start_2.setText("테스트중지")
        else:
            pop_window.display_critical_popup("디바이스가 연결되지 않았습니다. 디바이스를 연결해 주세요")

    def pushButton_start_3_connect_clicked(self):
        if self.device3 != None:
            if getattr(self, "thread_dev3", None) and self.thread_dev3.is_alive():
                self.thread_dev3_stop = True
                self.thread_dev3.join()
                self.pushButton_start_3.setText("테스트시작")
            else:
                self.thread_dev3_stop = False 
                self.thread_dev3 = threading.Thread(target=self.endurance_test, args=("dev3",))
                self.thread_dev3.start()
                self.pushButton_start_3.setText("테스트중지")
        else:
            pop_window.display_critical_popup("디바이스가 연결되지 않았습니다. 디바이스를 연결해 주세요")

    def pushButton_dev1_connect_clicked(self):
        self.device1 = self.adb_connect_dev(1)
        
    def pushButton_dev2_connect_clicked(self):
        self.device2 = self.adb_connect_dev(2)
        
    def pushButton_dev3_connect_clicked(self):
        self.device3 = self.adb_connect_dev(3)

    def pushButton_dev1_disconnect_clicked(self):
        if getattr(self, "thread_dev1", None) and self.thread_dev1.is_alive():
            pop_window.display_critical_popup("테스트가 진행 중입니다.\n먼저 테스트를 중지해 주세요")
            return

        if self.device1 != None:
            self.adb_disconnect_dev(1)


    def pushButton_dev2_disconnect_clicked(self):
        if getattr(self, "thread_dev2", None) and self.thread_dev2.is_alive():
            pop_window.display_critical_popup("테스트가 진행 중입니다.\n먼저 테스트를 중지해 주세요")
            return

        if self.device2 != None:
            self.adb_disconnect_dev(2)


    def pushButton_dev3_disconnect_clicked(self):
        if getattr(self, "thread_dev3", None) and self.thread_dev3.is_alive():
            pop_window.display_critical_popup("테스트가 진행 중입니다.\n먼저 테스트를 중지해 주세요")
            return

        if self.device3 != None:
            self.adb_disconnect_dev(3)


    def adb_disconnect_dev(self, dev_index):
        if dev_index   == 1:
            ip_addr = self.lineEdit_dev1_ip.text()
            device = self.device1
        elif dev_index == 2:
            ip_addr = self.lineEdit_dev2_ip.text()
            device = self.device2
        elif dev_index == 3:
            ip_addr = self.lineEdit_dev3_ip.text() 
            device = self.device3
        else:    
            print("inalid device id")
            return None

        if self.is_valid_ip(ip_addr) == False:
            print("inalid ip addr id")
            pop_window.display_critical_popup("잘못된 IP 어드레스 입니다.\n아이피를 확인해 주세요")
            return None
        
        client = self.adb_client 
        port = 5555
        result = client.remote_disconnect(ip_addr, port)
        print(f"[INFO] ADB disconnect result: {result}")

        if dev_index == 1:
            self.device1 = None
            self.textEdit_dev1_status.setText("OK ! - device disconnected")
        elif dev_index == 2:
            self.device2 = None
            self.textEdit_dev2_status.setText("OK ! - device disconnected")
        elif dev_index == 3:
            self.device3 = None
            self.textEdit_dev3_status.setText("OK ! - device disconnected")
        
    def adb_connect_dev(self, dev_index):
        if dev_index   == 1:
            ip_addr = self.lineEdit_dev1_ip.text()
        elif dev_index == 2:
            ip_addr = self.lineEdit_dev2_ip.text()
        elif dev_index == 3:
            ip_addr = self.lineEdit_dev3_ip.text() 
        else:    
            print("inalid device id")
            return None

        if self.is_valid_ip(ip_addr) == False:
            print("inalid ip addr id")
            pop_window.display_critical_popup("잘못된 IP 어드레스 입니다.\n아이피를 확인해 주세요")
            return None

        client = self.adb_client 
        port = 5555

        result = client.remote_connect(ip_addr, port)
        print(type(result), result)  # 디버깅용

        if result == False:
            pop_window.display_information_popup("디바이스 연결에 실패 했습니다 !!")
            return None

        device = client.device(f"{ip_addr}:{port}")
        if device : 
            pop_window.display_information_popup("디바이스가 정상적으로 연결되었습니다 !!")
            if dev_index   == 1:
                self.textEdit_dev1_status.setText("OK ! - device connected ")
            elif dev_index == 2:
                self.textEdit_dev2_status.setText("OK ! - device connected ")
            elif dev_index == 3:
                self.textEdit_dev3_status.setText("OK ! - device connected ")
            
            return device
        else :
            pop_window.display_information_popup("디바이스 연결에 실패 했습니다 !!")
            return None

    def is_valid_ip(sel, ip_str: str) -> bool:
        try:
            ipaddress.ip_address(ip_str)
            return True
        except ValueError:
            return False
    # adb root 명령 실행
    def adb_root(self):
        full_cmd = [ADB_PATH, "root"]
        result = subprocess.run(full_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode, result.stdout.decode(), result.stderr.decode()
    
    #adb kill-server 명령실행
    def adb_kill_server(self):
        full_cmd = [ADB_PATH, "kill-server"]
        result = subprocess.run(full_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode, result.stdout.decode(), result.stderr.decode()

    # adb shell 명령 실행
    def adb_shell(self, dev_ip, cmd):
        full_cmd = [ADB_PATH, "-s", dev_ip, "shell"] + cmd
        result = subprocess.run(full_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode, result.stdout.decode(), result.stderr.decode()

    # adb push 파일
    def adb_push(self, dev_ip, local_file, remote_file):
        full_cmd = [ADB_PATH, "-s", dev_ip, "push", local_file, remote_file]
        result = subprocess.run(full_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.returncode == 0

    # 패턴 파일 생성
    def create_pattern_file(self, filename, size_bytes, pattern_byte):
        with open(filename, "wb") as f:
            f.write(pattern_byte * size_bytes)

    # 메인 테스트 함수
    def endurance_test(self, dev):
        if dev == "dev1":
            dev_ip = self.lineEdit_dev1_ip.text()
        elif dev == "dev2":
            dev_ip = self.lineEdit_dev2_ip.text()
        elif dev == "dev3":
            dev_ip = self.lineEdit_dev3_ip.text()
        else :
            self.noti_signal.emit(dev, "테스트를 진행을 할수 없습니다. 디바이스 연결 상태를 확인해 주세요")
            return 

        temp_file = f"pattern_{dev}.bin"
        remote_temp = f"/data/pattern_{dev}.bin"

        temp_file_path = Path(temp_file)

        # Step 1: 테스트용 패턴 파일 만들기
        if temp_file_path.is_file():
            temp_file_path.unlink()
            print(f"{temp_file_path} 삭제됨.")

        self.create_pattern_file(temp_file, PARTITION_SIZE, PATTERN_BYTE)
        print(f"[INFO] Pattern file '{temp_file}' created.")

        # Step 2: 디바이스로 push
        if not self.adb_push(dev_ip, temp_file, remote_temp):
            print("[ERROR] Failed to push pattern file to device.")
            return

        iteration = 0

        dev_stop = False
        while (dev_stop == False):            
            if dev == "dev1":
                dev_stop = self.thread_dev1_stop
            elif dev == "dev2":
                dev_stop = self.thread_dev2_stop
            elif dev == "dev3":
                dev_stop = self.thread_dev3_stop

            if dev_stop == True:
                print(f"test stopped = {dev}")
                break 

            try:
                print(f"[INFO] Iteration {iteration + 1} 시작")
                self.noti_signal.emit(dev, f"[INFO] Iteration {iteration + 1} 시작")
                # 1. Write
                cmd = ["dd", f"if={remote_temp}", f"of={TARGET_PARTITION}", "bs=4096", "count=1024", "conv=notrunc"]
                print(f"cmd = {cmd}")
                ret, out, err = self.adb_shell(dev_ip, cmd)
                if ret != 0:
                    raise Exception(f"Write 실패: {err}")

                # 2. Verify (read to file)
                remote_read_file = f"/data/readback_{dev}.bin"
                cmd = ["dd", f"if={TARGET_PARTITION}", f"of={remote_read_file}", "bs=4096", "count=1024"]
                print(f"cmd = {cmd}")

                ret, out, err = self.adb_shell(dev_ip, cmd)
                if ret != 0:
                    raise Exception(f"Read 실패: {err}")

                # Pull the readback file
                local_read_file = f"readback_{dev}.bin"
                subprocess.run([ADB_PATH, "-s", dev_ip, "pull", remote_read_file, local_read_file], stdout=subprocess.DEVNULL)

                with open(local_read_file, "rb") as f:
                    data = f.read()
                    if data != PATTERN_BYTE * PARTITION_SIZE:
                        raise Exception("Verification mismatch")

                iteration += 1
                print(f"[INFO] Iteration {iteration} 완료")

            except Exception as e:
                self.noti_signal.emit(dev, f"[ERROR] 에러 발생 at iteration {iteration}: {e}")
                print(f"[ERROR] 에러 발생 at iteration {iteration}: {e}")
                break

        self.noti_signal.emit(dev, f"[RESULT] 최종 반복 횟수: {iteration}")

def add_current_directory_to_path():
    current_dir = os.path.join(os.getcwd(), "android")
    current_path = os.environ.get("PATH", "")

    if current_dir not in current_path.split(";"):
        os.environ["PATH"] += ";" + current_dir
        print(f"[OK] PATH에 추가됨: {current_dir}")
    else:
        print(f"[SKIP] 이미 PATH에 존재함: {current_dir}")

if __name__ == "__main__":\
    ## Display ui 
    app = QApplication(sys.argv)

    add_current_directory_to_path()

    MW = MainWindow()
    MW.show()
    ret = MW.adb_kill_server()
    print (f"=====> {ret}")
    ret = MW.adb_root()
    print (f"=====> {ret}")
    sys.exit(app.exec())

    ## endurance_test()