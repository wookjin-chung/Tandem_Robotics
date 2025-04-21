"""
microbit_abot.py
I2C communication for Micro:bit (master) to Arduino Uno (slave) robot.
Use alongside the provided Arduino library and example codes.
Repo: https://github.com/wookjin-chung/Tandem_Robotics | MIT License
@fribot.com created Apr 7, 2025
@version 0.1.0
"""
from microbit import *

# Handshake with I2C device at address 93
handshake_successful = False
while not handshake_successful:
    try:
        i2c.write(93, b'\xAA')
        sleep(100)
        if i2c.read(93, 1) == b'\x55':
            print("Handshake successful")
            handshake_successful = True
    except OSError:
        pass

class bot:
    def __init__(self, p=27, q=33):
        super().__init__()
        self.pA, self.pB = p, q

    def botdisable(self):
        pin8.set_pull(pin8.NO_PULL)
        sleep(200)
        reset()

    def send_c(self, c, s=0, d=None, f=None):
        a = bytes([1, self.pA, self.pB, s])
        if d is not None:
            a += int(round(d)).to_bytes(4, 'little')
        if f is not None:
            a += int(round(f)).to_bytes(4, 'little')
        try:
            i2c.write(93, a)
            i2c.write(93, bytes([0, c]))
            c_val = b'\x01'
            while c_val != b'\0':
                i2c.write(93, b'\0')
                c_val = i2c.read(93, 1)
        except:
            self.botdisable()

    def read_r(self):
        try:
            req = bytes([0x18, self.pA])
            i2c.write(93, req)
            r = i2c.read(93, 4)
            return int.from_bytes(r, 'little')
        except:
            self.botdisable()

    def write_digital(self, s):
        if s > 1 or s < 0:
            s = 4
        elif s == 0:
            s = 2
        self.send_c(s)

    def write_analog(self, f):
        self.send_c(32, 0, f)

    def read_digital(self):
        self.send_c(3)
        return self.read_r()

    def pulse_out(self, d):
        self.send_c(11, 0, d)

    def pulse_in(self, s):
        self.send_c(10, s)
        return self.read_r()

    def pulse_count(self, d):
        self.send_c(12, 0, d)
        return self.read_r()

    def rc_time(self, s, d=None, f=None):
        self.send_c(16, s, d, f)
        return self.read_r()

    def tone(self, f, d):
        self.send_c(13, 0, d, f)

    def ir_detect(self, f):
        bot(self.pB, self.pA).send_c(31, 0, f)
        return self.read_r()

    def ir_distance(self):
        bot(self.pB, self.pA).send_c(33, 0)
        return self.read_r()

    def servo_attachpins(self):
        self.send_c(38)

    def servo_angle(self, v=None):
        c = 28 if v is None else 24
        self.send_c(c, 0, v)

    def servo_speed(self, vL=None, vR=None):
        c = 28 if vL is None else 25
        self.send_c(c, 0, vL, vR)

    def detach(self):
        self.send_c(39, 0)
