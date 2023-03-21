"""! 
@file main.py
    This file contains the main
    
    @author Jack Ellsworth, Hannah Howe, Mathew Smith
    @date   14-Mar-2023
    @copyright (c) 2023 by Nobody and released under GNU Public License v3
"""
import utime
import gc
import pyb
import cotask
import task_share
from mlx_cam import MLX_Cam
from machine import I2C
from pi_control import PI_Control
from motor_driver import Motor_Driver
from encoder_reader import Encoder_Reader

def yaw_motor_task(shares):
    """!
    This function contains the task for controlling the yaw motor. 

    @param shares A list holding the shared variables used by this task
    """
    yaw_position, pitch_position, yaw_boolean, pitch_boolean, timer_boolean = shares
    en1_pin = pyb.Pin(pyb.Pin.board.PB6, pyb.Pin.IN)
    en2_pin = pyb.Pin(pyb.Pin.board.PB7, pyb.Pin.IN)
    timer3 = pyb.Timer(4, prescaler=0, period=0xFFFF)
    e = Encoder_Reader(en1_pin, en2_pin, timer3)
    angles = [190, 188, 186, 184, 182, 180, 178, 176, 174, 172, 170]
    
    # Set up motor for the B pins
    en_pin = pyb.Pin(pyb.Pin.board.PA10, pyb.Pin.OUT_OD, pyb.Pin.PULL_UP)
    in1pin = pyb.Pin(pyb.Pin.board.PB4, pyb.Pin.OUT_PP)
    in2pin = pyb.Pin(pyb.Pin.board.PB5, pyb.Pin.OUT_PP)
    tim = pyb.Timer(3, prescaler = 0 , period = 0xFFFF)
    m = Motor_Driver(en_pin, in1pin, in2pin, tim)
    
    
    # Set up control class
    Kp = 0.05       # Motor control parameter
    Ki = 0.0
    Kd = 0.0
    freq = 1/.002
    c = PI_Control(Kp, Ki, Kd, freq, 0, e, m)
    scale = 2000
    
    # Get references to the share and queue which have been passed to this task
    yield 0
    while True:
        if(yaw_position.get() == -1):
            c.run(180 * scale)
        else:
            index = yaw_position.get() - 8
            if(index) <= 0:
                index = 0
            if(index) >= 11:
                index = 10
            c.run(angles[index] * scale)
            #c.run(yaw_position.get())
        yield 0


def pitch_motor_task(shares):
    """!
    This function contains the task for controlling the pitch motor. 

    @param shares A list holding the shared variables used by this task
    """
    yaw_position, pitch_position, yaw_boolean, pitch_boolean, timer_boolean = shares
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
    
    # Get references to the share and queue which have been passed to this task
    yield 0
    while True:
        if(pitch_position.get() == -1):
            c.run(0)
        else:
            c.run(0)
            #c.run(pitch_position.get())
        yield 0

def camera_task(shares):
    """!
    This function contains the task for image capturing and analyzing the thermal camera

    @param shares A list holding the shared variables used by this task
    """
    # Get references to the share and queue which have been passed to this task
    yaw_position, pitch_position, yaw_boolean, pitch_boolean, timer_boolean = shares
    
    i2c_bus = I2C(1)
    i2c_address = 0x33
    camera = MLX_Cam(i2c_bus)
    runs = 0
    yield 0
    
    while True:
        # Show everything currently in the queue and the value in the share
        if runs >= 4:
            yield 0
        else:
            if(timer_boolean.get() != 2):
                pitch_position.put(-1)
                yaw_position.put(-1)
                yield 0
            else:
                image = camera.get_image()
                index = 0
                highest_index = 0
                highest = -999999
                for i in image:
                    i += 100
                    if i > highest:
                        highest_index = index
                        highest = i
                    index += 1
        
                print(highest, highest_index % 32, 24 - int(highest_index / 32))
                yaw_position.put(24 - int(highest_index / 32))
                pitch_position.put(highest_index % 32)
                #camera.ascii_art(image)
                runs += 1
                yield 0

