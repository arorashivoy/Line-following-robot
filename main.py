from gpiozero import Robot, LineSensor, Motor
from signal import pause
from time import sleep


###############################################################################
# Global Vars
###############################################################################
# found_line = False

###############################################################################
# Pins
###############################################################################
# Motor pins
LEFT_FORWARD_PIN = 8
LEFT_BACKWARD_PIN = 7
LEFT_ENABLE_PIN = 25

RIGHT_FORWARD_PIN = 9
RIGHT_BACKWARD_PIN = 10
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

leftMotor = Motor(LEFT_FORWARD_PIN, LEFT_BACKWARD_PIN, enable=LEFT_ENABLE_PIN, pwm=True)
rightMotor = Motor(RIGHT_FORWARD_PIN, RIGHT_BACKWARD_PIN, enable=RIGHT_ENABLE_PIN, pwm=True)

robot = Robot(leftMotor, rightMotor)


###############################################################################
# Helper functions
###############################################################################
def move(s1, s2, s3, s4, s5):
    global found_line
    found_line = found_line or s2 == 0 or s3 == 0 or s4 == 0
    # found_line = found_line or s1 == 0 or s2 == 0 or s3 == 0 or s4 == 0 or s5 == 0
    if not found_line:
        robot.right()
    if s3 == 0:
        robot.forward(speed=0.5)
    elif s4 == 0:
        robot.forward(speed=0.5, curve_right=1)
    elif s2 == 0:
        robot.forward(speed=0.5, curve_left=1)
    # elif s5 == 0:
    #     robot.forward(speed=0.2, curve_right=1)
    # elif s1 == 0:
    #     robot.forward(speed=0.2, curve_left=1)
    else:
        # robot.forward(speed=0.2)
        robot.stop()


###############################################################################
# Main loop
###############################################################################
if __name__ == "__main__":
    found_line = False
    found_line = found_line or S2.value == 0 or S3.value == 0 or S4.value == 0
    while not found_line:
        robot.right()
        sleep(0.01)
        found_line = found_line or S2.value == 0 or S3.value == 0 or S4.value == 0

    while True:
        move(S1.value, S2.value, S3.value, S4.value, S5.value)
        # print(S1.value, S2.value, S3.value, S4.value, S5.value)
        sleep(0.01)

