# ch7_19_distributed_dance_sequence.py

from microbit import *
from microbit_abot import *
from abot_calibrated import *
import radio
import music

# —————————————————————————————————————————————————
# 1. Radio 설정 (같은 그룹)
# —————————————————————————————————————————————————
radio.on()
radio.config(group=1)

# —————————————————————————————————————————————————
# 2. 로봇 초기화
# —————————————————————————————————————————————————
abot = CalibratedMotionBot(13, 12)
abot.servo_attachpins()
abot.set_left_speed_offset(-5)
abot.set_calibrated_speed(65, -66, 2200)
abot.servo_speed_calibrated(0, 0)

# —————————————————————————————————————————————————
# 3. 미리 정의된 군무 시퀀스들
# —————————————————————————————————————————————————
sequence_names = ['Classic', 'Quick', 'SpinOnly']

# (1) Classic: 원래의 다채로운 동작
classic_moves = [
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

# (2) Quick: 빠른 전진 ↔ 후진 패턴
quick_moves = [
    {'action': 'forward',   'duration': 200},
    {'action': 'pause',     'duration': 100},
    {'action': 'backward',  'duration': 200},
    {'action': 'pause',     'duration': 100},
]

# (3) SpinOnly: 360° 회전만 반복
spin_only_moves = [
    {'action': 'spin360'},
    {'action': 'pause',     'duration': 300},
]

dance_sequences = [classic_moves, quick_moves, spin_only_moves]

# 초기 선택
seq_index = 0
dance_moves = dance_sequences[seq_index]

# —————————————————————————————————————————————————
# 4. 개별 동작 처리 함수
#    (중간에 TOGGLE/SELECT 수신 시에도 반응)
# —————————————————————————————————————————————————
def perform_move(move):
    global dancing, seq_index, dance_moves

    # 토글 신호 우선 처리
    msg = radio.receive()
    if msg == 'TOGGLE':
        dancing = not dancing
        return False
    # 시퀀스 변경 신호 처리
    elif msg and msg.startswith('SELECT:'):
        idx = int(msg.split(':')[1])
        if 0 <= idx < len(dance_sequences):
            seq_index = idx
            dance_moves = dance_sequences[idx]
        return False

    # 실제 동작
    action = move['action']
    if action == 'forward':
        abot.servo_speed_calibrated(50, -50)
        sleep(move['duration'])
        abot.servo_speed_calibrated(0, 0)

    elif action == 'backward':
        abot.servo_speed_calibrated(-50, 50)
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

    # 마무리 토글/선택 신호 체크
    msg = radio.receive()
    if msg in ('TOGGLE',) or (msg and msg.startswith('SELECT:')):
        if msg == 'TOGGLE':
            dancing = not dancing
        else:
            idx = int(msg.split(':')[1])
            if 0 <= idx < len(dance_sequences):
                seq_index = idx
                dance_moves = dance_sequences[idx]
        return False

    return True

# —————————————————————————————————————————————————
# 5. dance(): 선택된 dance_moves 전체 반복
# —————————————————————————————————————————————————
def dance():
    global dancing
    music.play(music.DADADADUM, wait=False)
    for move in dance_moves:
        if not dancing:
            break
        if not perform_move(move):
            break
    music.stop()
    abot.servo_speed_calibrated(0, 0)

# —————————————————————————————————————————————————
# 6. 메인 루프: 버튼 A 토글 / 버튼 B 시퀀스 선택
# —————————————————————————————————————————————————
dancing = False
while True:
    # (1) 버튼 A: dancing 토글 & 방송
    if button_a.was_pressed():
        dancing = not dancing
        radio.send('TOGGLE')
        display.show(Image.HAPPY if dancing else Image.SAD)
        sleep(200)
        display.clear()
        # dancing 상태일 때 바로 dance() 실행
        if dancing:
            dance()

    # (2) 버튼 B: seq_index 순환 & 방송
    if button_b.was_pressed() and not dancing:
        seq_index = (seq_index + 1) % len(dance_sequences)
        dance_moves = dance_sequences[seq_index]
        # 화면에 시퀀스 이름 표시
        display.scroll(sequence_names[seq_index])
        radio.send('SELECT:{}'.format(seq_index))
        sleep(200)
        display.clear()

    # (3) 네트워크 토글/선택 메시지 수신
    msg = radio.receive()
    if msg == 'TOGGLE':
        dancing = not dancing
        display.show(Image.HAPPY if dancing else Image.SAD)
        sleep(200)
        display.clear()
        if dancing:
            dance()
    elif msg and msg.startswith('SELECT:'):
        idx = int(msg.split(':')[1])
        if 0 <= idx < len(dance_sequences):
            seq_index = idx
            dance_moves = dance_sequences[idx]
            display.scroll(sequence_names[idx])
            sleep(200)
            display.clear()

    sleep(50)
