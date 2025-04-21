# ch7_18_peer_to_peer_dance_LEDs.py

from microbit import *
import radio

# 1. 설정
radio.on()
radio.config(group=1)

# 각 로봇마다 고유 ID를 지정 (0,1,2,... 등)
MY_ID = 0          # ← 기기별로 바꿔주세요
TOTAL_NODES = 3    # 네트워크에 참여한 로봇 대수

# 준비 메시지 수신 집합
ready_set = set()

# 2. 메시지 브로드캐스트 함수
def broadcast_ready():
    radio.send('READY:{}'.format(MY_ID))

# 3. 합의(Consensus) 확인 함수
def wait_for_all_ready(timeout=5000):
    """
    timeout(ms) 동안 READY:<ID> 메시지를 수집해서
    서로 TOTAL_NODES 만큼 모였으면 True 반환
    """
    start = running_time()
    ready_set.clear()
    # 자기 자신도 포함
    ready_set.add(str(MY_ID))
    while running_time() - start < timeout:
        msg = radio.receive()
        if msg and msg.startswith('READY:'):
            _, peer_id = msg.split(':')
            ready_set.add(peer_id)
        if len(ready_set) >= TOTAL_NODES:
            return True
    return False

# 4. 분산 군무 동작 예시
def do_dance():
    # LED 3번 깜빡이기
    for _ in range(3):
        display.show(Image.HEART)
        sleep(300)
        display.clear()
        sleep(300)

# 5. 메인 루프
while True:
    # A 버튼: 준비 신호 발신
    if button_a.was_pressed():
        display.show('R')           # Ready 알림
        broadcast_ready()

        if wait_for_all_ready():
            # 모두 준비되면 동시에 군무 시작
            display.show(Image.HAPPY)
            do_dance()
        else:
            # 타임아웃 시 실패 표시
            display.show(Image.NO)

        # 종료 후 초기화
        ready_set.clear()
        sleep(500)
        display.clear()

    # B 버튼: 전체 정지(예시)
    if button_b.was_pressed():
        display.show(Image.SAD)
        # 필요 시 모터 정지 로직 삽입
        sleep(500)
        display.clear()

    sleep(100)
