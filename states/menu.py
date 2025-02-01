from states.state import State

from src.point import Point
from src.particle import BackgroundParticle
from src.utils import Utils

from math import sin, radians, sqrt
from random import randint, choice

from pygame import Surface
from pygame.draw import aaline

class Menu(State):
    def setup(self) -> None:
        self.points = [
            Point(self.manager.SCREEN_C[0], self.manager.SCREEN_C[1], "clickable"),
            Point(self.manager.SCREEN_C[0], self.manager.SCREEN_C[1] + 40, "clickable"),
            Point(self.manager.SCREEN_C[0], self.manager.SCREEN_C[1] + 80, "clickable"),
            Point(self.manager.SCREEN_C[0], self.manager.SCREEN_C[1] + 120, "clickable" if Utils.read_settings(key="music") else "static"),
            Point(self.manager.SCREEN_C[0], self.manager.SCREEN_C[1] + 160, "clickable" if Utils.read_settings(key="sound") else "static"),
            Point(self.manager.SCREEN_C[0] - 40, self.manager.SCREEN_C[1] + 120, "static" if Utils.read_settings(key="music") else "clickable"),
            Point(self.manager.SCREEN_C[0] - 40, self.manager.SCREEN_C[1] + 160, "static" if Utils.read_settings(key="sound") else "clickable")]

        self.lables = [
            ["-  Play", self.manager.SCREEN_C[0] + 30, self.manager.SCREEN_C[1]],
            ["-  Level", self.manager.SCREEN_C[0] + 30, self.manager.SCREEN_C[1] + 40],
            ["-  Docs", self.manager.SCREEN_C[0] + 30, self.manager.SCREEN_C[1] + 80],
            ["-  Music", self.manager.SCREEN_C[0] + 30, self.manager.SCREEN_C[1] + 120],
            ["-  Sound", self.manager.SCREEN_C[0] + 30, self.manager.SCREEN_C[1] + 160]]

        self.background_particles = []

        self.title_y = 80
        self.title_speed = 0

    def update(self, events: dict, **kwargs) -> None:
        if events.get("mousebuttondown"):
            for i, point in enumerate(self.points):
                if point.collide(events["mousebuttondown"].pos):
                    if point.state == "clickable":
                        match i:
                            case 0 | 1 | 2:
                                point.switch_state("dynamic")
                            case 3:
                                point.switch_state("static")
                                self.points[5].switch_state("clickable")
                                self.manager.toggle_music(False)
                            case 5:
                                point.switch_state("static")
                                self.points[3].switch_state("clickable")
                                self.manager.toggle_music(True)
                            case 4:
                                point.switch_state("static")
                                self.points[6].switch_state("clickable")
                                self.manager.toggle_sound(False)
                            case 6:
                                point.switch_state("static")
                                self.points[4].switch_state("clickable")
                                self.manager.toggle_sound(True)
                        self.manager.play_sound("click")

        if randint(0, 20) == 0:
            if randint(0, 1) == 0:
                x = randint(0, self.manager.SCREEN_W - 10)
                y = choice((0, self.manager.SCREEN_H - 10))
            else:
                x = choice((0, self.manager.SCREEN_W - 10))
                y = randint(0, self.manager.SCREEN_H)
            BackgroundParticle.spawn(self.background_particles, x, y, radius=(1, 2), amount=1)

        BackgroundParticle.update_particles(self.background_particles, (self.manager.SCREEN_W, self.manager.SCREEN_H))

        collision = False
        for point in self.points:
            if point.state != "static" and point.collide(kwargs["mouse_pos"]):
                collision = True
                break

        if collision:
            self.manager.switch_cursor(self.manager.cursors["hand"])
        else:
            self.manager.switch_cursor(self.manager.cursors["arrow"])

        for point in self.points:
            point.update()
            if point.state == "dynamic":
                match self.points.index(point):
                    case 0:
                        self.manager.transition_to("game")
                    case 1:
                        self.manager.transition_to("levels")
                    case 2:
                        self.manager.transition_to("tutorial")

        self.title_speed += 1
        self.title_y += sin(radians(self.title_speed)) * 0.8

    def render(self, surface: Surface) -> None:
        BackgroundParticle.render_particles(self.background_particles, surface)

        for particle_a in self.background_particles:
            for particle_b in self.background_particles[self.background_particles.index(particle_a) + 1:]:
                dx = particle_a.x - particle_b.x
                dy = particle_a.y - particle_b.y
                if sqrt(dx * dx + dy * dy) < 150:
                    aaline(surface, particle_a.color, (particle_a.x, particle_a.y), (particle_b.x, particle_b.y))

        for point in self.points:
            point.render(surface)

        for label in self.lables:
            self.manager.render_text(surface, label[0], label[1], label[2], render_centerx=False)

        self.manager.render_text(surface, "Floppy Sticks", self.manager.SCREEN_C[0], self.title_y, font="title", offset_3D=[3, 3])

    def reposition(self, surface_diffx: int | float, surface_diffy: int | float) -> None:
        for point in self.points:
            point.move(surface_diffx / 2, surface_diffy / 2)
        for label in self.lables:
            label[1] += surface_diffx / 2
            label[2] += surface_diffy / 2
