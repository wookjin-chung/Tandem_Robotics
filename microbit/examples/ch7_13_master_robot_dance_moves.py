# ch7_13_master_robot_dance_moves.py

from microbit import *
from microbit_abot import *
from abot_calibrated import *
import radio
import music

# Configure radio communication
radio.on()
radio.config(group=1)

# Initialize the robot
abot = CalibratedMotionBot(13, 12)
abot.servo_attachpins()
abot.set_left_speed_offset(-5)
abot.set_calibrated_speed(65, -66, 2200)
abot.servo_speed_calibrated(0, 0)

dancing = False
prev_logo_state = False

# Define the dance move sequence
dance_moves = [
    {'action': 'forward',   'duration': 300},
    {'action': 'pause',     'duration': 200},
    {'action': 'rotate',    'angle': 90},
    {'action': 'pause',     'duration': 200},
    {'action': 'spin360'},                # 360° 회전
    {'action': 'pause',     'duration': 200},
    {'action': 'wiggle'},                  # 좌우 흔들기
    {'action': 'pause',     'duration': 200},
    {'action': 'zigzag',    'duration': 400},  # 지그재그
    {'action': 'pause',     'duration': 200},
    {'action': 'flash'},                   # LED 플래시
    {'action': 'melody'},                  # 간단 멜로디
]

def dance():
    global dancing
    try:
        music.play(music.DADADADUM, wait=False)
        for move in dance_moves:
            if not dancing:
                break

            action = move['action']
            print("Executing action:", action)

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
                # 앞뒤 전진 → 회전 → 전진 → 반대 회전
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
                # 간단한 음계 재생
                music.play(['c4:4', 'e4:4', 'g4:4'], wait=True)

            elif action == 'pause':
                sleep(move['duration'])

            # 동작 중간에 스톱 요청이 들어오면 즉시 종료
            if not dancing:
                break
            sleep(50)

        music.stop()

    except Exception as e:
        print("Error during dance:", e)
        abot.servo_speed_calibrated(0, 0)
        display.show(Image.SAD)
        dancing = False
        
def main():
    global dancing, prev_logo_state
    display.scroll("Ready")

    while True:
        current_logo_state = pin_logo.is_touched()
        if current_logo_state and not prev_logo_state:
            dancing = not dancing
            if dancing:
                radio.send('start')
                display.show(Image.HAPPY)
                dance()
            else:
                radio.send('stop')
                abot.servo_speed_calibrated(0, 0)
                display.show(Image.SAD)
        prev_logo_state = current_logo_state
        sleep(50)

if __name__ == "__main__":
    main()
