"""
CardSprite visual component for interactive playing cards.
Supports card base template background, suit/rank overlays, lift selection animation, hover bounce, and glowing halos.
"""
import pygame
from ui.ui_element import UIElement
from entities.card import Card
from settings import CARD_DISPLAY_W, CARD_DISPLAY_H, C


class CardSprite(UIElement):
    def __init__(self, x: int, y: int, card: Card,
                 w=CARD_DISPLAY_W, h=CARD_DISPLAY_H):
        super().__init__(x, y, w, h)
        self.card = card
        self.is_selected = False
        self.offset_y = 0.0
        self.target_offset_y = 0.0
    def get_hit_rect(self) -> pygame.Rect:
        r = self.rect.copy()
        r.y += int(self.offset_y)
        return r

    def update(self, dt: float, mouse_pos: tuple[int, int]):
        self.target_scale = 1.05 if (self.is_hovered and self.enabled) else 1.0
        self.scale += (self.target_scale - self.scale) * min(dt * 15.0, 1.0)
        self.target_offset_y = -26.0 if self.is_selected else (-10.0 if self.is_hovered else 0.0)
        self.offset_y += (self.target_offset_y - self.offset_y) * min(dt * 22.0, 1.0)

    def draw(self, surface: pygame.Surface, asset_mgr):
        if not self.visible:
            return

        w, h = self.rect.width, self.rect.height
        sw = int(w * self.scale)
        sh = int(h * self.scale)
        
        cx = self.rect.centerx
        cy = self.rect.centery + int(self.offset_y)

        # -------------------------------------------------------------------
        # 1. Base Card Surface (White rounded card with border)
        # -------------------------------------------------------------------
        card_base = pygame.Surface((w, h), pygame.SRCALPHA)
        
        # Use white card template from Enhancers (tile 0,1) if available, or crisp white rect
        base_template = asset_mgr.enhancers[1] if (asset_mgr.enhancers and len(asset_mgr.enhancers) > 1) else None
        if base_template:
            scaled_bg = pygame.transform.smoothscale(base_template, (w, h))
            card_base.blit(scaled_bg, (0, 0))
        else:
            pygame.draw.rect(card_base, C.CARD_WHITE, (0, 0, w, h), border_radius=6)
            pygame.draw.rect(card_base, (200, 200, 210), (0, 0, w, h), width=2, border_radius=6)

        # -------------------------------------------------------------------
        # 2. Suit & Rank Overlay or Card Back (if face down)
        # -------------------------------------------------------------------
        if getattr(self.card, 'is_face_down', False):
            card_back_img = asset_mgr.card_back if asset_mgr.card_back else None
            if card_back_img:
                overlay = pygame.transform.smoothscale(card_back_img, (w, h))
                card_base.blit(overlay, (0, 0))
            else:
                pygame.draw.rect(card_base, C.MULT_RED, (0, 0, w, h), border_radius=6)
        else:
            overlay = asset_mgr.get_card(self.card.suit_idx, self.card.rank_idx, (w, h))
            if overlay:
                card_base.blit(overlay, (0, 0))

        # Debuffed overlay (red mask and red X indicator)
        if getattr(self.card, 'debuffed', False):
            dark_mask = pygame.Surface((w, h), pygame.SRCALPHA)
            dark_mask.fill((120, 0, 0, 110))
            card_base.blit(dark_mask, (0, 0))
            pygame.draw.line(card_base, C.MULT_RED, (12, 12), (w - 12, h - 12), 4)
            pygame.draw.line(card_base, C.MULT_RED, (w - 12, 12), (12, h - 12), 4)

        # -------------------------------------------------------------------
        # 3. Card Drop Shadow
        # -------------------------------------------------------------------
        shadow_surf = pygame.Surface((sw, sh), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surf, (0, 0, 0, 90), (0, 0, sw, sh), border_radius=6)
        shadow_rect = shadow_surf.get_rect(center=(cx + 4, cy + 6))
        surface.blit(shadow_surf, shadow_rect)



        # -------------------------------------------------------------------
        # 5. Render final scaled card
        # -------------------------------------------------------------------
        if self.scale != 1.0:
            rendered_card = pygame.transform.smoothscale(card_base, (sw, sh))
        else:
            rendered_card = card_base

        card_rect = rendered_card.get_rect(center=(cx, cy))
        surface.blit(rendered_card, card_rect)
