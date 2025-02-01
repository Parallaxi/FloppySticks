from states.state import State

from src.point import Point
from src.button import Button
from src.utils import Utils

from pygame import Surface

class Levels(State):
    def setup(self) -> None:
        self.current_level = Utils.read_settings(key="current_level")
        self.end_level = Utils.read_settings(key="end_level")

        self.points = []
        for y in range(60, 240, 60):
            for x in range(round(self.manager.SCREEN_C[0] - 180), round(self.manager.SCREEN_C[0] + 240), 60):
                if len(self.points) > self.end_level:
                    self.points.append(Point(x, y, "static"))
                else:
                    self.points.append(Point(x, y, "clickable"))

        self.buttons = [
            Button("compass", 10, 10, self.manager.images["compass_button"])]

    def update(self, events: dict, **kwargs) -> None:
        if events.get("mousebuttondown"):
            for point in self.points:
                if point.state == "clickable":
                    if point.collide(events["mousebuttondown"].pos):
                        point.switch_state("dynamic")
                        self.manager.play_sound("click")
            for button in self.buttons:
                if button.collide(events["mousebuttondown"].pos):
                    match button.name:
                        case "compass":
                            self.manager.transition_to("menu")
                    self.manager.play_sound("click")

        collision = False
        for point in self.points:
            if point.state != "static" and point.collide(kwargs["mouse_pos"]):
                collision = True
                break

        for button in self.buttons:
            if button.collide(kwargs["mouse_pos"]):
                if button.image.get_alpha() != 180:
                    button.image.set_alpha(180)
                    break
            else:
                if button.image.get_alpha() != 255:
                    button.image.set_alpha(255)

        if Button.collide_array(kwargs["mouse_pos"], self.buttons) or collision:
            self.manager.switch_cursor(self.manager.cursors["hand"])
        else:
            self.manager.switch_cursor(self.manager.cursors["arrow"])

        for point in self.points:
            point.update()

        for point in self.points:
            if point.state == "dynamic" and not self.manager._states["transition"].active:
                Utils.write_settings("current_level", self.points.index(point))
                self.manager.transition_to("game")

    def render(self, surface: Surface):
        for point in self.points:
            point.render(surface)

        for button in self.buttons:
            button.render(surface)

    def reposition(self, surface_diffx: int | float, surface_diffy: int | float):
        for point in self.points:
            point.move(surface_diffx / 2, 0)
