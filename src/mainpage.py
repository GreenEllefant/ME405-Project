'''! @file mainpage.py
@author Jack Ellsworth
@mainpage

@section ss_timeline Project Timeline

We laid out our timeline begining with the design and ending with coding and testing.

\image html WorkflowTimeline.png width=800cm

@section ss_Aiming Software Design
The software is divided into the 'mastermind' aiming protocol, which steps through the
various phases of the program. It remains to be determined if this will be performed 
by a separate file or the cotask.py setup given in class. This protocol interfaces 
between the motors, thermal camera, and firing controls described in the following 
subsections.

\image html FSM_Aiming.png width=800cm

@subsection ss_motor Motor FSM
The Motor FSM describes the behavior of both the yaw and pitch motors (though each acts 
independantly of one another). This FSM simply waits for a target position and when 
given a position, moves to that position and holds. This will be accomplished by 
implementing a PI controller.

\image html FSM_Motor.png width=800cm

@subsection ss_camera Thermal Camera FSM
The thermal camera FSM describes the behavior of the interface with the thermal camera.
The system will retrieve data from the thermal camera to specify the target motor 
positions, and will not retrieve data while the system is on standby.

\image html FSM_ThermalCamera.png width=800cm

@subsection ss_firing Firing FSM
The firing FSM describes the behavior of the firing system, which waits until both 
motors are in position before activating the firing switches on our nerf gun.

\image html FSM_Firing.png width=800cm

'''