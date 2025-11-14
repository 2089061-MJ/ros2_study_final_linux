# ROS2 실습 과제 
Python, PyQt, MySQL을 이용해서 turtle의 cmd_vel(방향), Pose(좌표), reset(turtle 초기화) 기능을 앱으로 제어하는 기능을 구현하고 현재 turtle의 Pose 값(x, y, theta)을 DB에 저장하는 기능도 구현하였습니다.

## 요구 사항
1. ROSBridge가 제공하는 웹 소켓 서버를 활성화 해야합니다.(리눅스 환경)
2. 리눅스 서버에서 turtlesim_node를 활성화 해놓은 상태여야 합니다.
3. MySQL 데이터베이스 스키마, 테이블 생성 필수

## 적용하기
리눅스 우분투 22.04 환경 기준으로 작성하였습니다.

### 필요한 패키지를 설치합니다.
    $ sudo apt install ros-humble-rosbridge-server
    $ pip3 install pymysql
    $ pip3 install PyQt5
    $ pip3 install PyQt5-tools
    $ pip3 install roslibpy
### turtlesim을 실행합니다.
    $ source /opt/ros/humble/setup.bash
    $ ros2 run turtlesim turtlesim_node
  
### 9090번 포트로 ROSBridge 서버를 실행합니다.
    $ ros2 run rosbridge_server rosbridge_websocket -port 9090

### clone 한 파일 빌드하고 실행하기
    $ colcon build
    $ source ./install/local_setup.bash
    $ ros2 run test_package controller_node

## 실행
<img width="293" height="268" alt="스크린샷 2025-11-14 102640" src="https://github.com/user-attachments/assets/077cd7a2-bc6f-4325-9baa-0c4197a97d37" />

[![Video Label](http://img.youtube.com/vi/-K5hbV-BERc/0.jpg)](https://www.youtube.com/watch?v=-K5hbV-BERc)




