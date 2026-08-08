"""
Subtle Retro CRT Post-Processing Filter for Pygame.
Includes low-intensity scanlines, gentle RGB shift, and minimal glass frame.
"""
import math
import numpy as np
import pygame
from settings import DESIGN_W, DESIGN_H


class CRTFilter:
    def __init__(self, width=DESIGN_W, height=DESIGN_H):
        self.w = width
        self.h = height
        self.enabled = True
        self.time = 0.0

        # -------------------------------------------------------------------
        # 1. Low-Intensity Scanline Overlay (Subtle 3px spacing)
        # -------------------------------------------------------------------
        self.scanline_surf = pygame.Surface((width, height), pygame.SRCALPHA)
        for y in range(0, height, 3):
            pygame.draw.line(self.scanline_surf, (0, 0, 0, 18), (0, y), (width, y), 1)

        # -------------------------------------------------------------------
        # 2. Minimal CRT Bezel & Subtle Edge Shadow
        # -------------------------------------------------------------------
        self.bezel_surf = pygame.Surface((width, height), pygame.SRCALPHA)
        
        inner_margin = 4
        inner_rect = pygame.Rect(inner_margin, inner_margin, width - inner_margin * 2, height - inner_margin * 2)

        self.bezel_surf.fill((0, 0, 0, 255))
        pygame.draw.rect(self.bezel_surf, (0, 0, 0, 0), inner_rect, border_radius=14)
        
        # Subtle inner vignette border
        pygame.draw.rect(self.bezel_surf, (0, 0, 0, 25), inner_rect, width=6, border_radius=14)

    def update(self, dt: float):
        self.time += dt

    def apply(self, surface: pygame.Surface):
        if not self.enabled:
            return surface

        # -------------------------------------------------------------------
        # A) Subtle Chromatic Aberration (1px shift)
        # -------------------------------------------------------------------
        try:
            arr = pygame.surfarray.pixels3d(surface)
            arr[:, :, 0] = np.roll(arr[:, :, 0], -1, axis=0)
            arr[:, :, 2] = np.roll(arr[:, :, 2], 1, axis=0)
            del arr
        except Exception:
            pass

        # -------------------------------------------------------------------
        # B) Scanline & Bezel overlays
        # -------------------------------------------------------------------
        surface.blit(self.scanline_surf, (0, 0))
        surface.blit(self.bezel_surf, (0, 0))
        return surface
