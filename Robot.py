from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

class Robot:
    def __init__(self, left_motor_port, right_motor_port):
        self.WHEEL_DIAMETER = 55.5
        self.AXLE_TRACK = 104

        self.ev3 = EV3Brick()

        self.left_motor = Motor(left_motor_port)
        self.right_motor = Motor(right_motor_port)
        self.wheels = DriveBase(left_motor, right_motor, WHEEL_DIAMETER, AXLE_TRACK)

    def move(self):
        wheels.straight(1000)

    def beep(self):
        ev3.speaker.beep()