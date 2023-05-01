from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, UltrasonicSensor
from pybricks.parameters import Port, Stop, Direction
from pybricks.tools import wait
from math import atan2, degrees, sqrt

class Robot:
    def __init__(self):
        self.brick = EV3Brick()
        self.left_motor = Motor(Port.B)
        self.right_motor = Motor(Port.C)
        self.wheels = DriveBase(left_motor, right_motor, wheel_diameter=55.5, axle_track=104)

        # Set robot dimensions
        self.field_width = 4000
        self.field_height = 2000

        # Set initial position
        self.x = 0
        self.y = 0

    def move_to(self, x, y):
        dx = x - self.x
        dy = y - self.y
        angle = degrees(atan2(dy, dx))
        distance = sqrt(dx ** 2 + dy ** 2)

        # Turn towards the destination
        self.left_motor.run_angle(self.motor_speed, angle, Stop.BRAKE, False)
        self.right_motor.run_angle(-self.motor_speed, angle, Stop.BRAKE, True)

        # Move forward to the destination
        self.left_motor.run_angle(self.motor_speed, distance, Stop.BRAKE, False)
        self.right_motor.run_angle(self.motor_speed, distance, Stop.BRAKE, True)

        # Update current position
        self.x = x
        self.y = y

    def get_wheels():
        return self.wheels