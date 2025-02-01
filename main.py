import pygame
import sys
import random

from states.intro import Intro
from states.tutorial import Tutorial
from states.menu import Menu
from states.game import Game
from states.levels import Levels
from states.end import End
from states.transition import Transition

from src.utils import Utils

class Main(object):
    def __init__(self) -> None:
        pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=512)
        pygame.init()

        self.MONITOR_SIZE = (pygame.display.Info().current_w, pygame.display.Info().current_h)

        self.SCREEN_W, self.SCREEN_H = Utils.read_settings("resolution")
        self.SCREEN = pygame.display.set_mode((self.SCREEN_W, self.SCREEN_H), flags=pygame.RESIZABLE)
        self.SCREEN_C = (self.SCREEN_W / 2, self.SCREEN_H / 2)
        self.CLOCK = pygame.time.Clock()
        self.DISPLAY = pygame.Surface((self.SCREEN_W, self.SCREEN_H), flags=pygame.SRCALPHA)

        self.fullscreen = False

        pygame.display.set_caption("Floppy Sticks - Intro")
        pygame.display.set_icon(pygame.image.load("assets/images/icon.png"))

        pygame.mixer.music.load("assets/music/Context Sensitive - Overgrowth.mp3")
        pygame.mixer.music.set_volume(0.4)
        self.toggle_music(Utils.read_settings(key="music"))

        self.sound = Utils.read_settings(key="sound")

        self.screen_shake = {
            "intensity": 0,
            "duration": 0,
            "active": False}

        self.notification = {
            "x": 0,
            "y": 0,
            "w": 0,
            "h": 0,
            "destination": 0,
            "time": 0,
            "text_surface": None,
            "text_rect": None,
            "active": False}

        self.fonts = {
            "general": pygame.font.Font("assets/fonts/oswald.ttf", 25),
            "title": pygame.font.Font("assets/fonts/pressstart2p.ttf", 35),
            "notification": pygame.font.Font("assets/fonts/audiowide.ttf", 18)}

        self.images = {
                    "restart_button": pygame.image.load("assets/images/buttons/restart_button.png"),
                    "compass_button": pygame.image.load("assets/images/buttons/compass_button.png")}

        self.sounds = {
            "click": pygame.mixer.Sound("assets/sounds/click.wav"),
            "explosion": pygame.mixer.Sound("assets/sounds/explosion.wav"),
            "notification": pygame.mixer.Sound("assets/sounds/notification.wav"),
            "hover": pygame.mixer.Sound("assets/sounds/hover.wav")}

        self.cursors = {
            "arrow": pygame.SYSTEM_CURSOR_ARROW,
            "hand": pygame.SYSTEM_CURSOR_HAND}

        self._events = {}

        self._states = {
            "intro": Intro(self),
            "tutorial": Tutorial(self),
            "menu": Menu(self),
            "game": Game(self),
            "levels": Levels(self),
            "end": End(self),
            "transition": Transition(self)}

        self._state = "intro"

        self.render_notification("Initializing...")

    def events(self) -> None:
        self._events.clear()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.shutdown()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self._events["mousebuttondown"] = event

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self._events["keydown-r"] = True

                if event.key == pygame.K_F11:
                    self.fullscreen = not self.fullscreen

                    old_screen_w = self.SCREEN_W
                    old_screen_h = self.SCREEN_H

                    if self.fullscreen:
                        self.SCREEN_W = self.MONITOR_SIZE[0]
                        self.SCREEN_H = self.MONITOR_SIZE[1]
                        self.SCREEN = pygame.display.set_mode((self.SCREEN_W, self.SCREEN_H), flags=pygame.FULLSCREEN)
                    elif not self.fullscreen:
                        self.SCREEN_W, self.SCREEN_H = Utils.read_settings("resolution")
                        self.SCREEN = pygame.display.set_mode((self.SCREEN_W, self.SCREEN_H), flags=pygame.RESIZABLE)
                    self.SCREEN_C = (self.SCREEN_W / 2, self.SCREEN_H / 2)
                    self.DISPLAY = pygame.Surface((self.SCREEN_W, self.SCREEN_H), flags=pygame.SRCALPHA)
                    self.reposition(self.SCREEN_W - old_screen_w, self.SCREEN_H - old_screen_h)

            if event.type == pygame.VIDEORESIZE:
                if not self.fullscreen:
                    old_screen_w = self.SCREEN_W
                    old_screen_h = self.SCREEN_H

                    self.SCREEN_W = event.w
                    self.SCREEN_H = event.h
                    self.SCREEN_C = (self.SCREEN_W / 2, self.SCREEN_H / 2)
                    self.SCREEN = pygame.display.set_mode((self.SCREEN_W, self.SCREEN_H), flags=pygame.RESIZABLE)
                    self.DISPLAY = pygame.Surface((self.SCREEN_W, self.SCREEN_H), flags=pygame.SRCALPHA)

                    Utils.write_settings("resolution", [self.SCREEN_W, self.SCREEN_H])

                    self.reposition(self.SCREEN_W - old_screen_w, self.SCREEN_H - old_screen_h)

    def update(self) -> None:
        self._states[self._state].update(self._events, mouse_pos=pygame.mouse.get_pos())
        self._states["transition"].update()

        if self.notification["active"] == True:
            self.notification["x"] += (self.notification["destination"] - self.notification["x"]) * 0.1
            if min(self.notification["x"] - self.notification["destination"], 1) != 1:
                self.notification["time"] -= self.CLOCK.get_time()
                if self.notification["time"] <= 0:
                    self.notification["destination"] = self.SCREEN_W
            if self.notification["time"] <= 0 and min(self.notification["destination"] - self.notification["x"], 1) != 1:
                self.notification["active"] = False
            self.notification["text_rect"] = self.notification["text_surface"].get_rect(center=(self.notification["x"] + self.notification["w"] / 1.8, self.notification["y"] + self.notification["h"] / 2))

        if self.screen_shake["active"]:
            if self.screen_shake["duration"] > 0:
                self.screen_shake["duration"] -= 1
            else:
                self.screen_shake["active"] = False

    def render(self) -> None:
        self.DISPLAY.fill((0, 0, 0, 40))

        if self.notification["active"]:
            points = (
                (self.notification["x"], self.notification["y"]),
                (self.notification["x"] + self.notification["w"], self.notification["y"]),
                (self.notification["x"] + self.notification["w"] + self.notification["w"] / 8, self.notification["y"] + self.notification["h"]),
                (self.notification["x"] + self.notification["w"] / 8, self.notification["y"] + self.notification["h"]))
            pygame.draw.polygon(self.DISPLAY, (255, 255, 255), points, width=2)

            self.DISPLAY.blit(self.notification["text_surface"], self.notification["text_rect"])

        self._states[self._state].render(self.DISPLAY)
        self._states["transition"].render(self.DISPLAY)

        self.render_text(self.DISPLAY, f"FPS: {int(self.CLOCK.get_fps())}", 10, 50, render_centerx=False, render_centery=False)

        display_offset = [0, 0]

        if self.screen_shake["active"]:
            display_offset[0] += random.randint(-self.screen_shake["intensity"][0], self.screen_shake["intensity"][0])
            display_offset[1] += random.randint(-self.screen_shake["intensity"][1], self.screen_shake["intensity"][1])

        self.SCREEN.blit(self.DISPLAY, display_offset)

        pygame.display.update()

    def loop(self) -> None:
        while True:
            self.events()
            self.update()
            self.render()
            self.CLOCK.tick(75)

    def toggle_music(self, value: bool) -> None:
        if value:
            Utils.write_settings("music", True)
            pygame.mixer.music.play(-1)
        elif not value:
            Utils.write_settings("music", False)
            pygame.mixer.music.fadeout(1000)

    def toggle_sound(self, value: bool) -> None:
        if value:
            Utils.write_settings("sound", True)
            self.sound = True
        elif not value:
            self.sound = False
            Utils.write_settings("sound", False)

    def play_sound(self, sound: str) -> None:
        if self.sound:
            self.sounds[sound].play()

    def screenshake(self, intensity=[2, 2], duration=20) -> None:
        self.screen_shake["intensity"] = intensity
        self.screen_shake["duration"] = duration
        self.screen_shake["active"] = True

    def switch_cursor(self, cursor: int) -> None:
        if pygame.mouse.get_cursor()[0] != cursor:
            pygame.mouse.set_cursor(cursor)

    def set_caption(self, caption: str) -> None:
        pygame.display.set_caption("Floppy Sticks" + " - " + caption)

    def render_notification(self, text: str, milliseconds=2000):
        if self.notification["active"]:
            return

        text_surface = self.fonts["notification"].render(text, True, (255, 255, 255))

        self.notification["w"] = text_surface.get_width() * 1.2
        self.notification["h"] = text_surface.get_height()
        self.notification["x"] = self.SCREEN_W
        self.notification["y"] = self.SCREEN_H - self.notification["h"] - 30

        self.notification["destination"] = self.SCREEN_W - text_surface.get_width() * 1.4
        self.notification["time"] = milliseconds

        self.notification["text_surface"] = text_surface.copy()
        self.notification["text_rect"] = text_surface.get_rect(center=(self.notification["x"] + self.notification["w"] / 1.8, self.notification["y"] + self.notification["h"] / 2))
        self.notification["active"] = True

        self.play_sound("notification")

    def render_text(self, surface: pygame.Surface, text: str, x: int | float, y: int | float, font="general", render_centerx=True, render_centery=True, offset_3D=[0, 0]) -> None:
        for i, line in enumerate(text.split("\n")):
            text_surface = self.fonts[font].render(line, True, (255, 255, 255))
            text_surface_3D = self.fonts[font].render(line, True, (120, 120, 120))

            match render_centerx, render_centery:
                case True, True:
                    text_rect = text_surface.get_rect(center=(x, y + text_surface.get_height() * i))
                case True, False:
                    text_rect = text_surface.get_rect(centerx=x, top=y + text_surface.get_height() * i)
                case False, True:
                    text_rect = text_surface.get_rect(left=x, centery=y + text_surface.get_height() * i)
                case False, False:
                    text_rect = text_surface.get_rect(topleft=(x, y + text_surface.get_height() * i))

            text_rect_3D = text_rect.copy()
            text_rect_3D.x += offset_3D[0]
            text_rect_3D.y -= offset_3D[1]

            surface.blit(text_surface_3D, text_rect_3D)
            surface.blit(text_surface, text_rect)

    def transition_to(self, state: str, setup=True, speed=2) -> None:
        if not self._states["transition"].active:
            if setup:
                self._states[state].setup()
            self._states["transition"].setup()
            self._states["transition"].speed = speed
            self._states["transition"].active = True
            self._states["transition"].endstate = state

    def reposition(self, surface_diffx: int | float, surface_diffy: int | float) -> None:
        self.transition_to(self._state, setup=False, speed=25)
        self.notification["x"] += surface_diffx
        self.notification["y"] += surface_diffy
        self.notification["destination"] += surface_diffx
        self._states[self._state].reposition(surface_diffx, surface_diffy)
        self._states["transition"].reposition()

    def shutdown(self) -> None:
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    Main().loop()
