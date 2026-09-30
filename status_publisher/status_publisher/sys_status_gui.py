import sys
import rclpy
from rclpy.node import Node
from status_interfaces.msg import SystemStatus
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt

class StatusSubscriber(Node):
    def __init__(self):
        super().__init__('sys_status_gui')
        self.subscription = self.create_subscription(SystemStatus, 'sys_status_topic', self.listener_callback, 10)
        self.latest_msg = None

    def listener_callback(self, msg):
        self.latest_msg = msg

class MainWindow(QMainWindow):
    def __init__(self, node):
        super().__init__()
        self.node = node
        self.setWindowTitle("系统状态监控 (ROS2)")
        self.resize(400, 300)
        self.label = QLabel("等待数据...", self)
        self.label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(self.label)
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_ui)
        self.timer.start(1000)

    def update_ui(self):
        if self.node.latest_msg:
            msg = self.node.latest_msg
            text = (f"主机名: {msg.hostname}\n\nCPU: {msg.cpu_percent}%\n\n"
                    f"内存使用率: {msg.memory_percent}%\n总内存: {msg.memory_total:.2f} MB\n"
                    f"剩余内存: {msg.memory_available:.2f} MB\n\n"
                    f"网络发送: {msg.net_sent:.2f} MB\n网络接收: {msg.net_recv:.2f} MB")
            self.label.setText(text)

def main(args=None):
    rclpy.init(args=args)
    node = StatusSubscriber()
    app = QApplication(sys.argv)
    window = MainWindow(node)
    window.show()
    
    timer = QTimer()
    timer.timeout.connect(lambda: rclpy.spin_once(node, timeout_sec=0))
    timer.start(50)
    sys.exit(app.exec_())
