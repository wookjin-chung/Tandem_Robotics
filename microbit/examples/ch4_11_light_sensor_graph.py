# ch4_11_light_sensor_graph.py

from microbit import *

while True:
    # Read the light sensor value (range: 0 to 255)
    light_level = display.read_light_level()
    
    # Clear the display before plotting the graph
    display.clear()
    
    # Convert the light_level to a number of LEDs to light up in a 5x5 matrix
    num_leds = light_level * 25 // 256  # Maximum of 25 LEDs
    
    # Light up LEDs according to the converted value
    for i in range(num_leds):
        # Set brightness to 9
        display.set_pixel(i % 5, i // 5, 9)
    
    # Print the light level value to the serial monitor
    print("Light level:", light_level)
    
    # Wait for 1 second
    sleep(1000)
