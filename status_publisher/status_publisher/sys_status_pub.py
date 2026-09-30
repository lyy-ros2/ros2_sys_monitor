import rclpy
from rclpy.node import Node
from status_interfaces.msg import SystemStatus
import psutil
import platform

class SysStatusPub(Node):
    def __init__(self):
        super().__init__('sys_status_pub')
        self.publisher_ = self.create_publisher(SystemStatus, 'sys_status_topic', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        msg = SystemStatus()
        msg.stamp = self.get_clock().now().to_msg()
        msg.hostname = platform.node()
        msg.cpu_percent = psutil.cpu_percent()
        
        mem = psutil.virtual_memory()
        msg.memory_percent = mem.percent
        msg.memory_total = mem.total / (1024 * 1024)
        msg.memory_available = mem.available / (1024 * 1024)
        
        net_io = psutil.net_io_counters()
        msg.net_sent = net_io.bytes_sent / (1024 * 1024)
        msg.net_recv = net_io.bytes_recv / (1024 * 1024)
        
        self.publisher_.publish(msg)
        self.get_logger().info(f'发送: CPU {msg.cpu_percent}% | 内存 {msg.memory_percent}%')

def main(args=None):
    rclpy.init(args=args)
    node = SysStatusPub()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()
