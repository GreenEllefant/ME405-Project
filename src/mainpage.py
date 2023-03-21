'''! @file mainpage.py
@author Jack Ellsworth, Mathew Smith, Hannah Howe
@mainpage

@section ss_introduction Software Summary

Our completes three main functions, taking an image with the thermal camera to determine the targets position, moving the motors to aim the nerf rifle to the target position, and firing the rifle once certain parameters have been met. The gives us five total tasks, one for each motor that positions the rifle, one for capturing and processing the image from the thermal camera, one for firing the rifle, and one for timing the image taking and firing to occur at specific moments in time.

\image html TaskDiagram.png width=800cm

@subsection ss_Camera Camera Task
The image that is captured by the camera is stored as an iterable image data type with 768 total values. Each value corresponds to a thermal value captured by the camera. The higher the value, the hotter that spot in space is. Since the human would be the hottest item in the frame of the thermal camera, we can assume that the brightest spot in the frame is a human. Taking the index of the brightest value, we can split it into a yaw index and pitch index according to the orientation of our thermal camera. Each index corresponds to a specific pitch or yaw angle for the rifle. The camera will only take images after the target as stopped moving in order to remove any possible bugs. Additionally, only four images are taken so the task does not interfere with the motor control. This task has the longest period since it takes the most amount of time to complete.

\image html CameraStateDiagram.png width=800cm

@subsection ss_motor Motor Task
The motor control uses a simple positional control. Our class can preform PID control, but we did not take advantage of this fact. In our testing, we found that basic positional control worked best for our purposes. The positional control class works based on the ticks of the encoder. Based on gear ratios, we can change the ticks from the encoder to degrees in the real world. We are able to read the encoder and compare it to the desired value to determine how hard we want to run the motors. This task has the highest period rate since it needs to be run multiple times in order for accurate data from the encoder. Once the motors are within a certain distance from the target, it tells the fire task to fire the rifle.

\image html PitchStateDiagram.png width=800cm
\image html YawStateDiagram.png width=800cm

@subsection ss_firing Firing Task
The firing task waits until a certain amount of time has elapsed. Once that time has elapsed, it will turn on the flywheels and wait until the rifle is in position to fire. Once the motor tasks have determined that rifle is in position, the firing task then fires the rifle at the target.

\image html FireStateDiagram.png width=800cm

@subsection ss_timing Timing Task
The timing task simply calculates how long the program as been running. It does this so that it can time when to capture images and when it is able to fire safely without losing points. Once four seconds have passed, it tells the firing task to start spinning the flywheels. After 5 seconds, the timing task tells the camera task to start capturing images. Since timing is critical to the execution of the program, this task has the highest priority.

\image html TimingStateDiagram.png width=800cm

'''