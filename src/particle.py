from pygame.draw import circle
from pygame import Surface, Color

from random import uniform

class Particle(object):
    def __init__(self, x: int | float, y: int | float, radius: int, color: Color, velx=0, vely=0) -> None:
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.velx = velx
        self.vely = vely

    def update(self) -> None:
        pass

    def render(self, surface: Surface) -> None:
        pass

    @staticmethod
    def update_particles(array: list, screen_size: list | tuple) -> None:
        for i, particle in sorted(enumerate(array), reverse=True):
            particle.update()
            if particle.color.a <= 0 or (particle.x < -particle.radius) or (particle.y < -particle.radius) or (particle.x > screen_size[0] - particle.radius) or (particle.y > screen_size[1] - particle.radius):
                array.pop(i)

    @staticmethod
    def render_particles(array: list, surface: Surface) -> None:
        for particle in array:
            particle.render(surface)

    @classmethod
    def spawn(cls, array: list, x: int | float, y: int | float, radius=(1, 3), amount=30) -> None:
        array.extend([cls(x, y, uniform(radius[0], radius[1])) for _ in range(amount)])

class ExplosionParticle(Particle):
    def __init__(self, x: int | float, y: int | float, radius: int) -> None:
        super().__init__(x, y, radius, Color(255, 0, 130, 250), velx=uniform(-2.0, 2.0), vely=uniform(-2.0, 2.0))

    def update(self) -> None:
        self.x += self.velx
        self.y += self.vely
        self.color.a -= 2
        self.vely += 0.1

    def render(self, surface: Surface) -> None:
        circle(surface, self.color, (self.x, self.y), self.radius)

class BackgroundParticle(Particle):
    def __init__(self, x: int | float, y: int | float, radius: int) -> None:
        super().__init__(x, y, radius, Color(100, 100, 100), velx=uniform(0.1, 2.0) if x == 0 else uniform(-2.0, -0.1), vely=uniform(0.1, 3.0) if y == 0 else uniform(-2.0, -0.1))

    def update(self) -> None:
        self.x += self.velx
        self.y += self.vely

    def render(self, surface: Surface) -> None:
        circle(surface, self.color, (self.x, self.y), self.radius)
