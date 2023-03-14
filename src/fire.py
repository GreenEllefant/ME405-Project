
'''! @file fire.py
@author Hannah Howe
@fire

Description: 
this will be a class that establishes the firing capabilities of the blaster
'''
import utime
        
class fire:
    def __init__(self, m1_pin, m2_pin):
        self.m1_pin = m1_pin
        self.m2_pin = m2_pin


    def flywheel(self, highlow):
        #turn on motor 1 to get flywheel up to speed
        if(highlow):
            self.m1_pin.high()
        else:
            self.m1_pin.low()
        pass
    
    def piston(self):
        self.m2_pin.high()
    
    def release(self):
        self.m2_pin.low()                  #if flywheel is on turn on piston else don't move piston

if __name__ == "__main__":
    m1_pin = pyb.Pin(pyb.Pin.board.PC2, pyb.Pin.OUT_PP)
    m2_pin = pyb.Pin(pyb.Pin.board.PC3, pyb.Pin.OUT_PP)
    fire = fire(m1_pin, m2_pin)
    time = utime.ticks_ms()
    fire.flywheel(True)
    while(utime.ticks_ms() - time) < 2000:
        utime.sleep_ms(1)
    time = utime.ticks_ms()
    fire.piston()
    while(utime.ticks_ms() - time) < 700:
        utime.sleep_ms(1)
    fire.release()
    fire.flywheel(False)
   
        


