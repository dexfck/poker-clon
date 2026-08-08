"""
Animated green felt vortex background shader effect using NumPy array manipulation for Pygame.
Recreates Balatro's hypnotizing green casino felt table background.
"""
import math
import numpy as np
import pygame
from settings import DESIGN_W, DESIGN_H, C


class VortexBackground:
    def __init__(self, width=DESIGN_W, height=DESIGN_H, scale_down=4):
        self.w = width
        self.h = height
        self.scale_down = scale_down
        self.sw = width // scale_down
        self.sh = height // scale_down

        x = np.linspace(-1.5, 1.5, self.sw)
        y = np.linspace(-1.0, 1.0, self.sh)
        self.xx, self.yy = np.meshgrid(x, y)
        self.r = np.sqrt(self.xx**2 + self.yy**2) + 0.001
        self.angle = np.arctan2(self.yy, self.xx)

        self.time = 0.0
        self.surface = pygame.Surface((self.sw, self.sh))
        self.scaled_surface = pygame.Surface((width, height))

        # Green felt table colors
        self.c1 = np.array(C.VORTEX_1)
        self.c2 = np.array(C.VORTEX_2)
        self.c3 = np.array(C.VORTEX_3)

    def set_colors(self, c1, c2, c3):
        self.c1 = np.array(c1, dtype=float)
        self.c2 = np.array(c2, dtype=float)
        self.c3 = np.array(c3, dtype=float)

    def update(self, dt):
        self.time += dt

    def draw(self, surface):
        t = self.time * 0.4
        
        swirl = self.angle + 2.0 * np.sin(self.r * 2.5 - t * 0.4)
        wave1 = np.sin(self.xx * 3.5 + swirl * 1.8 + t)
        wave2 = np.cos(self.yy * 3.5 - swirl * 2.2 + t * 0.9)
        v = (wave1 + wave2 + 2.0) / 4.0

        col = np.zeros((self.sh, self.sw, 3), dtype=np.uint8)
        mask1 = v < 0.5
        mask2 = ~mask1

        v1 = v * 2.0
        v2 = (v - 0.5) * 2.0

        for channel in range(3):
            ch1 = self.c1[channel] * (1.0 - v1) + self.c2[channel] * v1
            ch2 = self.c2[channel] * (1.0 - v2) + self.c3[channel] * v2
            channel_arr = np.where(mask1, ch1, ch2)
            col[:, :, channel] = np.clip(channel_arr * 255.0, 0, 255).astype(np.uint8)

        pygame.surfarray.blit_array(self.surface, np.transpose(col, (1, 0, 2)))
        pygame.transform.smoothscale(self.surface, (self.w, self.h), self.scaled_surface)
        surface.blit(self.scaled_surface, (0, 0))
