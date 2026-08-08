"""
Pantalla de Fin de Partida / Game Over.
"""
import pygame
from ui.button import Button
from ui.panel import Panel
from settings import DESIGN_W, DESIGN_H, C


class GameOverScreen:
    def __init__(self, manager, game_state, sound_manager=None):
        self.manager = manager
        self.state = game_state
        self.sound = sound_manager

        self.btn_new_run = Button(
            DESIGN_W // 2 - 120, DESIGN_H // 2 + 80, 240, 50,
            "NUEVA PARTIDA", bg_color=C.BTN_RED, hover_color=C.BTN_RED_HI,
            font_size=24, callback=self.start_new_run
        )
        self.btn_menu = Button(
            DESIGN_W // 2 - 120, DESIGN_H // 2 + 145, 240, 45,
            "MENU PRINCIPAL", bg_color=C.PANEL_LIGHT, hover_color=C.PANEL_BORDER,
            font_size=22, callback=lambda: self.manager.change_screen("main_menu")
        )

        self.buttons = [self.btn_new_run, self.btn_menu]

    def start_new_run(self):
        self.state.reset_run(0)
        self.manager.change_screen("blind_select")

    def on_enter(self):
        if self.sound:
            self.sound.play_game_over()

    def update(self, dt: float, mouse_pos: tuple[int, int]):
        for btn in self.buttons:
            btn.update(dt, mouse_pos)

    def handle_event(self, event: pygame.event.Event):
        for btn in self.buttons:
            btn.handle_event(event)

    def draw(self, surface: pygame.Surface, asset_mgr):
        panel_rect = pygame.Rect(DESIGN_W // 2 - 200, DESIGN_H // 2 - 160, 400, 380)
        Panel.draw_panel(surface, panel_rect, bg_color=C.PANEL_DARK, border_color=C.MULT_RED)

        font_h = asset_mgr.font(44)
        txt = font_h.render("FIN DE LA PARTIDA", True, C.MULT_RED)
        surface.blit(txt, (DESIGN_W // 2 - txt.get_width() // 2, DESIGN_H // 2 - 130))

        font_body = asset_mgr.font(22)
        t_ante = font_body.render(f"Ante alcanzado: {self.state.ante}", True, C.WHITE)
        t_score = font_body.render(f"Puntaje Final: {self.state.current_score:,}", True, C.MONEY_GOLD)

        surface.blit(t_ante, (DESIGN_W // 2 - t_ante.get_width() // 2, DESIGN_H // 2 - 50))
        surface.blit(t_score, (DESIGN_W // 2 - t_score.get_width() // 2, DESIGN_H // 2 - 15))

        for btn in self.buttons:
            btn.draw(surface, asset_mgr.font(22))
