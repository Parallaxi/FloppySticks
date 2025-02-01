from states.state import State

from src.point import Point

from pygame import Surface
from pygame.draw import rect

class Tutorial(State):
    def setup(self) -> None:
        self.points = [
            Point(self.manager.SCREEN_C[0] - 300, self.manager.SCREEN_C[1] - 120, "clickable"),
            Point(self.manager.SCREEN_C[0] + 300, self.manager.SCREEN_C[1] + 40, "dynamic"),
            Point(self.manager.SCREEN_C[0] - 300, self.manager.SCREEN_C[1] + 200, "static")]

        self.lables = [
            ["First the clickable point, its spends most of its life static until clicked.\nOnce clicked it will convert itself into a dynamic point.\nClick this top one when you're done reading to continue....", self.manager.SCREEN_C[0] - 270, self.manager.SCREEN_C[1] - 120],
            ["The dynamic is probably the most simple of points, it\nisn't pinned in place and constantly wants to\nmove around.", self.manager.SCREEN_C[0] - 110, self.manager.SCREEN_C[1] + 40],
            ["Finally you've got the static point,\nby the name I'm sure you can guess what this one does.\nThe only way to get this one dynamic is to bump it with a dynamic point.", self.manager.SCREEN_C[0] - 270, self.manager.SCREEN_C[1] + 200],
            ["Tip: Press F11 to\nmake window fullscreen", self.manager.SCREEN_C[0] - 350, self.manager.SCREEN_C[1] + 50]]

        self.boxes = [
            [self.points[0].x - 30, self.points[0].y - 30, 580, 130],
            [self.points[1].x - 430, self.points[1].y - 30, 460, 130],
            [self.points[2].x - 30, self.points[2].y - 30, 600, 130]]

    def update(self, events: dict, **kwargs) -> None:
        if events.get("mousebuttondown"):
            if self.points[0].collide(events["mousebuttondown"].pos):
                self.points[0].switch_state("dynamic")
                self.manager.play_sound("click")

        if self.points[0].collide(kwargs["mouse_pos"]):
            self.manager.switch_cursor(self.manager.cursors["hand"])
        else:
            self.manager.switch_cursor(self.manager.cursors["arrow"])

        self.points[0].update()
        if self.points[0].state == "dynamic":
            self.manager.transition_to("menu")

    def render(self, surface: Surface) -> None:
        for point in self.points:
            point.render(surface)

        for label in self.lables:
            self.manager.render_text(surface, label[0], label[1], label[2], render_centerx=False)

        for box in self.boxes:
            rect(surface, (200, 200, 200), box, width=2)

        self.manager.render_text(surface, "There are 3 types of points (clickable, dynamic and static)\nYour job is to turn them all into dynamic points.", self.manager.SCREEN_C[0], self.manager.SCREEN_C[1] - 250, font="notification")

    def reposition(self, surface_diffx: int | float, surface_diffy: int | float) -> None:
        for point in self.points:
            point.move(surface_diffx / 2, surface_diffy / 2)
        for label in self.lables:
            label[1] += surface_diffx / 2
            label[2] += surface_diffy / 2
        for box in self.boxes:
            box[0] += surface_diffx / 2
            box[1] += surface_diffy / 2
