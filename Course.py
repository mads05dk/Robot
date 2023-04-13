class Ball:
    def __init__(self, color, LOWER_COLOR, UPPER_COLOR, x, y):
        self.LOWER_COLOR = LOWER_COLOR
        self.UPPER_COLOR = UPPER_COLOR
        self.x = x
        self.y = y

    def __init__(self, x, y): # standard color constructor
        self.LOWER_COLOR = (0, 0, 255)
        self.UPPER_COLOR = (180, 255, 255)
        self.x = x
        self.y = y

    def __str__(self):
        return "Ball: " + "(" + str(self.x) + ", " + str(self.y) + ")"


class Course:
    def __init__(self):
        self.WIDTH_CM = 180
        self.HEIGTH_CM = 120
        self.BALL_DIAMETER_CM = 4
        self.ROWS = self.WIDTH_CM / self.BALL_DIAMETER_CM
        self.COLUMNS = self.HEIGTH_CM / self.BALL_DIAMETER_CM
        self.BALL_MINIMUM_MOVEMENT_CM = self.COLUMNS * 7 # 1 ball diameter, can be changed to make it more sensitive
        self.balls = []

    def __str__(self):
        return "Course: " + str(self.WIDTH_CM) + "x" + str(self.HEIGTH_CM) + "cm, " + str(self.ROWS) + "x" + str(self.COLUMNS) + " cells, " + str(self.BALL_DIAMETER_CM) + "cm ball diameter, " + str(self.BALL_MINIMUM_MOVEMENT_CM) + "cm minimum ball movement"

    def print_balls(self):
        print("There are " + str(len(self.balls)) + " balls on the course:")
        for ball in self.balls:
            print(ball)

    def add_ball(self, ball):
        self.balls.append(ball)

    def ball_seen_at(self, x, y):
        if self.__ball_is_not_close_to_any_previously_detected_ball(Ball(x, y)):
            self.add_ball(Ball(x, y))
            return True

    def __ball_is_not_close_to_any_previously_detected_ball(self, ball):
        for other_ball in self.balls:
            if self.__ball_is_close_to_ball(ball, other_ball):
                return False
        return True

    def __update_ball(self, ball, x, y):
        ball.x = x
        ball.y = y

    def __ball_is_close_to_ball(self, ball, other_ball):
        if abs(ball.x - other_ball.x) < self.BALL_MINIMUM_MOVEMENT_CM and abs(ball.y - other_ball.y) < self.BALL_MINIMUM_MOVEMENT_CM:
            self.__update_ball(other_ball, ball.x, ball.y)
            return True
        return False