# ch4_14_micro_analog_voltage_reader.py

from microbit import *

# Infinite loop
while True:
    # Read the analog input from pin P0
    analog_value = pin0.read_analog()
    
    # Convert the analog value to an actual voltage
    voltage = (analog_value / (1024 - 1)) * 3.3
    
    # Display the measured voltage on the micro:bit LED
    # display.scroll("{:.2f}V".format(voltage))
    
    # Print the measured voltage to the serial monitor
    print("{:.2f}V".format(voltage))
    
    # Wait briefly
    sleep(100)  # Wait for 1 second
