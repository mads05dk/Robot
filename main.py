#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, UltrasonicSensor
from pybricks.parameters import Port, Stop, Direction
from pybricks.tools import wait
from math import atan2, degrees, sqrt, cos, sin, radians
import time

# assumes robot start at 0,0 facing right
class Robot:
    def __init__(self):
        self.brick = EV3Brick()
        self.left_motor = Motor(Port.B)
        self.right_motor = Motor(Port.C)
        self.wheel_diameter = 70
        self.axle_track = 160
        self.wheels = DriveBase(self.left_motor, self.right_motor, wheel_diameter=self.wheel_diameter, axle_track=self.axle_track)

        # Set robot dimensions
        self.field_width = 1800 #cm
        self.field_height = 1200 #cm

        # Set initial position and orientation
        self.x = 0
        self.y = 0
        self.angle = 0

        # Set up odometry
        self.left_motor.reset_angle(0)
        self.right_motor.reset_angle(0)
        self.left_last_angle = 0
        self.right_last_angle = 0

    def move_to(self, x, y):
        # Get the current angles of the wheels
        left_angle = self.left_motor.angle()
        right_angle = self.right_motor.angle()

        # Compute the distances traveled by each wheel since the last call to move_to
        left_distance = (left_angle - self.left_last_angle) * self.wheel_diameter * 0.5 / 360
        right_distance = (right_angle - self.right_last_angle) * self.wheel_diameter * 0.5 / 360

        # Compute the average distance and heading of the robot
        distance = (left_distance + right_distance) * 0.5
        heading = self.angle + degrees((right_distance - left_distance) / self.axle_track)

        # Update the position of the robot based on the computed distance and heading
        self.x += distance * cos(radians(heading))
        self.y += distance * sin(radians(heading))
        self.angle = heading

        # Move the robot to the target position using the updated position and heading
        dx = x - self.x
        dy = y - self.y
        target_angle = degrees(atan2(dy, dx))

        # Calculate the shortest turn to face the target point
        delta_angle = target_angle - self.angle
        if delta_angle > 180:
            delta_angle -= 360
        elif delta_angle < -180:
            delta_angle += 360

        # Turn towards the target point
        self.wheels.turn(delta_angle)

        # Move forward to the target point
        distance = sqrt(dx ** 2 + dy ** 2)
        self.wheels.straight(distance)

        # Remember the current angles of the wheels for the next call to move_to
        self.left_last_angle = left_angle
        self.right_last_angle = right_angle

    def move_to_avoid(self, x, y):
        # Calculate the position of the cross
        cross_x = self.field_width / 2 - 100
        cross_y = self.field_height / 2 - 100
        
        # Calculate the distance between the robot and the cross
        dx = cross_x - self.x
        dy = cross_y - self.y
        distance_to_cross = sqrt(dx ** 2 + dy ** 2)
        
        # If the robot is on the left of the cross, move to the right side
        if self.x < cross_x:
            if self.y < cross_y:
                # Move to the top-right corner of the cross
                self.move_to(cross_x + 100, cross_y + 100)
            elif self.y > cross_y + 200:
                # Move to the bottom-right corner of the cross
                self.move_to(cross_x + 100, cross_y - 100)
            else:
                # Move to the right of the cross
                self.move_to(cross_x + 200, self.y)
        
        # If the robot is on the right of the cross, move to the left side
        elif self.x > cross_x + 200:
            if self.y < cross_y:
                # Move to the top-left corner of the cross
                self.move_to(cross_x - 100, cross_y + 100)
            elif self.y > cross_y + 200:
                # Move to the bottom-left corner of the cross
                self.move_to(cross_x - 100, cross_y - 100)
            else:
                # Move to the left of the cross
                self.move_to(cross_x - self.wheel_diameter, self.y)
        
        # If the robot is above or below the cross, move around it
        else:
            if self.y < cross_y:
                # Move to the top of the cross
                self.move_to(self.x, cross_y - self.wheel_diameter)
            else:
                # Move to the bottom of the cross
                self.move_to(self.x, cross_y + 200 + self.wheel_diameter)
        
        # Move to the desired (x, y) coordinate
        self.move_to(x, y)

    def get_wheels(self):
        return self.wheels

robot = Robot()

wait = 7.0
turn = 180


robot.move_to_avoid(1200, 1000) # move to the bottom middle
time.sleep(wait)