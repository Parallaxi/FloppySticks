from pygame import Surface

class State(object):
    def __init__(self, manager) -> None:
        self.manager = manager
        self.setup()

    def setup(self) -> None:
        pass

    def update(self, events: dict, **kwargs) -> None:
        pass

    def render(self, surface: Surface) -> None:
        pass

    def reposition(self, surface_diffx: int | float, surface_diffy: int | float) -> None:
        pass
