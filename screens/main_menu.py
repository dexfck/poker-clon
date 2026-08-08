"""
Menú Principal con opciones de Nueva Partida, Continuar, Debug y Opciones.
"""
import pygame
from ui.button import Button
from ui.panel import Panel
from settings import DESIGN_W, DESIGN_H, C


class MainMenuScreen:
    def __init__(self, manager, game_state):
        self.manager = manager
        self.state = game_state

        bx = DESIGN_W // 2 - 120
        by = DESIGN_H // 2 - 85

        self.btn_new_run = Button(
            bx, by, 240, 48, "NUEVA PARTIDA", bg_color=C.BTN_GREEN,
            hover_color=C.BTN_GREEN_HI, font_size=24,
            callback=self.start_new_run
        )
        self.btn_continue = Button(
            bx, by + 60, 240, 48, "CONTINUAR", bg_color=C.BTN_BLUE,
            hover_color=C.BTN_BLUE_HI, font_size=24,
            callback=lambda: self.manager.change_screen("gameplay")
        )
        self.btn_debug = Button(
            bx, by + 120, 240, 48, "MODO DEBUG", bg_color=C.BTN_ORANGE,
            hover_color=C.BTN_ORANGE_HI, font_size=24,
            callback=lambda: self.manager.change_screen("debug")
        )
        self.btn_options = Button(
            bx, by + 180, 240, 48, "OPCIONES", bg_color=C.PANEL_LIGHT,
            hover_color=C.PANEL_BORDER, font_size=24,
            callback=lambda: self.manager.change_screen("settings")
        )

        self.buttons = [
            self.btn_new_run, self.btn_continue,
            self.btn_debug, self.btn_options
        ]

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
        panel_rect = pygame.Rect(DESIGN_W // 2 - 160, DESIGN_H // 2 - 170, 320, 370)
        Panel.draw_panel(surface, panel_rect, bg_color=C.PANEL_DARK)

        font_h = asset_mgr.font(34)
        txt = font_h.render("MENU PRINCIPAL", True, C.WHITE)
        surface.blit(txt, (DESIGN_W // 2 - txt.get_width() // 2, DESIGN_H // 2 - 145))

        for btn in self.buttons:
            btn.draw(surface, asset_mgr.font(24))
