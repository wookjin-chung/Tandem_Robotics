# ch5_01_abot_servo_centering.py
from microbit_abot import *

def check_logo_touch():
    if pin_logo.is_touched():
        reset()

display.show(Image.HAPPY)
bot(13, 12).servo_attachpins()
bot(13, 12).servo_speed(0, 0)
sleep(5000)
display.clear()

bot(13).detach()
bot(12).detach()

while True:
    check_logo_touch()
    sleep(100)
