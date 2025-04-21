# ch2_07_loop_display_numbers.py

from microbit import *

for i in range(5):
    display.scroll(str(i))
    sleep(500)
    