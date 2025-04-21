# ch7_17_slave_robot_dance_moves_with_per_move_sync.py

from microbit import *
from microbit_abot import *
from abot_calibrated import *
import radio
import music

# 1. Radio 설정 (마스터와 동일한 그룹)
radio.on()
radio.config(group=1)

# 2. 로봇 초기화
abot = CalibratedMotionBot(13, 12)
abot.servo_attachpins()
abot.set_left_speed_offset(-5)
abot.set_calibrated_speed(65, -66, 2200)
abot.servo_speed_calibrated(0, 0)

# 3. 마스터와 동일한 dance_moves 정의
dance_moves = [
    {'action': 'forward',   'duration': 300},
    {'action': 'pause',     'duration': 200},
    {'action': 'rotate',    'angle': 90},
    {'action': 'pause',     'duration': 200},
    {'action': 'spin360'},
    {'action': 'pause',     'duration': 200},
    {'action': 'wiggle'},
    {'action': 'pause',     'duration': 200},
    {'action': 'zigzag',    'duration': 400},
    {'action': 'pause',     'duration': 200},
    {'action': 'flash'},
    {'action': 'melody'},
]

# 4. 개별 동작 처리 함수
def perform_move(move):
    action = move['action']

    if action == 'forward':
        abot.servo_speed_calibrated(50, -50)
        sleep(move['duration'])
        abot.servo_speed_calibrated(0, 0)

    elif action == 'pause':
        sleep(move['duration'])

    elif action == 'rotate':
        abot.rotate_degrees(move['angle'])

    elif action == 'spin360':
        abot.rotate_degrees(360)

    elif action == 'wiggle':
        for _ in range(3):
            abot.rotate_degrees(30)
            sleep(100)
            abot.rotate_degrees(-30)
            sleep(100)

    elif action == 'zigzag':
        abot.servo_speed_calibrated(40, -40)
        sleep(move['duration'])
        abot.rotate_degrees(45)
        abot.servo_speed_calibrated(40, -40)
        sleep(move['duration'])
        abot.rotate_degrees(-45)
        abot.servo_speed_calibrated(0, 0)

    elif action == 'flash':
        for img in (Image.HEART, Image.HAPPY, Image.SMILE):
            display.show(img)
            sleep(150)
        display.clear()

    elif action == 'melody':
        music.play(['c4:4', 'e4:4', 'g4:4'], wait=True)


# 5. 메인 루프: 마스터 명령 수신 → ACK 응답 → MOVE별 수행
while True:
    msg = radio.receive()
    if msg is None:
        sleep(10)
        continue

    # 5-1) 전체 시작 동기화
    if msg == 'start':
        radio.send('ACK')

    # 5-2) 즉시 정지
    elif msg == 'stop':
        abot.servo_speed_calibrated(0, 0)
        music.stop()

    # 5-3) 개별 동작 동기화
    elif msg.startswith('MOVE:'):
        # 1) ACK 보내고
        radio.send('ACK')
        # 2) 해당 동작 수행
        idx = int(msg.split(':')[1])
        perform_move(dance_moves[idx])

    sleep(10)
