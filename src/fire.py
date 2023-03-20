
'''! @file fire.py
This file contains code for the firing mechanism 

@author Jack Ellsworth, Hannah Howe, Mathew Smith
@date   14-Mar-2023
@copyright (c) 2023 by Nobody and released under GNU Public License v3
'''
import utime
        
class fire:
    """!
    This class contains code for the firing mechanism
    """
    def __init__(self, m1_pin, m2_pin):
        """!
        This class conatins code for the firing mechanism

        @param m1_pin The pin connected to the flywheel motor
        @param m2_pin The pin connected to the firing motor
        """
        self.m1_pin = m1_pin
        self.m2_pin = m2_pin


    def flywheel(self, highlow):
        """!
        @details: this function turns the flywheel either on or off

        @param highlow if true then the flywheel is turned on, turned off if false
        """
        if(highlow):
            self.m1_pin.high()
        else:
            self.m1_pin.low()
    
    def piston(self):
        """!
        @details: this function turns the firing mechanism 
        """
        self.m2_pin.high()
    
    def release(self):
        """!
        @details: this function turns off the firig mechanism
        """
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
        