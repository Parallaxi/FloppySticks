from states.state import State

from src.softbody import SoftBody
from src.button import Button
from src.particle import ExplosionParticle, BackgroundParticle
from src.utils import Utils

from random import randint, choice
from math import sqrt

from pygame import Surface
from pygame.draw import aaline

class Game(State):
    def setup(self) -> None:
        self.softbody = SoftBody()
        self.levels = Utils.read_models("models")
        self.current_level = Utils.read_settings(key="current_level")
        self.end_level = Utils.read_settings(key="end_level")
        self.load_level(self.current_level)

        self.explosion_particles = []
        self.background_particles = []

        self.buttons = [
            Button("compass", 10, 10, self.manager.images["compass_button"]),
            Button("restart", 10, self.manager.SCREEN_H - 42, self.manager.images["restart_button"])]

        self.next = False
        self.restart = False

    def next_level(self) -> None:
        self.current_level += 1
        if self.current_level >= len(self.levels):
            self.current_level = 0
        self.softbody.load_model(self.levels[self.current_level], (self.manager.SCREEN_C[0], self.manager.SCREEN_C[1] / 1.5))
        if self.current_level > self.end_level:
            self.end_level = self.current_level
            Utils.write_settings("end_level", self.end_level)
        Utils.write_settings("current_level", self.current_level)
        self.manager.render_notification(f"Next up - {self.current_level}")

    def load_level(self, level: int) -> None:
        self.softbody.load_model(self.levels[level], (self.manager.SCREEN_C[0], self.manager.SCREEN_C[1] / 1.5))

    def restart_level(self) -> None:
        self.softbody.load_model(self.levels[self.current_level], (self.manager.SCREEN_C[0], self.manager.SCREEN_C[1] / 1.5))
        self.manager.render_notification(f"Restarted - {self.current_level}")

    def update(self, events: dict, **kwargs) -> None:
        if events.get("mousebuttondown"):
            for point in self.softbody.clickable:
                if point.collide(events["mousebuttondown"].pos):
                    point.switch_state("dynamic")
                    self.manager.play_sound("click")

            for button in self.buttons:
                if button.collide(events["mousebuttondown"].pos):
                    match button.name:
                        case "compass":
                            self.manager.transition_to("menu")
                        case "restart":
                            self.restart = True
                    self.manager.play_sound("click")

        if events.get("keydown-r"):
            self.levels = Utils.read_models("models")
            self.restart_level()

        for button in self.buttons:
            if button.collide(kwargs["mouse_pos"]):
                if button.image.get_alpha() != 180:
                    button.image.set_alpha(180)
                    self.manager.play_sound("hover")
                    break
            else:
                if button.image.get_alpha() != 255:
                    button.image.set_alpha(255)

        if randint(0, 20) == 0:
            if randint(0, 1) == 0:
                x = randint(0, self.manager.SCREEN_W - 10)
                y = choice((0, self.manager.SCREEN_H - 10))
            else:
                x = choice((0, self.manager.SCREEN_W - 10))
                y = randint(0, self.manager.SCREEN_H)
            BackgroundParticle.spawn(self.background_particles, x, y, radius=(1, 2), amount=1)

        BackgroundParticle.update_particles(self.background_particles, (self.manager.SCREEN_W, self.manager.SCREEN_H))
        ExplosionParticle.update_particles(self.explosion_particles, (self.manager.SCREEN_W, self.manager.SCREEN_H))

        if Button.collide_array(kwargs["mouse_pos"], self.buttons) or self.softbody.collide(kwargs["mouse_pos"], self.softbody.clickable):
            self.manager.switch_cursor(self.manager.cursors["hand"])
        else:
            self.manager.switch_cursor(self.manager.cursors["arrow"])

        self.softbody.update_points()
        self.softbody.update_sticks()

        if not self.restart:
            for point in self.softbody.dynamic:
                collisions = point.collide_points(self.softbody.static)
                for collision in collisions:
                    ExplosionParticle.spawn(self.explosion_particles, collision.x, collision.y, amount=50)
                    collision.switch_state("dynamic")
                    self.manager.screenshake()
                    self.manager.play_sound("explosion")

            for point in self.softbody.dynamic:
                collisions = point.collide_points(self.softbody.clickable)
                for collision in collisions:
                    collision.switch_state("dynamic")
                    self.manager.screenshake()

        if len(self.softbody.points) == len(self.softbody.dynamic):
            self.next = True
        elif len(self.softbody.static) > 0 and len(self.softbody.clickable) == 0:
            self.restart = True

        if self.next:
            if self.current_level >= len(self.levels) - 1:
                self.manager.transition_to("end", speed=1)
            self.manager.transition_to("game", setup=False)
            if self.manager._states["transition"].alpha >= 250:
                self.next_level()
                self.next = False

        elif self.restart:
            self.manager.transition_to("game", setup=False, speed=5)
            if self.manager._states["transition"].alpha >= 250:
                self.restart_level()
                self.restart = False

    def render(self, surface: Surface) -> None:
        BackgroundParticle.render_particles(self.background_particles, surface)
        ExplosionParticle.render_particles(self.explosion_particles, surface)

        for particle_a in self.background_particles:
            for particle_b in self.background_particles[self.background_particles.index(particle_a) + 1:]:
                dx = particle_a.x - particle_b.x
                dy = particle_a.y - particle_b.y
                if sqrt(dx * dx + dy * dy) < 150:
                    aaline(surface, particle_a.color, (particle_a.x, particle_a.y), (particle_b.x, particle_b.y))

        self.softbody.render_sticks(surface)
        self.softbody.render_points(surface)

        for button in self.buttons:
            button.render(surface)

        self.manager.render_text(surface, f"{self.current_level}/{len(self.levels) - 1}", self.manager.SCREEN_W - 40, 30)

    def reposition(self, surface_diffx: int | float, surface_diffy: int | float) -> None:
        self.softbody.move(surface_diffx / 2, surface_diffy / 3)
        for button in self.buttons:
            if button.name == "restart":
                button.y += surface_diffy
