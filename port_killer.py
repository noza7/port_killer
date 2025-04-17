import sys
import os
import ctypes
import psutil
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QLineEdit, QPushButton, QTextEdit,
                            QLabel, QMessageBox, QCheckBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPalette, QColor

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def get_process_on_port(port):
    for proc in psutil.process_iter(['pid', 'name']):
        try:
            connections = proc.connections()
            for conn in connections:
                if hasattr(conn, 'laddr') and conn.laddr.port == port:
                    return proc
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            continue
    return None

class PortKiller(QMainWindow):
    def __init__(self):
        super().__init__()
        self.is_english = False
        self.setWindowTitle("Windows Port Process Killer")
        self.setMinimumSize(600, 400)
        
        # Set GitHub-like style
        self.setStyleSheet("""
            QMainWindow {
                background-color: #ffffff;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #d1d5da;
                border-radius: 6px;
                background-color: #ffffff;
                font-size: 14px;
            }
            QPushButton {
                padding: 8px 16px;
                background-color: #2ea44f;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2c974b;
            }
            QTextEdit {
                border: 1px solid #d1d5da;
                border-radius: 6px;
                background-color: #ffffff;
                font-size: 14px;
            }
            QLabel {
                font-size: 14px;
                color: #24292e;
            }
            QCheckBox {
                font-size: 14px;
                color: #24292e;
            }
        """)

        # Create central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        # Language switch
        lang_layout = QHBoxLayout()
        self.lang_switch = QCheckBox("English / 中文")
        self.lang_switch.stateChanged.connect(self.toggle_language)
        lang_layout.addWidget(self.lang_switch)
        lang_layout.addStretch()
        layout.addLayout(lang_layout)

        # Admin status label
        self.admin_label = QLabel()
        self.update_admin_label()
        layout.addWidget(self.admin_label)

        # Port input section
        input_layout = QHBoxLayout()
        self.port_label = QLabel("端口:")
        self.port_input = QLineEdit()
        self.port_input.setPlaceholderText("输入端口号 (1-65535)")
        input_layout.addWidget(self.port_label)
        input_layout.addWidget(self.port_input)
        layout.addLayout(input_layout)

        # Buttons layout
        buttons_layout = QHBoxLayout()
        self.search_button = QPushButton("查找进程")
        self.kill_button = QPushButton("结束进程")
        self.search_button.clicked.connect(self.search_process)
        self.kill_button.clicked.connect(self.kill_process)
        buttons_layout.addWidget(self.search_button)
        buttons_layout.addWidget(self.kill_button)
        layout.addLayout(buttons_layout)

        # Process list
        self.process_list = QTextEdit()
        self.process_list.setReadOnly(True)
        self.process_list.setPlaceholderText("进程信息将显示在这里...")
        layout.addWidget(self.process_list)

    def toggle_language(self, state):
        self.is_english = bool(state)
        self.update_texts()

    def update_texts(self):
        if self.is_english:
            self.setWindowTitle("Windows Port Process Killer")
            self.port_label.setText("Port:")
            self.port_input.setPlaceholderText("Enter port number (1-65535)")
            self.search_button.setText("Search")
            self.kill_button.setText("Kill Process")
            self.process_list.setPlaceholderText("Process information will appear here...")
            self.update_admin_label()
        else:
            self.setWindowTitle("Windows 端口进程管理器")
            self.port_label.setText("端口:")
            self.port_input.setPlaceholderText("输入端口号 (1-65535)")
            self.search_button.setText("查找进程")
            self.kill_button.setText("结束进程")
            self.process_list.setPlaceholderText("进程信息将显示在这里...")
            self.update_admin_label()

    def update_admin_label(self):
        if self.is_english:
            admin_status = "Running with admin privileges" if is_admin() else "Running without admin privileges (some processes may not be accessible)"
        else:
            admin_status = "正在以管理员权限运行" if is_admin() else "未以管理员权限运行（部分进程可能无法访问）"
        
        self.admin_label.setText(admin_status)
        self.admin_label.setStyleSheet("color: #d73a49;" if not is_admin() else "color: #2ea44f;")

    def validate_port(self, port_str):
        try:
            port = int(port_str)
            if not 1 <= port <= 65535:
                return False, "端口号必须在1-65535之间" if not self.is_english else "Port number must be between 1 and 65535"
            return True, port
        except ValueError:
            return False, "请输入有效的端口号" if not self.is_english else "Please enter a valid port number"

    def search_process(self):
        port_str = self.port_input.text().strip()
        if not port_str:
            msg = "请输入端口号" if not self.is_english else "Please enter a port number"
            QMessageBox.warning(self, "Error", msg)
            return

        is_valid, result = self.validate_port(port_str)
        if not is_valid:
            QMessageBox.warning(self, "Error", result)
            return

        port = result
        self.process_list.clear()
        
        try:
            proc = get_process_on_port(port)
            if proc:
                proc_name = proc.name()
                proc_pid = proc.pid
                if self.is_english:
                    self.process_list.append(f"Found process: {proc_name} (PID: {proc_pid}) on port {port}")
                else:
                    self.process_list.append(f"找到进程: {proc_name} (PID: {proc_pid}) 占用端口 {port}")
            else:
                msg = f"No process found using port {port}" if self.is_english else f"未找到占用端口 {port} 的进程"
                QMessageBox.information(self, "Info", msg)
            
        except Exception as e:
            error_msg = f"Error searching process: {str(e)}" if self.is_english else f"搜索进程时出错: {str(e)}"
            QMessageBox.critical(self, "Error", error_msg)

    def kill_process(self):
        port_str = self.port_input.text().strip()
        if not port_str:
            msg = "请输入端口号" if not self.is_english else "Please enter a port number"
            QMessageBox.warning(self, "Error", msg)
            return

        is_valid, result = self.validate_port(port_str)
        if not is_valid:
            QMessageBox.warning(self, "Error", result)
            return

        port = result
        self.process_list.clear()
        
        try:
            proc = get_process_on_port(port)
            if proc:
                try:
                    proc_name = proc.name()
                    proc_pid = proc.pid
                    proc.kill()
                    if self.is_english:
                        self.process_list.append(f"✓ Killed process: {proc_name} (PID: {proc_pid}) on port {port}")
                    else:
                        self.process_list.append(f"✓ 已结束进程: {proc_name} (PID: {proc_pid}) 占用端口 {port}")
                except psutil.AccessDenied:
                    if self.is_english:
                        self.process_list.append(f"⚠ Could not kill process: {proc_name} (PID: {proc_pid}) - Access denied")
                    else:
                        self.process_list.append(f"⚠ 无法结束进程: {proc_name} (PID: {proc_pid}) - 访问被拒绝")
                    if not is_admin():
                        if self.is_english:
                            msg = "Process could not be killed due to insufficient permissions.\nTry running the program as administrator."
                        else:
                            msg = "由于权限不足，进程无法被结束。\n请尝试以管理员身份运行程序。"
                        QMessageBox.warning(self, "Warning", msg)
            else:
                msg = f"No process found using port {port}" if self.is_english else f"未找到占用端口 {port} 的进程"
                QMessageBox.information(self, "Info", msg)
            
            self.port_input.clear()
            
        except Exception as e:
            error_msg = f"Error killing process: {str(e)}" if self.is_english else f"结束进程时出错: {str(e)}"
            QMessageBox.critical(self, "Error", error_msg)

def main():
    app = QApplication(sys.argv)
    window = PortKiller()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main() 