# ch7_16_master_robot_dance_moves_with_per_move_sync.py

from microbit import *
from microbit_abot import *
from abot_calibrated import *
import radio
import music

# 1. 설정: 슬레이브 대수
TOTAL_SLAVES = 2   # ← 실제 연결된 슬레이브 로봇 수로 맞춰주세요

# 2. Radio 설정
radio.on()
radio.config(group=1)

# 3. 로봇 초기화
abot = CalibratedMotionBot(13, 12)
abot.servo_attachpins()
abot.set_left_speed_offset(-5)
abot.set_calibrated_speed(65, -66, 2200)
abot.servo_speed_calibrated(0, 0)

dancing = False
prev_logo_state = False

# 4. 동작 시퀀스 정의 (마스터·슬레이브 공통)
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

# 5. ACK 동기화 함수
def wait_for_all_acks(timeout_ms=2000):
    """timeout_ms 내에 TOTAL_SLAVES 만큼 'ACK' 수신을 대기"""
    start = running_time()
    ack_count = 0
    while running_time() - start < timeout_ms and ack_count < TOTAL_SLAVES:
        msg = radio.receive() 
        if msg == 'ACK':
            ack_count += 1
    return ack_count >= TOTAL_SLAVES

# 6. 동기화된 dance() 함수
def dance():
    global dancing

    # 배경음악 비동기 재생
    music.play(music.DADADADUM, wait=False)

    for idx, move in enumerate(dance_moves):
        if not dancing:
            break

        # 6-1) 마스터에서 각 move 브로드캐스트
        radio.send('MOVE:{}'.format(idx))
        display.show(Image.SQUARE)            # 동기화 대기 표시
        if not wait_for_all_acks():
            # 타임아웃 또는 일부 슬레이브 응답 누락 시 전체 중단
            display.show(Image.NO)
            dancing = False
            break

        # 6-2) 마스터 본체도 같은 동작 수행
        action = move['action']
        print("Master exec:", action)

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
                abot.rotate_degrees(30);  sleep(100)
                abot.rotate_degrees(-30); sleep(100)

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
                display.show(img); sleep(150)
            display.clear()

        elif action == 'melody':
            music.play(['c4:4','e4:4','g4:4'], wait=True)

        # 다음 동작 전 잠깐 대기
        sleep(50)

    music.stop()
    abot.servo_speed_calibrated(0, 0)

# 7. 메인 루프: start/stop 신호 처리
def main():
    global dancing, prev_logo_state
    display.scroll("Ready")

    while True:
        current = pin_logo.is_touched()
        if current and not prev_logo_state:
            dancing = not dancing

            if dancing:
                # 1) 시작 명령
                radio.send('start')
                display.show(Image.SQUARE)
                # 2) 모든 슬레이브 준비 ACK 대기
                if wait_for_all_acks():
                    display.show(Image.HAPPY)
                    dance()
                else:
                    display.show(Image.NO)
                    dancing = False

            else:
                # 중지 명령
                radio.send('stop')
                abot.servo_speed_calibrated(0, 0)
                display.show(Image.SAD)

        prev_logo_state = current
        sleep(50)

if __name__ == "__main__":
    main()
