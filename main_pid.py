from gpiozero import Robot, LineSensor, Motor
from signal import pause
from time import sleep
from simple_pid import PID


###############################################################################
# Global Vars
###############################################################################
done = False
speed = 0.8
# speed = 1

# Initialize the PID controller
Kp = 5
Ki = 1
Kd = 40
pid = PID(Kp=Kp, Ki=Ki, Kd=Kd, setpoint=0)

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

leftMotor = Motor(LEFT_FORWARD_PIN, LEFT_BACKWARD_PIN, enable=LEFT_ENABLE_PIN, pwm=True)
rightMotor = Motor(RIGHT_FORWARD_PIN, RIGHT_BACKWARD_PIN, enable=RIGHT_ENABLE_PIN, pwm=True)

robot = Robot(leftMotor, rightMotor)


###############################################################################
# Helper functions
###############################################################################
def move(s1, s2, s3, s4, s5):
    global done, speed

    # Calculate the error based on sensor values
    error = (s1 * -10 + s2 * -20 + s3 * 0 + s4 * 20 + s5 * 10)

    # Compute the correction using the PID controller
    correction = pid(error)

    # Normalize the correction to be between 0 and 1
    correction = max(min(correction, 1), -1)

    # # Apply the correction to the robot's movement
    # if s2 == 0 and s3 == 0 and s4 == 0:
    #     robot.forward(speed=speed)
    # else:
    #     curve_left = abs(correction) if correction > 0 else 0
    #     curve_right = abs(correction) if correction < 0 else 0
    #     # print(f"Curve Left: {curve_left}, Curve Right: {curve_right}")
    #     robot.forward(speed=speed, curve_left=curve_left, curve_right=curve_right)

    curve_left = abs(correction) if correction < 0 else 0
    curve_right = abs(correction) if correction > 0 else 0
    # print(f"Curve Left: {curve_left}, Curve Right: {curve_right}")
    robot.forward(speed=speed, curve_left=curve_left, curve_right=curve_right)


    # Stop the robot if no sensors are active
    if s1 == 1 and s2 == 1 and s3 == 1 and s4 == 1 and s5 == 1:
        done = True
        robot.stop()


###############################################################################
# Main loop
###############################################################################
if __name__ == "__main__":
    found_line = False
    found_line = found_line or S1.value == 0 or S2.value == 0 or S3.value == 0 or S4.value == 0 or S5.value == 0
    while not found_line:
        robot.right(speed=0.5)
        sleep(0.01)
        found_line = found_line or S2.value == 0 or S3.value == 0 or S4.value == 0

    while True:
        if (done):
            print("Done")
            break
        move(S1.value, S2.value, S3.value, S4.value, S5.value)
        # print(S1.value, S2.value, S3.value, S4.value, S5.value)
        # sleep(0.01)

