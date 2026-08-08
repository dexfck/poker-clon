"""
Collection Screen displaying discovered Jokers, Tarots, Planets, Spectrals, and Vouchers in a grid.
"""
import pygame
from ui.button import Button
from ui.panel import Panel
from ui.tooltip import Tooltip
from settings import DESIGN_W, DESIGN_H, C, JOKER_NAMES


class CollectionScreen:
    def __init__(self, manager, game_state):
        self.manager = manager
        self.state = game_state
        self.tooltip = Tooltip()
        self.active_tab = "Jokers"

        self.btn_back = Button(
            40, 40, 100, 40, "BACK", bg_color=C.PANEL_LIGHT,
            hover_color=C.PANEL_BORDER, font_size=20,
            callback=lambda: self.manager.change_screen("main_menu")
        )

        self.btn_tab_jokers = Button(
            DESIGN_W // 2 - 200, 100, 120, 36, "JOKERS",
            bg_color=C.BTN_BLUE, hover_color=C.BTN_BLUE_HI, font_size=18,
            callback=lambda: self.set_tab("Jokers")
        )
        self.btn_tab_tarots = Button(
            DESIGN_W // 2 - 70, 100, 120, 36, "TAROTS",
            bg_color=C.BTN_ORANGE, hover_color=C.BTN_ORANGE_HI, font_size=18,
            callback=lambda: self.set_tab("Tarots")
        )
        self.btn_tab_vouchers = Button(
            DESIGN_W // 2 + 60, 100, 120, 36, "VOUCHERS",
            bg_color=C.BTN_GREEN, hover_color=C.BTN_GREEN_HI, font_size=18,
            callback=lambda: self.set_tab("Vouchers")
        )

        self.buttons = [self.btn_back, self.btn_tab_jokers, self.btn_tab_tarots, self.btn_tab_vouchers]

    def set_tab(self, tab_name: str):
        self.active_tab = tab_name

    def on_enter(self):
        pass

    def update(self, dt: float, mouse_pos: tuple[int, int]):
        for btn in self.buttons:
            btn.update(dt, mouse_pos)

    def handle_event(self, event: pygame.event.Event):
        for btn in self.buttons:
            btn.handle_event(event)

    def draw(self, surface: pygame.Surface, asset_mgr):
        font_h = asset_mgr.font(36)
        txt = font_h.render("COLLECTION", True, C.WHITE)
        surface.blit(txt, (DESIGN_W // 2 - txt.get_width() // 2, 40))

        # Main grid display panel
        panel_rect = pygame.Rect(100, 150, DESIGN_W - 200, DESIGN_H - 190)
        Panel.draw_panel(surface, panel_rect, bg_color=C.PANEL_DARK)

        # Draw grid items according to tab
        rows, cols = 4, 10
        card_w, card_h = 50, 70
        start_x, start_y = 130, 170
        spacing_x, spacing_y = 90, 110

        font_label = asset_mgr.font(12)

        for r in range(rows):
            for c in range(cols):
                idx = r * cols + c
                x = start_x + c * spacing_x
                y = start_y + r * spacing_y

                if self.active_tab == "Jokers" and idx < len(asset_mgr.jokers):
                    j_img = asset_mgr.get_joker(idx, (card_w, card_h))
                    if j_img:
                        surface.blit(j_img, (x, y))
                        lbl = font_label.render(JOKER_NAMES[idx][:8] if idx < len(JOKER_NAMES) else f"#{idx}", True, C.L_GREY)
                        surface.blit(lbl, (x, y + card_h + 2))
                elif self.active_tab == "Tarots" and idx < len(asset_mgr.tarots):
                    t_img = asset_mgr.get_tarot(idx, (card_w, card_h))
                    if t_img:
                        surface.blit(t_img, (x, y))
                elif self.active_tab == "Vouchers" and idx < len(asset_mgr.vouchers):
                    v_img = asset_mgr.get_voucher(idx, (card_w, card_h))
                    if v_img:
                        surface.blit(v_img, (x, y))

        for btn in self.buttons:
            btn.draw(surface, asset_mgr.font(18))
