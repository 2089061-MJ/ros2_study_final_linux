import sys
from PyQt5.QtWidgets import *

import rclpy as rp
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_srvs.srv import Empty

import threading


class MyApp(QWidget):
    def __init__(self, node):
        super().__init__()
        self.node = node
        self.initUI()
    
    def initUI(self):
        btn1 = QPushButton(self)
        btn1.setText('w - 전진')
        btn1.clicked.connect(self.move_forward)

        btn2 = QPushButton(self)
        btn2.setText('s - 후진')
        btn2.clicked.connect(self.move_back)

        btn3 = QPushButton(self)
        btn3.setText('a - 좌회전')
        btn3.clicked.connect(self.move_left)

        btn4 = QPushButton(self)
        btn4.setText('d - 우회전')
        btn4.clicked.connect(self.move_right)

        btn5 = QPushButton(self)
        btn5.setText('reset')
        btn5.clicked.connect(self.reset)

        btn6 = QPushButton(self)
        btn6.setText('데이터베이스 저장(x, y, theta 값)')

        vbox = QVBoxLayout()
        vbox.addWidget(btn1)
        vbox.addWidget(btn2)
        vbox.addWidget(btn3)
        vbox.addWidget(btn4)
        vbox.addWidget(btn5)
        vbox.addWidget(btn6)

        self.setLayout(vbox)
        self.setWindowTitle('Turtle-Controller')
        self.setGeometry(300, 300, 300, 200)
        self.show()

    def move_forward(self):
        msg = Twist()
        msg.linear.x = 2.0
        self.node.publisher.publish(msg)

    def move_back(self):
        msg = Twist()
        msg.linear.x = -2.0
        self.node.publisher.publish(msg)

    def move_left(self):
        msg = Twist()
        msg.angular.z = 2.0
        self.node.publisher.publish(msg)

    def move_right(self):
        msg = Twist()
        msg.angular.z = -2.0
        self.node.publisher.publish(msg)

    def reset(self):
        self.node.reset_turtle()

class TurtlesimPublisher(Node):
    def __init__(self):
        super().__init__('turtlesim_publisher')
        self.publisher = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

    def reset_turtle(self):
        client = self.create_client(Empty, '/reset')
        while not client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Waiting for /reset service...')
        
        req = Empty.Request()
        future = client.call_async(req)
        return future
    
def main(args=None):
    rp.init(args=args)

    turtlesim_publisher = TurtlesimPublisher()

    ros_thread = threading.Thread(target=rp.spin, args=(turtlesim_publisher,), daemon=True)
    ros_thread.start()

    app = QApplication(sys.argv)
    ex = MyApp(node=turtlesim_publisher)
    app.exec_()

    turtlesim_publisher.destroy_node()
    rp.shutdown()


if __name__ == '__main__':
    main()