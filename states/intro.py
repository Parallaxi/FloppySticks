from states.state import State

from src.point import Point
from src.utils import Utils

from pygame import Surface

class Intro(State):
    def setup(self) -> None:
        self.point = Point(self.manager.SCREEN_C[0], self.manager.SCREEN_C[1], "clickable")
        self.show_tutorial = Utils.read_settings("tutorial")

    def update(self, events: dict, **kwargs) -> None:
        if events.get("mousebuttondown"):
            if self.point.collide(events["mousebuttondown"].pos):
                if self.point.collide(events["mousebuttondown"].pos):
                    self.point.switch_state("dynamic")
                    self.manager.play_sound("click")

        if self.point.collide(kwargs["mouse_pos"]):
            self.manager.switch_cursor(self.manager.cursors["hand"])
        else:
            self.manager.switch_cursor(self.manager.cursors["arrow"])

        self.point.update()

        if self.point.state == "dynamic":
            Utils.write_settings("tutorial", False)
            self.manager.transition_to("tutorial" if self.show_tutorial else "menu")

    def render(self, surface: Surface) -> None:
        self.point.render(surface)
        self.manager.render_text(surface, "These types of circles\nare clickable", self.manager.SCREEN_C[0], self.manager.SCREEN_C[1] - 70)

    def reposition(self, surface_diffx: int | float, surface_diffy: int | float) -> None:
        self.point.move(surface_diffx / 2, surface_diffy / 2)
