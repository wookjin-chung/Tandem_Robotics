# ch4_12_temperature_display.py

from microbit import *

while True:
    # Read the temperature in Celsius
    temp = temperature()
    
    # Display the temperature on the LED
    display.scroll(str(temp) + "C")
    
    # Print the temperature value to the serial monitor
    print("Temperature:", temp, "C")
    
    # Wait for 1 second
    sleep(1000)
