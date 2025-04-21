# ch4_04_micro_external_pin_twinkle_twinkle.py

from microbit import *
import utime

# Define note frequencies
notes = {
    'C': 1047,
    'D': 1175,
    'E': 1319,
    'F': 1397,
    'G': 1568,
    'a': 1760,
    'b': 1976,
    'c': 2093,
    ' ': 0  # Rest
}

# Melody to play
score = "CCGGaaGFFEEDDC GGFFEEDGGFFEED CCGGaaGFFEEDDC"

# Duration of each note (in milliseconds)
duration = 333

def play_note(frequency, duration):
    if frequency > 0:
        # Set pin0 to mid-point voltage (analog write)
        pin0.write_analog(512)
        # Set the analog period based on the note's frequency
        pin0.set_analog_period_microseconds(int(1000000 / frequency))
        # Play the note for the specified duration
        utime.sleep_ms(duration)
        # Turn off the pin after the duration
        pin0.write_digital(0)
    else:
        # Rest for the duration if the frequency is 0
        sleep(duration)

# Main loop
while True:
    for note in score:
        if note in notes:
            frequency = notes[note]
            play_note(frequency, duration)
    # Wait 5 seconds before repeating the melody
    sleep(5000)
