from pygame import Surface

class Button(object):
    def __init__(self, name: str, x: int | float, y: int | float, image: Surface) -> None:
        self.name = name
        self.x = x
        self.y = y
        self.image = image
        self.image_3D = image.copy()
        self.image_3D.set_alpha(120)

    def render(self, surface: Surface) -> None:
        surface.blit(self.image_3D, (self.x + 3, self.y - 3))
        surface.blit(self.image, (self.x, self.y))

    def collide(self, position: list | tuple) -> bool:
        return self.image.get_rect(topleft=(self.x, self.y)).collidepoint(position)

    @staticmethod
    def collide_array(position: list | tuple, buttons: list) -> list:
        collisions = []
        for button in buttons:
            if button.collide(position):
                collisions.append(button)
        return collisions
