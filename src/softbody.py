from pygame import Surface

from .point import Point
from .stick import Stick

from math import cos, sin, pi

class SoftBody(object):
    def __init__(self, gravity=0.2, friction=0.999) -> None:
        self.gravity = gravity
        self.friction = friction
        self.points = []
        self.sticks = []
        self.static = []
        self.dynamic = []
        self.clickable = []

    def move(self, velx: int | float, vely: int | float) -> None:
        for point in self.points:
            point.x += velx
            point.y += vely
            point.lastx += velx
            point.lasty += vely

    def load_model(self, model: dict, offset: list | tuple) -> None:
        self.points.clear()
        self.sticks.clear()

        self.static.clear()
        self.dynamic.clear()
        self.clickable.clear()

        for index, angle, length, state in model["points"]:
            try:
                x = self.points[index].x
                y = self.points[index].y
            except IndexError:
                x, y = offset

            x += cos(-angle * pi / 180) * length
            y += sin(-angle * pi / 180) * length

            self.add_point(x, y, state)

        for stick in model["sticks"]:
            self.add_stick(self.points[stick[0]], self.points[stick[1]])

        self.static = [self.points[i] for i in model["static"]]
        self.dynamic = [self.points[i] for i in model["dynamic"]]
        self.clickable = [self.points[i] for i in model["clickable"]]

    def add_point(self, x: int | float, y: int | float, state: str) -> None:
        self.points.append(Point(x, y, state, gravity=self.gravity, friction=self.friction))

    def add_stick(self, point1: Point, point2: Point) -> None:
        self.sticks.append(Stick(point1, point2))

    def update_points(self) -> None:
        self.static.clear()
        self.dynamic.clear()
        self.clickable.clear()

        for point in self.points:
            match point.state:
                case "static":
                    self.static.append(point)
                case "dynamic":
                    self.dynamic.append(point)
                case "clickable":
                    self.clickable.append(point)
            point.update()

    def update_sticks(self) -> None:
        for _ in range(2):
            for stick in self.sticks:
                stick.update()

    def render_points(self, surface: Surface) -> None:
        for point in self.points:
            point.render(surface)

    def render_sticks(self, surface: Surface) -> None:
        for stick in self.sticks:
            stick.render(surface)

    def collide(self, position: list | tuple, points: list) -> list:
        collisions = []
        for point in points:
            if point.collide(position):
                collisions.append(point)
        return collisions
