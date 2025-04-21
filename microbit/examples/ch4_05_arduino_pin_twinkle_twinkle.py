# ch4_05_arduino_pin_twinkle_twinkle.py

from microbit import *
from microbit_abot import bot  # Include the custom library

# Define the notes and their corresponding frequencies
notes = {
    'C': 262,
    'D': 294,
    'E': 330,
    'F': 349,
    'G': 392,
    'a': 440,
    'b': 494,
    'c': 523,
    ' ': 0  # Rest
}

# Define the melody for "Twinkle Twinkle Little Star"
melody = "CCGGaaGFFEEDDC GGFFEEDGGFFEED CCGGaaGFFEEDDC"

# Define the duration of each note in milliseconds
duration = 333

# Function to play a note using the Arduino buzzer
def play_note_on_arduino(note, duration):
    if note in notes:
        frequency = notes[note]
        if frequency > 0:
            bot(8).tone(frequency, duration)
            sleep(duration)

# Main loop to play the melody
while True:
    for note in melody:
        play_note_on_arduino(note, duration)
    sleep(5000)
