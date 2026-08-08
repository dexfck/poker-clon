"""
Blind Selection Screen displaying Small Blind, Big Blind, and Boss Blind cards.
Adapted from example with real BlindManager data from poker_clon.
"""
import pygame
from ui.button import Button
from ui.panel import Panel
from settings import DESIGN_W, DESIGN_H, C


class BlindSelectScreen:
    def __init__(self, manager, game_state):
        self.manager = manager
        self.state = game_state

        self.btn_select_small = Button(
            DESIGN_W // 2 - 330, DESIGN_H // 2 + 130, 180, 45, "SELECCIONAR",
            bg_color=C.BTN_BLUE, hover_color=C.BTN_BLUE_HI, font_size=22,
            callback=self.select_small
        )
        self.btn_skip_small = Button(
            DESIGN_W // 2 - 330, DESIGN_H // 2 + 185, 180, 40, "SALTAR ($3)",
            bg_color=C.BTN_ORANGE, hover_color=C.BTN_ORANGE_HI, font_size=18,
            callback=self.skip_small
        )
        self.btn_select_big = Button(
            DESIGN_W // 2 - 90, DESIGN_H // 2 + 130, 180, 45, "SELECCIONAR",
            bg_color=C.BTN_BLUE, hover_color=C.BTN_BLUE_HI, font_size=22,
            callback=self.select_big
        )
        self.btn_select_boss = Button(
            DESIGN_W // 2 + 150, DESIGN_H // 2 + 130, 180, 45, "SELECCIONAR",
            bg_color=C.BTN_RED, hover_color=C.BTN_RED_HI, font_size=22,
            callback=self.select_boss
        )

        self.buttons = [
            self.btn_select_small, self.btn_skip_small,
            self.btn_select_big, self.btn_select_boss
        ]
    def update_button_states(self):
        order = ["Small", "Big", "Boss"]
        curr_blind = self.state.blind_manager.current_blind
        curr_idx = order.index(curr_blind) if curr_blind in order else 0

        # Small Blind
        if 0 < curr_idx:
            self.btn_select_small.enabled = False
            self.btn_select_small.text = "SUPERADA"
            self.btn_select_small.bg_color = (60, 60, 60)
            self.btn_select_small.hover_color = (60, 60, 60)
            self.btn_select_small.text_color = C.D_GREY

            self.btn_skip_small.enabled = False
            self.btn_skip_small.text = "SUPERADA"
            self.btn_skip_small.bg_color = (40, 40, 40)
            self.btn_skip_small.hover_color = (40, 40, 40)
            self.btn_skip_small.text_color = C.D_GREY
        elif 0 == curr_idx:
            self.btn_select_small.enabled = True
            self.btn_select_small.text = "SELECCIONAR"
            self.btn_select_small.bg_color = C.BTN_BLUE
            self.btn_select_small.hover_color = C.BTN_BLUE_HI
            self.btn_select_small.text_color = C.WHITE

            self.btn_skip_small.enabled = True
            self.btn_skip_small.text = "SALTAR ($3)"
            self.btn_skip_small.bg_color = C.BTN_ORANGE
            self.btn_skip_small.hover_color = C.BTN_ORANGE_HI
            self.btn_skip_small.text_color = C.WHITE

        # Big Blind
        if 1 < curr_idx:
            self.btn_select_big.enabled = False
            self.btn_select_big.text = "SUPERADA"
            self.btn_select_big.bg_color = (60, 60, 60)
            self.btn_select_big.hover_color = (60, 60, 60)
            self.btn_select_big.text_color = C.D_GREY
        elif 1 == curr_idx:
            self.btn_select_big.enabled = True
            self.btn_select_big.text = "SELECCIONAR"
            self.btn_select_big.bg_color = C.BTN_BLUE
            self.btn_select_big.hover_color = C.BTN_BLUE_HI
            self.btn_select_big.text_color = C.WHITE
        else:
            self.btn_select_big.enabled = False
            self.btn_select_big.text = "BLOQUEADA"
            self.btn_select_big.bg_color = (45, 45, 55)
            self.btn_select_big.hover_color = (45, 45, 55)
            self.btn_select_big.text_color = C.GREY

        # Boss Blind
        if 2 == curr_idx:
            self.btn_select_boss.enabled = True
            self.btn_select_boss.text = "SELECCIONAR"
            self.btn_select_boss.bg_color = C.BTN_RED
            self.btn_select_boss.hover_color = C.BTN_RED_HI
            self.btn_select_boss.text_color = C.WHITE
        else:
            self.btn_select_boss.enabled = False
            self.btn_select_boss.text = "BLOQUEADA"
            self.btn_select_boss.bg_color = (45, 45, 55)
            self.btn_select_boss.hover_color = (45, 45, 55)
            self.btn_select_boss.text_color = C.GREY

    def select_small(self):
        if not self.btn_select_small.enabled:
            return
        self.state.blind_manager.current_blind = "Small"
        self.state.blind_state = "Small"
        self.state.reset_round()
        self.manager.change_screen("gameplay")

    def skip_small(self):
        if not self.btn_skip_small.enabled:
            return
        self.state.dollars += 3
        self.state.blind_manager.advance_blind()
        self.manager.change_screen("shop")

    def select_big(self):
        if not self.btn_select_big.enabled:
            return
        self.state.blind_manager.current_blind = "Big"
        self.state.blind_state = "Big"
        self.state.reset_round()
        self.manager.change_screen("gameplay")

    def select_boss(self):
        if not self.btn_select_boss.enabled:
            return
        self.state.blind_manager.current_blind = "Boss"
        self.state.blind_state = "Boss"
        self.state.reset_round()
        self.manager.change_screen("gameplay")

    def on_enter(self):
        self.update_button_states()

    def update(self, dt: float, mouse_pos: tuple[int, int]):
        self.update_button_states()
        for btn in self.buttons:
            btn.update(dt, mouse_pos)

    def handle_event(self, event: pygame.event.Event):
        for btn in self.buttons:
            btn.handle_event(event)

    def draw(self, surface: pygame.Surface, asset_mgr):
        font_h = asset_mgr.font(38)
        txt = font_h.render(f"ANTE {self.state.ante} / 8", True, C.WHITE)
        surface.blit(txt, (DESIGN_W // 2 - txt.get_width() // 2, 50))

        # Get blind data from real BlindManager
        bm = self.state.blind_manager
        base = bm.base_scores.get(bm.ante, bm.base_scores[8] * (bm.ante - 7))
        boss = bm.current_boss
        boss_mult = 4 if boss["name"] == "El Muro" else 2

        blinds = [
            ("Ciega Pequeña", f"Puntaje: {base:,}", "Recompensa: $3",
             asset_mgr.get_blind_chip(col=0, row=0, size=(64, 64)), C.CHIPS_BLUE),
            ("Ciega Grande", f"Puntaje: {int(base * 1.5):,}", "Recompensa: $4",
             asset_mgr.get_blind_chip(col=0, row=1, size=(64, 64)), C.MONEY_GOLD),
            (boss["name"], f"Puntaje: {base * boss_mult:,}", "Recompensa: $5",
             asset_mgr.get_blind_chip(col=boss["col"], row=boss["row"], size=(64, 64)), C.MULT_RED),
        ]

        card_xs = [DESIGN_W // 2 - 340, DESIGN_W // 2 - 100, DESIGN_W // 2 + 140]

        for i, (b_title, b_score, b_reward, chip_img, col) in enumerate(blinds):
            x = card_xs[i]
            panel_rect = pygame.Rect(x, DESIGN_H // 2 - 140, 200, 250)
            Panel.draw_panel(surface, panel_rect, bg_color=C.PANEL_DARK, border_color=col)

            f_title = asset_mgr.font(20)
            t_sf = f_title.render(b_title, True, col)
            surface.blit(t_sf, (x + 100 - t_sf.get_width() // 2, DESIGN_H // 2 - 125))

            if chip_img:
                surface.blit(chip_img, (x + 100 - 32, DESIGN_H // 2 - 95))

            f_body = asset_mgr.font(18)
            ts_sf = f_body.render(b_score, True, C.WHITE)
            tr_sf = f_body.render(b_reward, True, C.MONEY_GOLD)
            surface.blit(ts_sf, (x + 100 - ts_sf.get_width() // 2, DESIGN_H // 2 - 20))
            surface.blit(tr_sf, (x + 100 - tr_sf.get_width() // 2, DESIGN_H // 2 + 5))

            # Show boss description for boss blind
            if i == 2 and boss.get("desc"):
                lines = boss["desc"].split('\n')
                y_desc = DESIGN_H // 2 + 35
                f_desc = asset_mgr.font(14)
                for line in lines:
                    t_desc = f_desc.render(line, True, C.L_GREY)
                    surface.blit(t_desc, (x + 100 - t_desc.get_width() // 2, y_desc))
                    y_desc += 18

        for btn in self.buttons:
            btn.draw(surface, asset_mgr.font(20))
