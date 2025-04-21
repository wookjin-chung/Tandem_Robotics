# ch5_02_abot_basic_drive.py

from microbit_abot import *

def check_logo_touch():
    if pin_logo.is_touched():
        reset()

bot(13, 12).servo_attachpins()

# forward drive
bot(13, 12).servo_speed(100, -100)
sleep(2000)

# pivot left
bot(13, 12).servo_speed(0, -100)
sleep(1000)

# pivot right
bot(13, 12).servo_speed(100, 0)
sleep(1000)

# backward drive
bot(13, 12).servo_speed(-100, 100)
sleep(2000)

# detach servo
bot(13).detach()
bot(12).detach()

while True:
    check_logo_touch()
    sleep(100)
