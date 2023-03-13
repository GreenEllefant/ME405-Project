"""!
@file basic_tasks.py
    This file contains a demonstration program that runs some tasks, an
    inter-task shared variable, and a queue. The tasks don't really @b do
    anything; the example just shows how these elements are created and run.

@author JR Ridgely
@date   2021-Dec-15 JRR Created from the remains of previous example
@copyright (c) 2015-2021 by JR Ridgely and released under the GNU
    Public License, Version 2. 
"""

import gc
import pyb
import cotask
import task_share
from mlx_cam import MLX_Cam
from machine import I2C

def pitch_motor_task(shares):
    """!AS
    Task which puts things into a share and a queue.
    @param shares A list holding the share and queue used by this task
    """
    the_queue = shares
    
    # Get references to the share and queue which have been passed to this task
    I2C = pyb.I2C(1, pyb.I2C.CONTROLLER)
    accel = MMA845x(I2C, 29)
    accel.active()
    yield 0
    while True:
        the_queue.put(accel.get_ax())
        yield 0


def yaw_motor_task(shares):
    """!
    Task which takes things out of a queue and share and displays them.
    @param shares A tuple of a share and queue from which this task gets data
    """
    # Get references to the share and queue which have been passed to this task
    the_queue = shares
    
    yield 0
    while True:
        # Show everything currently in the queue and the value in the share
        if(the_queue.any()):
            print(f"{the_queue.get()}")
        yield 0

def camera_task(shares):
    """!
    Task which takes things out of a queue and share and displays them.
    @param shares A tuple of a share and queue from which this task gets data
    """
    # Get references to the share and queue which have been passed to this task
    yaw_position, pitch_position, yaw_boolean, pitch_boolean = shares
    
    i2c_bus = I2C(1)
    i2c_address = 0x33
    camera = MLX_Cam(i2c_bus)
    yield 0
    
    while True:
        # Show everything currently in the queue and the value in the share
        image = camera.get_image()
        index = 0
        highest_index = 0
        highest = -999999
        for i in image:
            if i > highest:
                highest_index = index
                highest = i
            index += 1
        
        print(highest_index % 32, 24 - int(highest_index / 24))
        yaw_position.put(24 - int(highest_index / 24))
        pitch_position.put(highest_index % 32)
        #camera.ascii_art(image)
        yield 0

def fire_task(shares):
    """!
    Task which takes things out of a queue and share and displays them.
    @param shares A tuple of a share and queue from which this task gets data
    """
    # Get references to the share and queue which have been passed to this task
    the_queue = shares
    
    yield 0
    while True:
        # Show everything currently in the queue and the value in the share
        if(the_queue.any()):
            print(f"{the_queue.get()}")
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
    
    # Create the tasks. If trace is enabled for any task, memory will be
    # allocated for state transition tracing, and the application will run out
    # of memory after a while and quit. Therefore, use tracing only for 
    # debugging and set trace to False when it's not needed
    #task1 = cotask.Task(pitch_motor_task, name="pitch_motor_task", priority=1, period=2,
    #                    profile=True, trace=False, shares=(yaw_position, pitch_position, yaw_boolean, pitch_boolean))
    #task2 = cotask.Task(yaw_motor_task, name="yaw_motor_task", priority=2, period=2,
    #                    profile=True, trace=False, shares=(yaw_position, pitch_position, yaw_boolean, pitch_boolean))
    task3 = cotask.Task(camera_task, name="camera_task", priority=2, period=1250,
                        profile=True, trace=False, shares=(yaw_position, pitch_position, yaw_boolean, pitch_boolean))
    #task4 = cotask.Task(fire_task, name="fire_ta", priority=2, period=2,
    #                    profile=True, trace=False, shares=(yaw_position, pitch_position, yaw_boolean, pitch_boolean))
    #cotask.task_list.append(task1)
    #cotask.task_list.append(task2)
    cotask.task_list.append(task3)
    #cotask.task_list.append(task4)

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
