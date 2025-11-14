import sys
from PyQt5.QtWidgets import *
import roslibpy
import pymysql

# ROSBridge 
ROS_HOST = '192.168.112.128' 
ROS_PORT = 9090

# ROSBridge 클라이언트 생성 및 연결
client = roslibpy.Ros(host=ROS_HOST, port=ROS_PORT)
client.run()
print("ROSBridge 서버에 연결됨")

# MySQL 서버
DB_CONFIG = dict(
        host = "localhost",
        user = "test",
        password = "1234",
        database = "ros_db",
        charset = "utf8"
)

class DB:
    def __init__(self, **config):
        self.config = config

    def connect(self):
        try:
            conn = pymysql.connect(**self.config)
            print("DB Connected")
            return conn
        except pymysql.MySQLError as e:
            print("DB Connect Failed")
            return None

# /turtle1/cmd_vel 퍼블리셔 생성
cmd_vel_pub = roslibpy.Topic(client, '/turtle1/cmd_vel', 'geometry_msgs/Twist')

# reset 서비스 클라이언트 생성
reset_srv = roslibpy.Service(client, '/reset', 'std_srvs/Empty')

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.current_pose = {'x': 0.0, 'y': 0.0, 'theta': 0.0}
        self.initUI()
        self.subscribe_pose()
        
    def initUI(self):
        btn1 = QPushButton('w - 전진', self)
        btn1.clicked.connect(self.move_forward)

        btn2 = QPushButton('s - 후진', self)
        btn2.clicked.connect(self.move_back)

        btn3 = QPushButton('a - 좌회전', self)
        btn3.clicked.connect(self.move_left)

        btn4 = QPushButton('d - 우회전', self)
        btn4.clicked.connect(self.move_right)

        btn5 = QPushButton('reset', self)
        btn5.clicked.connect(self.reset)
        
        btn6 = QPushButton('DB에 저장하기(x, y, theta)')
        btn6.clicked.connect(self.save_db)

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
        msg = {'linear': {'x': 2.0, 'y': 0.0, 'z': 0.0}, 'angular': {'x': 0.0, 'y': 0.0, 'z': 0.0}}
        cmd_vel_pub.publish(roslibpy.Message(msg))

    def move_back(self):
        msg = {'linear': {'x': -2.0, 'y': 0.0, 'z': 0.0}, 'angular': {'x': 0.0, 'y': 0.0, 'z': 0.0}}
        cmd_vel_pub.publish(roslibpy.Message(msg))

    def move_left(self):
        msg = {'linear': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'angular': {'x': 0.0, 'y': 0.0, 'z': 2.0}}
        cmd_vel_pub.publish(roslibpy.Message(msg))

    def move_right(self):
        msg = {'linear': {'x': 0.0, 'y': 0.0, 'z': 0.0}, 'angular': {'x': 0.0, 'y': 0.0, 'z': -2.0}}
        cmd_vel_pub.publish(roslibpy.Message(msg))

    def reset(self):
        req = roslibpy.ServiceRequest()
        reset_srv.call(req, lambda response: print('Turtle reset 완료'))
        
    def subscribe_pose(self):
        def callback(msg):
            self.current_pose['x'] = msg['x']
            self.current_pose['y'] = msg['y']
            self.current_pose['theta'] = msg['theta']
        pose_topic = roslibpy.Topic(client, '/turtle1/pose', 'turtlesim/Pose')
        pose_topic.subscribe(callback)
    
    def save_db(self):
        db = DB(**DB_CONFIG)
        conn = db.connect()
        cursor = conn.cursor()
        x = self.current_pose['x']
        y = self.current_pose['y']
        theta = self.current_pose['theta']
        cursor.execute("INSERT INTO turtle_pos (x, y, theta) VALUES (%s, %s, %s)", (x, y, theta))
        conn.commit()
        cursor.close()
        conn.close()

        print(f"저장 완료. x : {x}, y : {y}, theta : {theta}")

def main(args=None):
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())

    # 종료 시 ROSBridge 연결 종료
    cmd_vel_pub.unadvertise()
    client.terminate()


if __name__ == '__main__':
    main()