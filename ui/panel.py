"""
Balatro UI Panel container display module.
"""
import pygame
from settings import C


class Panel:
    @staticmethod
    def draw_panel(surface: pygame.Surface, rect: pygame.Rect,
                   bg_color=C.PANEL_BG, border_color=C.PANEL_BORDER,
                   radius=10, border_width=2):
        s = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
        # Solid uniform panel background
        pygame.draw.rect(s, bg_color, (0, 0, rect.width, rect.height), border_radius=radius)
        
        # Crisp border frame
        if border_width > 0:
            pygame.draw.rect(s, border_color, (0, 0, rect.width, rect.height), width=border_width, border_radius=radius)

        surface.blit(s, rect)
