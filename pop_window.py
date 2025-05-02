import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QDialog, QMessageBox, QLabel, QVBoxLayout, QPushButton
from PyQt6 import QtCore, QtGui, QtWidgets, uic

## def display_critical_popup(message):
##     msg = QMessageBox()
##     msg.setWindowTitle("Warnning")
##     msg.setText(message)
##     msg.setIcon(QMessageBox.Icon.Critical)
##     msg.setStyleSheet("""
##     QMessageBox 
##     {
##         background-color: #fff;
##         color: #000;
##         font-family: "Malgun Gothic";
##         font-size: 10pt;
##         font-style: normal;
##         font-weight: 700;
##         line-height: normal;
##     }
##                       
##     QPushButton:Pressed
##     {
##         color: #004FD7;
##         font-family: "Malgun Gothic";
##         font-size: 10pt;
##         font-style: normal;
##         font-weight: 700;
##         border-radius: 6px;
##         background: #004FD7;
##         border: 1px solid #C3C3C3;
##     }
## 
##     QPushButton
##     {
##         color: #FFFFFF;
##         font-family: "Malgun Gothic";
##         font-size: 10pt;
##         font-style: normal;
##         font-weight: 700;
##         border-radius: 6px;
##         border-radius: 6px;
##         background: #004FD7;
##         border: 1px solid #C3C3C3;
##     }
## """)
##     layout = msg.layout()
##     layout.setContentsMargins(20, 20, 20, 20)
##     layout.setSpacing(10)
## 
##     # Resize the QMessageBox
##     msg.setMinimumSize(400, 300)
##     msg.setMaximumSize(400, 300)
##     x = msg.exec()
## 
## def display_information_popup(message):
##     msg = QMessageBox()
##     msg.setWindowTitle("Information")
##     msg.setText(message)
##     msg.setIcon(QMessageBox.Icon.Information)
##     msg.setMinimumSize(400, 300)
##     msg.setMaximumSize(400, 300)
##     msg.setStyleSheet("""
##     QMessageBox 
##     {
##         background-color: #fff;
##         color: #000;
##         font-family: "Malgun Gothic";
##         font-size: 10pt;
##         font-style: normal;
##         font-weight: 700;
##         line-height: normal;
##     }
##                       
##     QPushButton:Pressed
##     {
##         color: #004FD7;
##         font-family: "Malgun Gothic";
##         font-size: 10pt;
##         font-style: normal;
##         font-weight: 700;
##         border-radius: 6px;
##         background: #004FD7;
##         border: 1px solid #C3C3C3;
##     }
## 
##     QPushButton
##     {
##         color: #FFFFFF;
##         font-family: "Malgun Gothic";
##         font-size: 10pt;
##         font-style: normal;
##         font-weight: 700;
##         border-radius: 6px;
##         background: #004FD7;
##         border: 1px solid #C3C3C3;
##     }
## """)
##     layout = msg.layout()
##     layout.setContentsMargins(20, 20, 20, 20)
##     layout.setSpacing(10)
## 
##     # Resize the QMessageBox
##     msg.setMinimumSize(400, 300)
##     msg.setMaximumSize(400, 300)
##     x = msg.exec()

class CustomMessageBox(QDialog):
    def __init__(self, title, message, login):
        super().__init__()

        uic.loadUi("pop_window.ui", self)

        self.setWindowTitle(title)
        self.setFixedSize(576, 258)  # 크기 고정
        self.pushButton_ok.clicked.connect(self.accept)
        self.label_message.setText(message)

        ## connect event
        self.pushButton_ok.clicked.connect(self.accept)
        self.pushButton_cancle.clicked.connect(self.reject)

        if login == False:
            self.pushButton_cancle.hide()


    def self_exit(self):
        QApplication.quit()

    def do_push_button(self):
        self.self_exit()
        
def display_information_popup(message): 
 ##   app = QApplication(sys.argv)
    custom_msg = CustomMessageBox("Information", message, False) 
    custom_msg.exec()
 ##   sys.exit(app.exec())

def display_critical_popup(message): 
 ##    app = QApplication(sys.argv)
    custom_msg = CustomMessageBox("Warning", message, False) 
    custom_msg.exec()
 ##   sys.exit(app.exec())

def display_logout_message():
 ##   app = QApplication(sys.argv)
    custom_msg = CustomMessageBox("Information", "로그 아웃 할까요 ?", True) 
    ret = custom_msg.exec()
    if ret == QDialog.DialogCode.Accepted:
        return True
    else :
        return False
 
 ##   sys.exit(app.exec())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    display_information_popup("펌웨어 다운로드 중")

    custom_msg = CustomMessageBox("Custom Dialog", "This is a custom dialog with fixed size.")
    custom_msg.exec()

    sys.exit(app.exec())