from pygame.draw import line
from pygame import Surface

from math import dist, sqrt

from .point import Point

class Stick(object):
    def __init__(self, point1: Point, point2: Point) -> None:
        self.point1 = point1
        self.point2 = point2
        self.length = round(dist((point1.x, point1.y), (point2.x, point2.y)), 2)

    def update(self) -> None:
        distx = self.point1.x - self.point2.x
        disty = self.point1.y - self.point2.y

        distance = sqrt(distx * distx + disty * disty)
        difference = self.length - distance

        try:
            percent = difference / distance / 2
        except ZeroDivisionError:
            percent = 0

        offsetx = distx * percent
        offsety = disty * percent

        if self.point1.state == "dynamic":
            self.point1.x += offsetx
            self.point1.y += offsety
        if self.point2.state == "dynamic":
            self.point2.x -= offsetx
            self.point2.y -= offsety

    def render(self, surface: Surface) -> None:
        line(surface, (150, 150, 150), (self.point1.x, self.point1.y), (self.point2.x, self.point2.y), width=5)
