
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
    #zero_pin = pyb.Pin(pyb.Pin.board.PC4, pyb.Pin.IN)
    fire = fire(m1_pin, m2_pin)
    time = utime.ticks_ms()
    fire.flywheel(True)
    while(utime.ticks_ms() - time) < 3000:
        utime.sleep_ms(1)
    time = utime.ticks_ms()
    fire.piston()
    while(utime.ticks_ms() - time) < 660 * 8:
        #if(zero_pin.value() != 0):
        #    print(zero_pin.value())
        utime.sleep_ms(1)
    fire.release()
    fire.flywheel(False)
    #zero_pin = pyb.Pin(pyb.Pin.board.PC4, pyb.Pin.IN)
