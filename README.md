# ME 405 Term Project
This directory contains the code required to run turret using an mlx90640 thermal camera with an STM32 chip running micropython. The turret was built as the final term project for the mechatornics class at Cal Poly. The purpose of the design was to intergrate simulatious task execution with a custom mechanical design.

## Overview of Hardware
Our hardware consists of a fully automatic nerf rifle placed on a pivoting stand that rotate on a turn table. The rifle is held upside down by the railing at the top of the rifle. 3D printed parts are bolted to a plate that is connected to a stand. The stand allows the plate to rotate in the pitch direction. The plate rotates through a belt that is attached to a motor. The motor is attached to the same turntable that the stand is on, ensuring that the motor and the stand are always in the same orientation.

For the yaw control, the motors is attached to the outside of the turntable. The turntable has teeth on the perimeter, allowing it to interact with the turntable. The wires are conncted through the middle of the table. The wires are long enough that the orientation of the stand does not effect the connection between the microcontroller and the motor.

The thermal camera is mounted to the base of the turn table, ensuring that it is always facing the same position, not matter how the gun rotates. This is due to the rules of the competition that this turret competed in. Since we do not need to hit a moving target, we only need to know where our target after at a certain moment.

The microcontroller and the breadboard for firing the gun are attached to the same turntable as the stand.

## Overview of Software
Our software preforms three main jobs, controlling the motors, determine where the target is from the camera, and timing the firing with motors to ensure it is only fired at a certain point. The camera only begin firing after 5 seconds have passed, since this it when the target will stop moving. The rifle will only fire once the motors indicate that they are withing a certain tolerance of the target. More indepth overview of our code can be found at (INSERT DOXYGEN LINK HERE)

## Results
Due to quality of parts and time constrains, our physical system did not preform as well as intended. Due to our gears for the pitch control being too weak, we could not control the pitch of the gun accurately. This meant that our final design did not have any pitch control. The mosfets we were using for our firing mechanism lost power during our testing, resulting in our firing mechanism also failing. The only part of our design that performed adequately was the yaw accuracy. The turret was able to reach it's desired location, which was determined by the thermal camera, almost every time.