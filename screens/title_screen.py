"""
Balatro Title Screen with interactive floating cards and animated press prompt.
"""
import math
import pygame
from ui.button import Button
from settings import DESIGN_W, DESIGN_H, C


class TitleScreen:
    def __init__(self, manager, game_state):
        self.manager = manager
        self.state = game_state
        self.time = 0.0

        self.btn_play = Button(
            DESIGN_W // 2 - 100, DESIGN_H // 2 + 120, 200, 50,
            "JUGAR", bg_color=C.BTN_RED, hover_color=C.BTN_RED_HI,
            font_size=32, callback=lambda: self.manager.change_screen("main_menu")
        )

    def on_enter(self):
        self.time = 0.0

    def update(self, dt: float, mouse_pos: tuple[int, int]):
        self.time += dt
        self.btn_play.update(dt, mouse_pos)

    def handle_event(self, event: pygame.event.Event):
        self.btn_play.handle_event(event)

    def draw(self, surface: pygame.Surface, asset_mgr):
        # Draw Balatro logo with floating sine wave offset
        logo = asset_mgr.logo
        if logo:
            lw, lh = logo.get_size()
            float_y = math.sin(self.time * 2.5) * 12.0
            cx = DESIGN_W // 2 - lw // 2
            cy = DESIGN_H // 2 - lh // 2 - 60 + int(float_y)
            
            # Logo drop shadow
            shadow = logo.copy()
            shadow.fill((0, 0, 0, 140), special_flags=pygame.BLEND_RGBA_MULT)
            surface.blit(shadow, (cx + 6, cy + 6))
            surface.blit(logo, (cx, cy))
        else:
            font_title = asset_mgr.font(80)
            txt = font_title.render("BALATRO", True, C.WHITE)
            surface.blit(txt, (DESIGN_W // 2 - txt.get_width() // 2, 200))

        # Floating interactive Ace of Spades card with full base background
        cw, ch = 120, 160
        card_surf = pygame.Surface((cw, ch), pygame.SRCALPHA)
        
        base_template = asset_mgr.enhancers[1] if (asset_mgr.enhancers and len(asset_mgr.enhancers) > 1) else None
        if base_template:
            scaled_bg = pygame.transform.smoothscale(base_template, (cw, ch))
            card_surf.blit(scaled_bg, (0, 0))
        else:
            pygame.draw.rect(card_surf, C.CARD_WHITE, (0, 0, cw, ch), border_radius=8)
            pygame.draw.rect(card_surf, (200, 200, 210), (0, 0, cw, ch), width=2, border_radius=8)

        card_ace = asset_mgr.get_card(3, 12, (cw, ch))
        if card_ace:
            card_surf.blit(card_ace, (0, 0))

        card_angle = math.sin(self.time * 1.8) * 8.0
        card_y = DESIGN_H // 2 - 190 + math.cos(self.time * 2.0) * 10.0

        # Drop shadow
        shadow_surf = pygame.Surface((cw, ch), pygame.SRCALPHA)
        pygame.draw.rect(shadow_surf, (0, 0, 0, 90), (0, 0, cw, ch), border_radius=8)
        rot_shadow = pygame.transform.rotate(shadow_surf, card_angle)
        shadow_rect = rot_shadow.get_rect(center=(DESIGN_W // 2 + 5, int(card_y) + 6))
        surface.blit(rot_shadow, shadow_rect)

        # Rotated card
        rotated_card = pygame.transform.rotate(card_surf, card_angle)
        card_rect = rotated_card.get_rect(center=(DESIGN_W // 2, int(card_y)))
        surface.blit(rotated_card, card_rect)

        self.btn_play.draw(surface, asset_mgr.font(28))

        # Subtitle prompt
        font_sub = asset_mgr.font(20)
        blink = (math.sin(self.time * 4.0) + 1.0) / 2.0
        alpha_val = int(120 + blink * 135)
        sub_sf = font_sub.render("Presiona JUGAR para iniciar una partida", True, C.L_GREY)
        sub_sf.set_alpha(alpha_val)
        surface.blit(sub_sf, (DESIGN_W // 2 - sub_sf.get_width() // 2, DESIGN_H - 60))
