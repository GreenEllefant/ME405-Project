"""! 
    This file contains the Position Control class
    
    @author Jack Ellsworth, Hannah Howe, Mathew Smith
    @date   05-Feb-2023
    @copyright (c) 2023 by Nobody and released under GNU Public License v3
"""
import utime

class PI_Control:
    """! 
    This class implements a closed loop position control for a motor
    """
    def __init__(self, gain, ki, setpoint, encoder, motor):
        """! 
        Creates a closed loop by initializing values
        used for closed loop control.
        @param gain: sets the gain from the controller
        @param setpoint: sets the initial setpoint for the controller
        @param encoder: takes an encoder_reader class for the system
        @param motor: takes a motor_driver class for the system
        """
        self.gain = gain
        self.ki = ki
        self.total_error = 0
        self.setpoint = setpoint
        self.values = [0, 0]
        self.encoder = encoder
        self.motor = motor
        self.time = utime.ticks_ms()
        self.prev_time = utime.ticks_ms()

    def run(self, setpoint):
        """! 
        Updates the system parameters
        @param gain: sets the gain from the controller
        @param setpoint: sets the initial setpoint for the controller
        @param encoder: takes an encoder_reader class for the system
        @param motor: takes a motor_driver class for the system
        """
        self.setpoint = setpoint
        self.values[0] = utime.ticks_ms() - self.time
        self.values[1] = self.encoder.read()
        pwm = self.gain * (self.setpoint - self.encoder.read()) + self.ki * (self.ki + (self.setpoint - self.encoder.read()) * (utime.ticks_ms() - self.prev_time))
        if pwm > 100:
            pwm = 99.9
        if pwm < -100:
            pwm = -99.9
        self.motor.set_duty_cycle(pwm)
        self.prev_time = utime.ticks_ms()

    def reset_values(self):
        """! 
        Resets the system values and time
        """
        self.values = [0, 0]
        self.time = utime.ticks_ms()

    def set_setpoint(self, setpoint):
        """!
        Sets a new setpoint
        @param setpoint: The new setpoint
        """
        self.setpoint = setpoint
    
    def set_Kp(self, gain):
        """!
        Sets a new controller gain
        @param gain: The new controller gain
        """
        self.gain = gain

    def set_Ki(self, gain):
        self.ki = gain

    def print_values(self):
        """!
        Print the values collected from running
        """
        for i in range(0, len(self.values[0])):
            print(str(self.values[0][i]) + "," + str(self.values[1][i]))
        
if __name__ == "__main__":
    en1_pin = pyb.Pin(pyb.Pin.board.PC6, pyb.Pin.IN)
    en2_pin = pyb.Pin(pyb.Pin.board.PC7, pyb.Pin.IN)
    timer3 = pyb.Timer(8, prescaler=0, period=0xFFFF)
    e = Encoder_Reader(en1_pin, en2_pin, timer3)
    
    # Set up motor for the B pins
    en_pin = pyb.Pin(pyb.Pin.board.PC1, pyb.Pin.OUT_OD, pyb.Pin.PULL_UP)
    in1pin = pyb.Pin(pyb.Pin.board.PA0, pyb.Pin.OUT_PP)
    in2pin = pyb.Pin(pyb.Pin.board.PA1, pyb.Pin.OUT_PP)
    timer5 = pyb.Timer(5, prescaler = 0, period = 0xFFFF)
    m = Motor_Driver(en_pin, in1pin, in2pin, timer5)
    
    # Set up control class
    Kp = 0.5       # Motor control parameter
    Ki = 0.001      
    c = PI_Control(Kp, Ki, 0, e, m)
    
    switch = False
    time = utime.ticks_ms()
    # Get references to the share and queue which have been passed to this task
    while True:
        if(switch):
            c.run(2000)
        else:
            c.run(-2000)
        if(utime.ticks_ms() - time > 1000):
            time = utime.ticks_ms()
            if(switch):
                switch = False
            else:
                switch = True