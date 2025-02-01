from states.state import State

from src.utils import Utils

from pygame import Surface

class End(State):
    def setup(self) -> None:
        self.credits = Utils.read_credits()
        self.y = self.manager.SCREEN_H

    def update(self, events: dict, **kwargs) -> None:
        self.y -= 0.5
        if self.y < self.manager.SCREEN_C[1] - 200:
            self.manager.transition_to("menu")

    def render(self, surface: Surface) -> None:
        self.manager.render_text(surface, self.credits, self.manager.SCREEN_C[0], self.y, font="notification")
