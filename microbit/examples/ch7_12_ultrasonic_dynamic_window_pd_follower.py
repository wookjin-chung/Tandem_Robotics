# ch7_12_ultrasonic_dynamic_window_pd_follower.py

from microbit import *
from microbit_abot import *
from ultrasonic import *
from abot_calibrated import *

# ===============================================
# 1. 설정 상수
# ===============================================
MIN_ANGLE       = 20
MAX_ANGLE       = 160
STEP            = 2
MAX_DIST        = 100
OBJ_THRESH      = 50

STEER_TARGET    = 90
STEER_KP, STEER_KD = 0.3, 0.4

TARGET_DIST     = 20
DIST_KP, DIST_KD   = -10, -2

WINDOW          = 45   # 동적 윈도우 반폭 (°)
LOST_LIMIT      = 3    # 연속 감지 실패 후 스캔 모드 진입

# 칼만 필터 파라미터
kalman_est = STEER_TARGET
kalman_err = 15
R, Q = 15, 0.2

# ===============================================
# 2. 유틸리티
# ===============================================
def kalman_update(meas, est, err, R, Q):
    K = err / (err + R)
    new_est = est + K * (meas - est)
    new_err = (1 - K) * err + Q
    return new_est, new_err

def clamp(x, lo, hi):
    return lo if x < lo else hi if x > hi else x

# ===============================================
# 3. 인스턴스 초기화
# ===============================================
abot = CalibratedMotionBot(13, 12)
abot.servo_attachpins()
abot.set_left_speed_offset(-5)
abot.set_calibrated_speed(65, -66, 2200)
abot.servo_speed_calibrated(0, 0)

scan_servo = bot(10)
ultra      = Ultrasonic(9)

display.scroll("Ready")
sleep(500)

# ===============================================
# 4. 상태 변수
# ===============================================
scan_min, scan_max = MIN_ANGLE, MAX_ANGLE
angle, direction  = scan_min, STEP

lost_count    = 0
last_left     = 0
last_right    = 0
last_angle    = STEER_TARGET

prev_steer_e = 0
prev_dist_e  = 0

# ===============================================
# 5. 메인 루프
# ===============================================
while True:
    # — 서보 위치: 스캔 모드일 때만 sweep, 아니면 마지막 검출 각도 고정
    if lost_count >= LOST_LIMIT:
        scan_servo.servo_angle(angle)
    else:
        scan_servo.servo_angle(int(last_angle))
    sleep(15)

    # — 거리 측정
    d = ultra.distance('cm')
    meas = MAX_DIST if d is None else min(int(d), MAX_DIST)

    if meas <= OBJ_THRESH:
        # — 객체 검출!
        lost_count = 0

        # 1) 칼만 필터로 각도 추정
        kalman_est, kalman_err = kalman_update(angle, kalman_est, kalman_err, R, Q)
        last_angle = kalman_est

        # 2) 방향 PD
        err_s = STEER_TARGET - kalman_est
        der_s = err_s - prev_steer_e
        prev_steer_e = err_s
        steer_c = STEER_KP * err_s + STEER_KD * der_s

        # 3) 거리 PD
        err_d = TARGET_DIST - meas
        der_d = err_d - prev_dist_e
        prev_dist_e = err_d
        dist_c = DIST_KP * err_d + DIST_KD * der_d

        # 4) 휠 속도 조합
        MAX_CTRL = 70
        left_spd  = clamp(int((dist_c + steer_c) * (MAX_CTRL/100)), -MAX_CTRL, MAX_CTRL)
        right_spd = clamp(int((-dist_c + steer_c) * (MAX_CTRL/100)), -MAX_CTRL, MAX_CTRL)
        last_left, last_right = left_spd, right_spd

        abot.servo_speed_calibrated(left_spd, right_spd)
        display.show("M")  # Moving

        # 5) 동적 윈도우 갱신
        scan_min = max(MIN_ANGLE, int(kalman_est) - WINDOW)
        scan_max = min(MAX_ANGLE, int(kalman_est) + WINDOW)
        angle    = clamp(angle, scan_min, scan_max)

    else:
        # — 감지 실패
        lost_count += 1

        if lost_count < LOST_LIMIT:
            # *히스테리시스 구간*: 마지막 속도 유지, 서버 각도 고정
            abot.servo_speed_calibrated(last_left, last_right)
            display.show("H")  # Hold
            continue
        else:
            # *진짜 스캔 모드* 진입
            abot.servo_speed_calibrated(0, 0)
            display.show("C")  # Scanning

    # — 스캔 모드일 때만 각도 sweep
    if lost_count >= LOST_LIMIT:
        angle += direction
        if angle >= scan_max:
            angle = scan_max
            direction = -STEP
        elif angle <= scan_min:
            angle = scan_min
            direction = STEP

    sleep(20)
