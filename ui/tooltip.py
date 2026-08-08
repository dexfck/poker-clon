"""
Tooltip component module.
"""
import pygame
from settings import C, DESIGN_W, DESIGN_H


class Tooltip:
    def __init__(self):
        self.active = False
        self.title = ""
        self.desc = ""
        self.x = 0
        self.y = 0

    def show(self, title: str, desc: str, x: int, y: int):
        self.title = title
        self.desc = desc
        self.x = x
        self.y = y
        self.active = True

    def hide(self):
        self.active = False

    def draw(self, surface: pygame.Surface, font_title, font_body):
        if not self.active or not self.title:
            return

        w = 200
        h = 80
        tx = min(self.x + 15, DESIGN_W - w - 10)
        ty = min(self.y + 15, DESIGN_H - h - 10)

        tooltip_surf = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(tooltip_surf, C.PANEL_DARK, (0, 0, w, h), border_radius=8)
        pygame.draw.rect(tooltip_surf, C.ORANGE, (0, 0, w, h), width=2, border_radius=8)

        t_title = font_title.render(self.title, True, C.MONEY_GOLD)
        tooltip_surf.blit(t_title, (10, 8))

        words = self.desc.split()
        lines = []
        curr_line = ""
        for word in words:
            test_line = f"{curr_line} {word}".strip()
            if font_body.size(test_line)[0] < w - 20:
                curr_line = test_line
            else:
                lines.append(curr_line)
                curr_line = word
        if curr_line:
            lines.append(curr_line)

        cy = 30
        for line in lines[:3]:
            t_line = font_body.render(line, True, C.L_GREY)
            tooltip_surf.blit(t_line, (10, cy))
            cy += 16

        surface.blit(tooltip_surf, (tx, ty))
