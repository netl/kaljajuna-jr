print("importing motor lib")
from machine import Pin, PWM

class motor():
    def __init__(self):
        self.m = [Pin(4, Pin.OUT), Pin(5, Pin.OUT)] #should be D1 & &2
        self.pwm = [PWM(self.m[0]),PWM(self.m[1])]
        for p in self.pwm:
            p.freq(1000)
            p.duty(0)

    def move(self, direction = 0):
        #parse the given direction to a float value
        direction = float(direction)

        #break
        if direction == 0:
            self.pwm[0].duty(0)
            self.pwm[1].duty(0)

        #forwards
        elif direction > 0:
            self.pwm[0].duty(0)
            self.pwm[1].duty(int(min(1,direction)*1024.0))

        #reverse
        else:
            self.pwm[0].duty(int(min(1,-direction)*1024.0))
            self.pwm[1].duty(0)
