"""
Pantalla de Victoria / Victory Screen.
"""
import pygame
from ui.button import Button
from ui.panel import Panel
from settings import DESIGN_W, DESIGN_H, C


class WinScreen:
    def __init__(self, manager, game_state):
        self.manager = manager
        self.state = game_state

        self.btn_new_run = Button(
            DESIGN_W // 2 - 120, DESIGN_H // 2 + 80, 240, 50,
            "NUEVA PARTIDA", bg_color=C.BTN_GREEN, hover_color=C.BTN_GREEN_HI,
            font_size=24, callback=self.start_new_run
        )
        self.btn_menu = Button(
            DESIGN_W // 2 - 120, DESIGN_H // 2 + 145, 240, 45,
            "MENÚ PRINCIPAL", bg_color=C.PANEL_LIGHT, hover_color=C.PANEL_BORDER,
            font_size=22, callback=lambda: self.manager.change_screen("main_menu")
        )

        self.buttons = [self.btn_new_run, self.btn_menu]

    def start_new_run(self):
        self.state.reset_run(0)
        self.manager.change_screen("blind_select")

    def on_enter(self):
        pass

    def update(self, dt: float, mouse_pos: tuple[int, int]):
        for btn in self.buttons:
            btn.update(dt, mouse_pos)

    def handle_event(self, event: pygame.event.Event):
        for btn in self.buttons:
            btn.handle_event(event)

    def draw(self, surface: pygame.Surface, asset_mgr):
        panel_rect = pygame.Rect(DESIGN_W // 2 - 210, DESIGN_H // 2 - 170, 420, 390)
        Panel.draw_panel(surface, panel_rect, bg_color=C.PANEL_DARK, border_color=C.MONEY_GOLD, border_width=3)

        font_h = asset_mgr.font(44)
        txt = font_h.render("¡VICTORIA!", True, C.MONEY_GOLD)
        surface.blit(txt, (DESIGN_W // 2 - txt.get_width() // 2, DESIGN_H // 2 - 140))

        font_sub = asset_mgr.font(20)
        t_sub = font_sub.render("¡Has completado con éxito la partida!", True, C.WHITE)
        surface.blit(t_sub, (DESIGN_W // 2 - t_sub.get_width() // 2, DESIGN_H // 2 - 85))

        font_body = asset_mgr.font(20)
        t_ante = font_body.render(f"Antes Superados: 8 / 8", True, C.CHIPS_BLUE)
        t_money = font_body.render(f"Dinero Final: ${self.state.dollars}", True, C.MONEY_GOLD)
        t_jokers = font_body.render(f"Comodines: {len(self.state.jokers)}", True, C.MULT_RED)

        surface.blit(t_ante, (DESIGN_W // 2 - t_ante.get_width() // 2, DESIGN_H // 2 - 45))
        surface.blit(t_money, (DESIGN_W // 2 - t_money.get_width() // 2, DESIGN_H // 2 - 15))
        surface.blit(t_jokers, (DESIGN_W // 2 - t_jokers.get_width() // 2, DESIGN_H // 2 + 15))

        for btn in self.buttons:
            btn.draw(surface, asset_mgr.font(22))
