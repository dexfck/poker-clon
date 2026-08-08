"""
Debug / UI Tester Screen.
Allows instant switching between game screens, triggering animations,
testing specific boss blinds, and manipulating game state.
"""
import random
import pygame
from ui.button import Button
from ui.panel import Panel
from entities.joker import ALL_JOKERS
from engine.blinds import BOSS_BLINDS
from settings import DESIGN_W, DESIGN_H, C, JOKER_NAMES


class DebugScreen:
    def __init__(self, manager, game_state):
        self.manager = manager
        self.state = game_state

        self.btn_back = Button(
            40, 30, 100, 40, "VOLVER", bg_color=C.PANEL_LIGHT,
            hover_color=C.PANEL_BORDER, font_size=18,
            callback=lambda: self.manager.change_screen("main_menu")
        )

        # Screen Switcher Buttons Grid
        self.btn_title = Button(
            DESIGN_W // 2 - 250, 110, 230, 38, "1. Título",
            bg_color=C.BTN_BLUE, hover_color=C.BTN_BLUE_HI, font_size=16,
            callback=lambda: self.manager.change_screen("title")
        )
        self.btn_main_menu = Button(
            DESIGN_W // 2 + 20, 110, 230, 38, "2. Menú Principal",
            bg_color=C.BTN_BLUE, hover_color=C.BTN_BLUE_HI, font_size=16,
            callback=lambda: self.manager.change_screen("main_menu")
        )

        self.btn_blind_select = Button(
            DESIGN_W // 2 - 250, 155, 230, 38, "3. Selec. Ciega",
            bg_color=C.BTN_BLUE, hover_color=C.BTN_BLUE_HI, font_size=16,
            callback=lambda: self.manager.change_screen("blind_select")
        )
        self.btn_gameplay = Button(
            DESIGN_W // 2 + 20, 155, 230, 38, "4. Gameplay HUD",
            bg_color=C.BTN_GREEN, hover_color=C.BTN_GREEN_HI, font_size=16,
            callback=lambda: self.manager.change_screen("gameplay")
        )

        self.btn_shop = Button(
            DESIGN_W // 2 - 250, 200, 230, 38, "5. Tienda",
            bg_color=C.BTN_GREEN, hover_color=C.BTN_GREEN_HI, font_size=16,
            callback=lambda: self.manager.change_screen("shop")
        )
        self.btn_collection = Button(
            DESIGN_W // 2 + 20, 200, 230, 38, "6. Colección",
            bg_color=C.BTN_ORANGE, hover_color=C.BTN_ORANGE_HI, font_size=16,
            callback=lambda: self.manager.change_screen("collection")
        )

        self.btn_settings = Button(
            DESIGN_W // 2 - 250, 245, 230, 38, "7. Opciones",
            bg_color=C.BTN_ORANGE, hover_color=C.BTN_ORANGE_HI, font_size=16,
            callback=lambda: self.manager.change_screen("settings")
        )
        self.btn_game_over = Button(
            DESIGN_W // 2 + 20, 245, 230, 38, "8. Fin de Partida",
            bg_color=C.BTN_RED, hover_color=C.BTN_RED_HI, font_size=16,
            callback=lambda: self.manager.change_screen("game_over")
        )

        # State Modifiers
        self.btn_add_money = Button(
            DESIGN_W // 2 - 250, 295, 230, 38, "+ $50 Dinero",
            bg_color=C.BTN_GREEN, hover_color=C.BTN_GREEN_HI, font_size=16,
            callback=self.add_money
        )
        self.btn_add_joker = Button(
            DESIGN_W // 2 + 20, 295, 230, 38, "+ Comodín Aleatorio",
            bg_color=C.BTN_BLUE, hover_color=C.BTN_BLUE_HI, font_size=16,
            callback=self.add_joker
        )
        self.btn_reset_run = Button(
            DESIGN_W // 2 - 250, 340, 230, 38, "Reiniciar Partida",
            bg_color=C.BTN_DISABLED, hover_color=C.PANEL_BORDER, font_size=16,
            callback=self.reset_state
        )
        self.btn_win = Button(
            DESIGN_W // 2 + 20, 340, 230, 38, "9. Victoria",
            bg_color=C.BTN_GREEN, hover_color=C.BTN_GREEN_HI, font_size=16,
            callback=lambda: self.manager.change_screen("win")
        )

        # Boss Selector Buttons
        self.btn_boss_anzuelo = Button(
            DESIGN_W // 2 - 280, 440, 105, 42, "Anzuelo",
            bg_color=C.BTN_RED, hover_color=C.BTN_RED_HI, font_size=15,
            callback=lambda: self.select_boss("El Anzuelo")
        )
        self.btn_boss_pilar = Button(
            DESIGN_W // 2 - 168, 440, 105, 42, "Pilar",
            bg_color=C.BTN_RED, hover_color=C.BTN_RED_HI, font_size=15,
            callback=lambda: self.select_boss("El Pilar")
        )
        self.btn_boss_rueda = Button(
            DESIGN_W // 2 - 56, 440, 105, 42, "Rueda",
            bg_color=C.BTN_RED, hover_color=C.BTN_RED_HI, font_size=15,
            callback=lambda: self.select_boss("La Rueda")
        )
        self.btn_boss_muro = Button(
            DESIGN_W // 2 + 56, 440, 105, 42, "Muro",
            bg_color=C.BTN_RED, hover_color=C.BTN_RED_HI, font_size=15,
            callback=lambda: self.select_boss("El Muro")
        )
        self.btn_boss_ventana = Button(
            DESIGN_W // 2 + 168, 440, 105, 42, "Ventana",
            bg_color=C.BTN_RED, hover_color=C.BTN_RED_HI, font_size=15,
            callback=lambda: self.select_boss("La Ventana")
        )

        self.buttons = [
            self.btn_back,
            self.btn_title, self.btn_main_menu,
            self.btn_blind_select, self.btn_gameplay,
            self.btn_shop, self.btn_collection,
            self.btn_settings, self.btn_game_over,
            self.btn_add_money, self.btn_add_joker,
            self.btn_reset_run, self.btn_win,
            self.btn_boss_anzuelo, self.btn_boss_pilar,
            self.btn_boss_rueda, self.btn_boss_muro,
            self.btn_boss_ventana
        ]

    def add_money(self):
        self.state.dollars += 50

    def add_joker(self):
        if len(self.state.jokers) < self.state.max_jokers:
            joker_class = random.choice(ALL_JOKERS)
            joker = joker_class()
            self.state.jokers.append(joker)

    def reset_state(self):
        self.state.reset_run()

    def select_boss(self, boss_name: str):
        for b in BOSS_BLINDS:
            if b["name"] == boss_name:
                self.state.blind_manager.current_boss = b
                break
        self.state.blind_manager.current_blind = "Boss"
        self.state.blind_state = "Boss"
        self.state.boss_name = boss_name
        self.state.reset_round()
        self.manager.change_screen("gameplay")

    def on_enter(self):
        pass

    def update(self, dt: float, mouse_pos: tuple[int, int]):
        for btn in self.buttons:
            btn.update(dt, mouse_pos)

    def handle_event(self, event: pygame.event.Event):
        for btn in self.buttons:
            btn.handle_event(event)

    def draw(self, surface: pygame.Surface, asset_mgr):
        font_h = asset_mgr.font(34)
        txt = font_h.render("MODO DEBUG / TESTER", True, C.MONEY_GOLD)
        surface.blit(txt, (DESIGN_W // 2 - txt.get_width() // 2, 22))

        panel_rect = pygame.Rect(DESIGN_W // 2 - 300, 70, 600, 470)
        Panel.draw_panel(surface, panel_rect, bg_color=C.PANEL_DARK)

        # Boss Section Divider Label
        font_lbl = asset_mgr.font(17)
        t_boss = font_lbl.render("PROBAR CIEGA JEFE (BOSS BLIND):", True, C.MONEY_GOLD)
        surface.blit(t_boss, (DESIGN_W // 2 - t_boss.get_width() // 2, 408))

        font_sm = asset_mgr.font(15)
        ts = font_sm.render(
            f"Estado: Dinero ${self.state.dollars} | Comodines {len(self.state.jokers)}/5 | Ante {self.state.ante} | Ciega: {self.state.blind_state}",
            True, C.WHITE
        )
        surface.blit(ts, (DESIGN_W // 2 - ts.get_width() // 2, 502))

        for btn in self.buttons:
            btn.draw(surface, asset_mgr.font(16))