def fire_task(shares):
    """!
    This function contains the task for firing the turret. 

    @param shares A list holding the shared variables used by this task
    """
    # Get references to the share and queue which have been passed to this task
    yaw_position, pitch_position, yaw_boolean, pitch_boolean, timer_boolean = shares
    
    yield 0
    while True:
        # Show everything currently in the queue and the value in the share
        #if(timer_boolean.get() >= 1):
        #    print("Spinning Flywheel")
        yield 0
    
def timer_task(shares):
    """!
    This function contains the task for timing events between tasks. 

    @param shares A list holding the shared variables used by this task
    """
    # Get references to the share and queue which have been passed to this task
    yaw_position, pitch_position, yaw_boolean, pitch_boolean, timer_boolean = shares
    initial_time = utime.ticks_ms()
    timer_boolean.put(0)
    yield 0
    while True:
        # Show everything currently in the queue and the value in the share
        if(utime.ticks_ms() - initial_time >= 5000):
            timer_boolean.put(2)
        elif(utime.ticks_ms() - initial_time >= 4000):
            timer_boolean.put(1)
        else:
            timer_boolean.put(0)
        yield 0


# This code creates a share, a queue, and two tasks, then starts the tasks. The
# tasks run until somebody presses ENTER, at which time the scheduler stops and
# printouts show diagnostic information about the tasks, share, and queue.
if __name__ == "__main__":
    print("Testing ME405 stuff in cotask.py and task_share.py\r\n"
          "Press Ctrl-C to stop and show diagnostics.")

    # Create a share and a queue to test function and diagnostic printouts
    yaw_position = task_share.Share('h', thread_protect = False, name = "yaw_position")
    pitch_position = task_share.Share('h', thread_protect = False, name = "pitch_position")
    yaw_boolean = task_share.Share('h', thread_protect = False, name = "yaw_boolean")
    pitch_boolean = task_share.Share('h', thread_protect = False, name = "pitch_boolean")
    timer_boolean = task_share.Share('b', thread_protect = False, name = "timer_boolean")
    
    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    task1 = cotask.Task(pitch_motor_task, name="pitch_motor_task", priority=3, period=10,
                        profile=True, trace=False, shares=(yaw_position, pitch_position, yaw_boolean, pitch_boolean, timer_boolean))
    task2 = cotask.Task(yaw_motor_task, name="yaw_motor_task", priority=3, period=10,
                        profile=True, trace=False, shares=(yaw_position, pitch_position, yaw_boolean, pitch_boolean, timer_boolean))
    task3 = cotask.Task(camera_task, name="camera_task", priority=1, period=500,
                        profile=True, trace=False, shares=(yaw_position, pitch_position, yaw_boolean, pitch_boolean, timer_boolean))
    task4 = cotask.Task(fire_task, name="fire_task", priority=2, period=100,
                        profile=True, trace=False, shares=(yaw_position, pitch_position, yaw_boolean, pitch_boolean, timer_boolean))
    task5 = cotask.Task(timer_task, name="timer_task", priority=0, period=100,
                        profile=True, trace=False, shares=(yaw_position, pitch_position, yaw_boolean, pitch_boolean, timer_boolean))
    
    #cotask.task_list.append(task1)
    cotask.task_list.append(task2)
    cotask.task_list.append(task3)
    cotask.task_list.append(task4)
    cotask.task_list.append(task5)

    # Run the memory garbage collector to ensure memory is as defragmented as
    # possible before the real-time scheduler is started
    gc.collect()

    # Run the scheduler with the chosen scheduling algorithm. Quit if ^C pressed
    while True:
        try:
            cotask.task_list.pri_sched()
        except KeyboardInterrupt:
            break

    # Print a table of task data and a table of shared information data
    print('\n' + str (cotask.task_list))
    print(task_share.show_all())
    print(task3.get_trace())
    print('')
