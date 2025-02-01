from pygame.image import load
from pygame import Surface

from math import dist

class Point(object):
    def __init__(self, x: int | float, y: int | float, state: str, gravity=0.3, friction=0.999) -> None:
        self.x = x
        self.y = y
        self.lastx = x
        self.lasty = y
        self.state = state
        self.gravity = gravity
        self.friction = friction
        self.load_image()

    def move(self, velx: int | float, vely: int | float) -> None:
        self.x += velx
        self.y += vely
        self.lastx += velx
        self.lasty += vely

    def switch_state(self, state: str) -> None:
        self.state = state
        self.load_image()

    def load_image(self) -> None:
        self.image = load("assets/images/points/" + self.state + ".png")
        self.image_3D = self.image.copy()
        self.image_3D.set_alpha(120)

    def update(self) -> None:
        if self.state == "dynamic": 
            velx = (self.x - self.lastx) * self.friction
            vely = (self.y - self.lasty) * self.friction

            self.lastx = self.x
            self.lasty = self.y

            self.x += velx
            self.y += vely
            self.y += self.gravity

    def render(self, surface: Surface) -> None:
        surface.blit(self.image_3D, (self.x - 10 + 3, self.y - 10 - 3))
        surface.blit(self.image, (self.x - 10, self.y - 10))

    def collide(self, position: list | tuple) -> bool:
        return dist(position, (self.x, self.y)) <= 14

    def collide_points(self, points: list) -> list:
        collisions = []
        for point in points:
            if dist((self.x, self.y), (point.x, point.y)) <= 10:
                collisions.append(point)
        return collisions
