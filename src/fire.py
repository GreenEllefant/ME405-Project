
'''! @file fire.py
@author Hannah Howe
@fire

Description: 
this will be a class that establishes the firing capabilities of the blaster
'''

        
class fire:
    def __init__(self, m1_pin, m2_pin, target_ac):
        self.m1_pin = m1_pin
        self.m2_pin = m2_pin
        self.target_ac = target_ac


    def flywheel(self, timeset):
        #turn on motor 1 to get flywheel up to speed
        
        pass
    
    def piston(self):
        #turn on motor 2 to push dart into flywheel
        pass
    
    def release(self, target_ac):
        if target_ac == 1:          #check if target_ac == 1 (or some other agreed value)
                                    #turn flywheel on: delay ~3 seconds
            pass
        else:
            pass                    #if flywheel is on turn on piston else don't move piston
        


