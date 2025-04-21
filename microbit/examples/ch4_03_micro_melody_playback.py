# ch4_03_micro_melody_playback.py

from microbit import *
import music

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

# Main loop
while True:
    for note in score:
        if note in notes:
            frequency = notes[note]
            # If frequency > 0, play the note; otherwise, it's a rest
            if frequency > 0:
                music.pitch(frequency, duration)
            else:
                sleep(duration)
    # Wait 5 seconds before repeating the melody
    sleep(5000)
