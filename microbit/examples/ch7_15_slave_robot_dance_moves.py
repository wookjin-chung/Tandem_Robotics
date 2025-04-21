# ch7_15_slave_robot_dance_moves.py

from microbit import *
from microbit_abot import *
from abot_calibrated import *
import radio
import music

# 1. Radio 설정 (마스터와 같은 그룹)
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

# 4. Dance 함수 (중간에 stop 감지)
def dance():
    music.play(music.DADADADUM, wait=False)
    for move in dance_moves:
        # 수행 도중 stop 메시지 수신 체크
        msg = radio.receive()
        if msg == 'stop':
            break

        action = move['action']
        # print는 디버깅용입니다
        print("Slave action:", action)

        if action == 'forward':
            abot.servo_speed_calibrated(50, -50)
            sleep(move['duration'])
            abot.servo_speed_calibrated(0, 0)

        elif action == 'backward':
            abot.servo_speed_calibrated(-50, 50)
            sleep(move['duration'])
            abot.servo_speed_calibrated(0, 0)

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

        elif action == 'pause':
            sleep(move['duration'])

        # 반복 중에도 stop 수신 체크
        msg = radio.receive()
        if msg == 'stop':
            break

    music.stop()
    # 혹시 남아 있을 모터 출력을 확실히 0으로
    abot.servo_speed_calibrated(0, 0)

# 5. 메인 루프: start/stop 신호 수신 처리
def main():
    """
    Main loop that listens for radio messages to start or stop dancing.
    """
    display.scroll("Ready")  # Indicate readiness
    
    while True:
        msg = radio.receive()
        if msg == 'start':
        # 준비 완료 ACK
            radio.send('ACK')
            dance()
        elif msg == 'stop':
            abot.servo_speed_calibrated(0, 0)
        sleep(50)

if __name__ == "__main__":
    main()
