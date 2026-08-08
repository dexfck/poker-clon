"""
Screen Manager controlling active screen state and smooth cross-fade transitions.
"""
import pygame


class ScreenManager:
    def __init__(self):
        self.screens = {}
        self.active_screen_key = None
        self.previous_screen_key = None
        self.active_screen = None
        self.fade_alpha = 0.0
        self.fade_target = 0.0
        self.pending_key = None

    def register(self, key: str, screen):
        self.screens[key] = screen

    def change_screen(self, key: str):
        if key in self.screens:
            if self.active_screen_key and self.active_screen_key != key:
                self.previous_screen_key = self.active_screen_key
            self.pending_key = key
            self.fade_target = 255.0

    def set_screen_immediate(self, key: str):
        if key in self.screens:
            self.active_screen_key = key
            self.active_screen = self.screens[key]
            self.active_screen.on_enter()

    def update(self, dt: float, mouse_pos: tuple[int, int]):
        if self.fade_target > 0 and self.pending_key:
            self.fade_alpha += dt * 800.0
            if self.fade_alpha >= 255.0:
                self.fade_alpha = 255.0
                self.active_screen_key = self.pending_key
                self.active_screen = self.screens[self.pending_key]
                self.active_screen.on_enter()
                self.pending_key = None
                self.fade_target = 0.0
        elif self.fade_alpha > 0:
            self.fade_alpha -= dt * 800.0
            if self.fade_alpha < 0:
                self.fade_alpha = 0.0

        if self.active_screen:
            self.active_screen.update(dt, mouse_pos)

    def handle_event(self, event: pygame.event.Event):
        if self.active_screen:
            self.active_screen.handle_event(event)

    def draw(self, surface: pygame.Surface, asset_mgr):
        if self.active_screen:
            self.active_screen.draw(surface, asset_mgr)

        if self.fade_alpha > 0:
            overlay = pygame.Surface((surface.get_width(), surface.get_height()))
            overlay.fill((0, 0, 0))
            overlay.set_alpha(int(self.fade_alpha))
            surface.blit(overlay, (0, 0))
