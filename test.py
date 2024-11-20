#! /usr/bin/env python3

from gpiozero import Robot, LineSensor, Motor, LED
from signal import pause
from time import sleep

###############################################################################
# Pins
###############################################################################
# Motor pins
LEFT_FORWARD_PIN = 7
LEFT_BACKWARD_PIN = 8
LEFT_ENABLE_PIN = 25

RIGHT_FORWARD_PIN = 10
RIGHT_BACKWARD_PIN = 9
RIGHT_ENABLE_PIN = 11

# Line sensor pins
S1_PIN = 17
S2_PIN = 18
S3_PIN = 27
S4_PIN = 22
S5_PIN = 23

###############################################################################
# Initialize the Robot
###############################################################################
S1 = LineSensor(S1_PIN)
S2 = LineSensor(S2_PIN)
S3 = LineSensor(S3_PIN)
S4 = LineSensor(S4_PIN)
S5 = LineSensor(S5_PIN)

# S1.when_line = lambda: print('Line detected 1')
# S2.when_line = lambda: print('Line detected 2')
# S3.when_line = lambda: print('Line detected 3')
# S4.when_line = lambda: print('Line detected 4')
# S5.when_line = lambda: print('Line detected 5')
#
# S1.when_no_line = lambda: print('No 1')
# S2.when_no_line = lambda: print('No 2')
# S3.when_no_line = lambda: print('No 3')
# S4.when_no_line = lambda: print('No 4')
# S5.when_no_line = lambda: print('No 5')

leftMotor = Motor(LEFT_FORWARD_PIN, LEFT_BACKWARD_PIN, enable=LEFT_ENABLE_PIN, pwm=True)
rightMotor = Motor(RIGHT_FORWARD_PIN, RIGHT_BACKWARD_PIN, enable=RIGHT_ENABLE_PIN, pwm=True)

robot = Robot(leftMotor, rightMotor)
# robot = Robot(left=(LEFT_FORWARD_PIN, LEFT_BACKWARD_PIN), right=(RIGHT_FORWARD_PIN, RIGHT_BACKWARD_PIN))


###############################################################################
# Helper functions
###############################################################################
def move(s1, s2, s3, s4, s5):
    # print(s1, s2, s3, s4, s5)
    # if s3 == 1:
    #     robot.forward()
    # elif s2 == 1:
    #     robot.left()
    # elif s4 == 1:
    #     robot.right()
    # elif s1 == 1:
    #     robot.left()
    # elif s5 == 1:
    #     robot.right()
    # else:
    #     robot.forward()
    #

    # robot.forward(speed=0.5)
    # print(1)
    # sleep(2)
    # robot.forward(speed=1)
    # print(2)
    # sleep(2)
    # robot.right()
    # print(3)
    # sleep(2)
    # robot.backward()
    # print(4)
    # sleep(2)
    # robot.left()
    # print(5)
    # sleep(2)

    print('forward')
    robot.forward(speed=0.5)
    sleep(1)

    print('right')
    robot.forward(speed=0.5, curve_right=1)
    sleep(1)

    print('left')
    robot.forward(speed=0.5, curve_left=1)
    sleep(1)

    print('stop')
    robot.stop()
    sleep(1)

    pass

###############################################################################
# Main loop
###############################################################################
if __name__ == "__main__":
    while True:
        move(S1.value, S2.value, S3.value, S4.value, S5.value)
        sleep(0.1)

