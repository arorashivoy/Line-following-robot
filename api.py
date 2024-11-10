from fastapi import FastAPI
from gpiozero import Robot, LineSensor, Motor
from signal import pause
from time import sleep
from math import cos, degrees, pow, sqrt

###############################################################################
# Showing colors in print
###############################################################################
class Colors:
    BOLD = "\033[1m"
    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    GREEN = "\033[0;32m"
    YELLOW = "\033[0;33m"
    BLUE = "\033[0;34m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    WHITE = "\033[0;37m"
    RESET = "\033[0m"

###############################################################################
# Global Vars
###############################################################################
app = FastAPI()
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
@app.get("/move/{x}/{y}/{angle}")
async def move(x: float, y: float, angle: float):
    x = x / 100
    y = y / 100

    # Calculating the speed
    speed = max(min(sqrt(pow(x, 2) + pow(y, 2)), 1), 0)

    print(Colors.GREEN + Colors.BOLD + f"x: {x}, y: {y}, speed: {speed}" + Colors.RESET)

    # Forward or backward
    if y > 0:
        if x < 0:
            robot.forward(speed=speed, curve_left=abs(x))
        elif x > 0:
            robot.forward(speed=speed, curve_right=abs(x))
        else:
            robot.forward(speed=speed)
    elif y < 0:
        if x < 0:
            robot.backward(speed=speed, curve_left=abs(x))
        elif x > 0:
            robot.backward(speed=speed, curve_right=abs(x))
        else:
            robot.backward(speed=speed)
    else:
        robot.stop()
    
    return {"x": x, "y": y}

# ###############################################################################
# # Main loop
# ###############################################################################
# if __name__ == "__main__":
#     found_line = False
#     found_line = found_line or S2.value == 0 or S3.value == 0 or S4.value == 0
#     while not found_line:
#         robot.right()
#         sleep(0.01)
#         found_line = found_line or S2.value == 0 or S3.value == 0 or S4.value == 0
#
#     while True:
#         move(S1.value, S2.value, S3.value, S4.value, S5.value)
#         # print(S1.value, S2.value, S3.value, S4.value, S5.value)
#         sleep(0.01)
#


@app.get("/")
async def root():
    return {"message": "Hello World"}
