"""
Settings Screen for toggling CRT filter, screen shake, and visual options.
"""
import pygame
from ui.button import Button
from ui.panel import Panel
from settings import DESIGN_W, DESIGN_H, C


class SettingsScreen:
    def __init__(self, manager, game_state, crt_filter, sound_manager=None):
        self.manager = manager
        self.state = game_state
        self.crt_filter = crt_filter
        self.sound = sound_manager

        bx = DESIGN_W // 2 - 130
        by = DESIGN_H // 2 - 60

        crt_state = "SÍ" if self.crt_filter.enabled else "NO"
        self.btn_toggle_crt = Button(
            bx, by, 260, 48, f"EFECTO CRT: {crt_state}",
            bg_color=C.BTN_GREEN if self.crt_filter.enabled else C.BTN_RED,
            hover_color=C.BTN_GREEN_HI if self.crt_filter.enabled else C.BTN_RED_HI,
            font_size=20, callback=self.toggle_crt
        )

        is_muted = getattr(self.sound, 'music_muted', False) if self.sound else False
        music_state = "SILENCIADA" if is_muted else "ACTIVADA"
        self.btn_toggle_music = Button(
            bx, by + 65, 260, 48, f"MÚSICA: {music_state}",
            bg_color=C.BTN_RED if is_muted else C.BTN_BLUE,
            hover_color=C.BTN_RED_HI if is_muted else C.BTN_BLUE_HI,
            font_size=20, callback=self.toggle_music
        )

        self.btn_back = Button(
            40, 40, 110, 42, "VOLVER", bg_color=C.PANEL_LIGHT,
            hover_color=C.PANEL_BORDER, font_size=20,
            callback=self.go_back
        )

        self.buttons = [self.btn_toggle_crt, self.btn_toggle_music, self.btn_back]

    def go_back(self):
        prev = self.manager.previous_screen_key
        target = prev if (prev and prev in self.manager.screens) else "main_menu"
        self.manager.change_screen(target)

    def toggle_crt(self):
        self.crt_filter.enabled = not self.crt_filter.enabled
        state_str = "SÍ" if self.crt_filter.enabled else "NO"
        self.btn_toggle_crt.text = f"EFECTO CRT: {state_str}"
        self.btn_toggle_crt.bg_color = C.BTN_GREEN if self.crt_filter.enabled else C.BTN_RED
        self.btn_toggle_crt.hover_color = C.BTN_GREEN_HI if self.crt_filter.enabled else C.BTN_RED_HI

    def toggle_music(self):
        if self.sound:
            is_muted = self.sound.toggle_mute_music()
            state_str = "SILENCIADA" if is_muted else "ACTIVADA"
            self.btn_toggle_music.text = f"MÚSICA: {state_str}"
            self.btn_toggle_music.bg_color = C.BTN_RED if is_muted else C.BTN_BLUE
            self.btn_toggle_music.hover_color = C.BTN_RED_HI if is_muted else C.BTN_BLUE_HI

    def on_enter(self):
        pass

    def update(self, dt: float, mouse_pos: tuple[int, int]):
        for btn in self.buttons:
            btn.update(dt, mouse_pos)

    def handle_event(self, event: pygame.event.Event):
        for btn in self.buttons:
            btn.handle_event(event)

    def draw(self, surface: pygame.Surface, asset_mgr):
        panel_rect = pygame.Rect(DESIGN_W // 2 - 170, DESIGN_H // 2 - 120, 340, 240)
        Panel.draw_panel(surface, panel_rect, bg_color=C.PANEL_DARK)

        font_h = asset_mgr.font(36)
        txt = font_h.render("OPCIONES", True, C.WHITE)
        surface.blit(txt, (DESIGN_W // 2 - txt.get_width() // 2, DESIGN_H // 2 - 105))

        for btn in self.buttons:
            btn.draw(surface, asset_mgr.font(20))
