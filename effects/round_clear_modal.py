"""
Round Clear / Cash Out Animated Overlay Modal for Balatro.
Features elastic drop-down entry, itemized bonus breakdown (reward, hands, discards, interest), and Cash Out button.
"""
import pygame
from ui.button import Button
from ui.panel import Panel
from effects.animations import Tween, ease_out_back
from settings import DESIGN_W, DESIGN_H, C


class RoundClearModal:
    def __init__(self, on_cash_out_cb):
        self.active = False
        self.anim_y = Tween(-400, DESIGN_H // 2 - 170, 0.5, ease_fn=ease_out_back)
        self.on_cash_out_cb = on_cash_out_cb
        
        self.base_reward = 3
        self.hands_bonus = 0
        self.discards_bonus = 0
        self.interest_bonus = 0
        self.total_earned = 0

        self.btn_cash_out = Button(
            DESIGN_W // 2 - 90, 0, 180, 48, "COBRAR",
            bg_color=C.BTN_GREEN, hover_color=C.BTN_GREEN_HI, font_size=24,
            callback=self.cash_out
        )

    def show(self, blind_reward=3, hands_left=0, discards_left=0, current_dollars=0):
        self.active = True
        self.anim_y.reset()
        
        # Calculate dynamic bonuses based on actual round stats
        self.base_reward = blind_reward
        self.hands_left = hands_left
        self.discards_left = discards_left
        self.hands_bonus = hands_left * 1
        self.discards_bonus = discards_left * 1
        self.interest_bonus = min(5, current_dollars // 5)
        self.total_earned = self.base_reward + self.hands_bonus + self.discards_bonus + self.interest_bonus

    def cash_out(self):
        self.active = False
        if self.on_cash_out_cb:
            self.on_cash_out_cb(self.total_earned)

    def update(self, dt: float, mouse_pos: tuple[int, int]):
        if not self.active:
            return

        curr_y = self.anim_y.update(dt)
        self.btn_cash_out.rect.y = int(curr_y) + 260
        self.btn_cash_out.update(dt, mouse_pos)

    def handle_event(self, event: pygame.event.Event) -> bool:
        if not self.active:
            return False
        return self.btn_cash_out.handle_event(event)

    def draw(self, surface: pygame.Surface, asset_mgr):
        if not self.active:
            return

        curr_y = int(self.anim_y.value)

        # Semi-transparent dark background backdrop
        dark_bg = pygame.Surface((DESIGN_W, DESIGN_H), pygame.SRCALPHA)
        dark_bg.fill((0, 0, 0, 150))
        surface.blit(dark_bg, (0, 0))

        # Main Modal Box
        modal_rect = pygame.Rect(DESIGN_W // 2 - 220, curr_y, 440, 330)
        Panel.draw_panel(surface, modal_rect, bg_color=C.PANEL_DARK, border_color=C.MONEY_GOLD, border_width=3)

        # Header Title
        font_h = asset_mgr.font(36)
        font_body = asset_mgr.font(20)
        font_bold = asset_mgr.font(26)

        t_title = font_h.render("¡CIEGA SUPERADA!", True, C.MONEY_GOLD)
        surface.blit(t_title, (modal_rect.centerx - t_title.get_width() // 2, curr_y + 20))

        # Divider line
        pygame.draw.line(surface, C.PANEL_BORDER, (modal_rect.x + 30, curr_y + 65), (modal_rect.right - 30, curr_y + 65), 2)

        # Breakdown lines
        lines = [
            ("Recompensa de ciega:", f"${self.base_reward}", C.WHITE),
            (f"Manos restantes ({self.hands_left}):", f"+${self.hands_bonus}", C.CHIPS_BLUE),
            (f"Descartes restantes ({self.discards_left}):", f"+${self.discards_bonus}", C.MULT_RED),
            ("Interes:", f"+${self.interest_bonus}", C.GREEN),
        ]

        cy = curr_y + 80
        for lbl, val, col in lines:
            t_lbl = font_body.render(lbl, True, C.L_GREY)
            t_val = font_body.render(val, True, col)
            surface.blit(t_lbl, (modal_rect.x + 40, cy))
            surface.blit(t_val, (modal_rect.right - 40 - t_val.get_width(), cy))
            cy += 28

        # Divider line
        pygame.draw.line(surface, C.PANEL_BORDER, (modal_rect.x + 30, cy + 5), (modal_rect.right - 30, cy + 5), 2)

        # Total Earned
        t_tot_lbl = font_bold.render("GANANCIA TOTAL:", True, C.WHITE)
        t_tot_val = font_bold.render(f"+${self.total_earned}", True, C.MONEY_GOLD)
        surface.blit(t_tot_lbl, (modal_rect.x + 40, cy + 15))
        surface.blit(t_tot_val, (modal_rect.right - 40 - t_tot_val.get_width(), cy + 15))

        # Cash Out Button
        self.btn_cash_out.draw(surface, asset_mgr.font(24))
