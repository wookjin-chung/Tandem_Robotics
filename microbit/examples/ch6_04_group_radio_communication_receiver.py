# ch6_04_group_radio_communication_receiver.py

from microbit import *
import radio

radio.on()  # Turn on the radio

groups = [1, 99]  # List of groups to receive
group_index = 0
current_group = groups[group_index]
radio.config(group=current_group)

# Time to stay on each group (milliseconds)
GROUP_SWITCH_INTERVAL = 500
last_switch_time = running_time()

def flush_radio_buffer():
    # Read all received messages to clear the buffer
    while radio.receive() is not None:
        pass

while True:
    incoming = radio.receive()
    if incoming:
        if current_group == 1:
            # Display when individual message is received
            display.show(Image.HAPPY)
            sleep(2000)
            display.clear()
        elif current_group == 99:
            # Display when multi-message is received
            display.show(Image.GIRAFFE)
            sleep(2000)
            display.clear()

    # Switch groups at every GROUP_SWITCH_INTERVAL
    if running_time() - last_switch_time > GROUP_SWITCH_INTERVAL:
        # Flush the buffer before switching groups
        flush_radio_buffer()
        group_index = (group_index + 1) % len(groups)
        current_group = groups[group_index]
        radio.config(group=current_group)
        last_switch_time = running_time()
