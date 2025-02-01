from pygame import Surface, SRCALPHA

from states.state import State

class Transition(State):
    def setup(self) -> None:
        self.image = Surface((self.manager.SCREEN_W, self.manager.SCREEN_H), flags=SRCALPHA)
        self.alpha = 0
        self.speed = 2
        self.active = False
        self.endstate = None

    def update(self) -> None:
        if self.active:
            self.image.fill((50, 50, 50, self.alpha))
            self.alpha += self.speed
            if self.alpha >= 250:
                self.speed = -5
                self.manager._state = self.endstate
                self.manager.set_caption(self.endstate.capitalize())
            elif self.alpha <= 0:
                self.active = False

    def render(self, surface: Surface) -> None:
        if self.active:
            surface.blit(self.image, (0, 0))

    def reposition(self) -> None:
        self.image = Surface((self.manager.SCREEN_W, self.manager.SCREEN_H), flags=SRCALPHA)
