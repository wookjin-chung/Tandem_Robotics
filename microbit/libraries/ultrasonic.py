"""
ultrasonic.py
Provides ultrasonic sensor functionality for distance measurements.
Integrated into the Micro:bit-Arduino robot system (has-a relationship).
Repo: https://github.com/wookjin-chung/Tandem_Robotics | MIT License
@fribot.com created Apr 7, 2025
@version 0.1.0
"""
from microbit_abot import *

class Ultrasonic:
    def __init__(self, p=33, q=None):
        self.pinA = p
        self.pinB = q
        
        if self.pinB is None:
            self.bot_instance = bot(self.pinA)
        else:
            self.bot_instance = bot(self.pinA, self.pinB)

    def distance(self, u=None):
        try:
            if self.pinB is None:
                # 3-pin ultrasonic sensor like as Ping sensor
                self.bot_instance.send_c(35)
            else:
                # 4-pin ultrasonic sensor like as HR-04
                self.bot_instance.send_c(36)
                
            d = self.bot_instance.read_r()

            if d is None:
                print("Error: No signal received or invalid reading.")
                return None
            
            if u == 'us':return d
            elif u == 'in':return d / 148
            else:return d / 58

        except Exception as e:
            print("Ultrasonic error:", e)
            return None
