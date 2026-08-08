"""
Animated score/chip/mult numbers counter that rolls smoothly between values with color pops.
Supports centered rendering inside bounding boxes.
"""
import pygame
from settings import C


class AnimatedCounter:
    def __init__(self, x: int = 0, y: int = 0, value=0, color=C.WHITE, font_size=28, label=""):
        self.x = x
        self.y = y
        self.target_val = value
        self.curr_val = float(value)
        self.color = color
        self.font_size = font_size
        self.label = label
        self.flash_timer = 0.0

    def set_target(self, val: int):
        if val != self.target_val:
            self.target_val = val
            self.flash_timer = 0.35

    def update(self, dt: float):
        if self.flash_timer > 0:
            self.flash_timer -= dt
        
        diff = self.target_val - self.curr_val
        if abs(diff) > 0.01:
            self.curr_val += diff * min(dt * 14.0, 1.0)
        else:
            self.curr_val = float(self.target_val)

    def draw(self, surface: pygame.Surface, font, center_rect: pygame.Rect = None):
        display_str = f"{self.label}{int(self.curr_val):,}"
        col = C.WHITE if self.flash_timer > 0 else self.color
        
        txt_sf = font.render(display_str, True, col)
        txt_sh = font.render(display_str, True, (0, 0, 0, 160))

        if center_rect:
            cx = center_rect.centerx - txt_sf.get_width() // 2
            cy = center_rect.centery - txt_sf.get_height() // 2
        else:
            cx, cy = self.x, self.y

        surface.blit(txt_sh, (cx + 2, cy + 2))
        surface.blit(txt_sf, (cx, cy))
