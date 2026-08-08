"""
JokerSprite visual component for displaying active Jokers in the Joker row or shop.
Draws card base template, Joker sprite, rarity border, and drop shadow.
"""
import pygame
from ui.ui_element import UIElement
from entities.joker import JokerBase as Joker
from settings import CARD_DISPLAY_W, CARD_DISPLAY_H, C


class JokerSprite(UIElement):
    RARITY_COLORS = {
        'Common': C.COMMON,
        'Uncommon': C.UNCOMMON,
        'Rare': C.RARE,
        'Legendary': C.LEGENDARY
    }

    def __init__(self, x: int, y: int, joker: Joker,
                 w=CARD_DISPLAY_W, h=CARD_DISPLAY_H):
        super().__init__(x, y, w, h)
        self.joker = joker

    def draw(self, surface: pygame.Surface, asset_mgr):
        if not self.visible:
            return

        w, h = self.rect.width, self.rect.height
        sw = int(w * self.scale)
        sh = int(h * self.scale)
        cx, cy = self.rect.center

        # Drop shadow
        shadow = pygame.Surface((sw, sh), pygame.SRCALPHA)
        pygame.draw.rect(shadow, (0, 0, 0, 80), (0, 0, sw, sh), border_radius=6)
        surface.blit(shadow, (cx - sw // 2 + 3, cy - sh // 2 + 4))

        # Base surface
        joker_base = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(joker_base, C.CARD_WHITE, (0, 0, w, h), border_radius=6)

        joker_surf = asset_mgr.get_joker(self.joker.sprite_idx, (w, h))
        if joker_surf:
            joker_base.blit(joker_surf, (0, 0))

        if self.scale != 1.0:
            rendered = pygame.transform.smoothscale(joker_base, (sw, sh))
        else:
            rendered = joker_base

        rect = rendered.get_rect(center=(cx, cy))
        surface.blit(rendered, rect)

        # Rarity border highlight
        border_col = self.RARITY_COLORS.get(self.joker.rarity_name, C.COMMON)
        border_surf = pygame.Surface((sw, sh), pygame.SRCALPHA)
        pygame.draw.rect(border_surf, border_col, (0, 0, sw, sh), width=2, border_radius=6)
        surface.blit(border_surf, rect)
