"""
Full Gameplay Screen with step-by-step scoring animation using REAL poker_clon logic.
Merges example's visual design with poker_clon's scoring, joker effects, and economy.
"""
import random
import pygame
from ui.button import Button
from ui.panel import Panel
from ui.card_sprite import CardSprite
from ui.joker_sprite import JokerSprite
from ui.counter import AnimatedCounter
from ui.tooltip import Tooltip
from engine.poker_hands import evaluate_hand
from engine.sound_manager import SoundManager
from effects.screen_shake import ScreenShake
from effects.particles import ParticleSystem
from effects.round_clear_modal import RoundClearModal
from settings import DESIGN_W, DESIGN_H, C, CARD_DISPLAY_W, CARD_DISPLAY_H, RANK_VALUES


class GameplayScreen:

    # Animation States
    IDLE = 0
    LIFT_PLAYED = 1
    SCORE_CARDS = 2
    SCORE_JOKERS = 3
    CALCULATE = 4
    DISCARDING = 5

    def __init__(self, manager, game_state, sound_manager: SoundManager):
        self.manager = manager
        self.state = game_state
        self.sound_manager = sound_manager
        self.shake = ScreenShake()
        self.particles = ParticleSystem()
        self.tooltip = Tooltip()
        self.round_modal = RoundClearModal(self.on_cash_out_complete)

        self.card_sprites: list[CardSprite] = []
        self.joker_sprites: list[JokerSprite] = []
        self.played_card_sprites: list[CardSprite] = []

        # Scoring State Machine variables
        self.scoring_state = self.IDLE
        self.state_timer = 0.0
        self.current_card_idx = 0
        self.current_joker_idx = 0
        self.accumulated_chips = 0
        self.accumulated_mult = 0

        # Store played cards for joker context
        self.played_cards = []
        self.hand_name = ""

        # Anzuelo boss discard animation list
        self.anzuelo_discard_sprites = []
        self.anzuelo_discard_cards = []

        # Animated formula counters
        self.chip_counter = AnimatedCounter(value=0, color=C.WHITE, font_size=24)
        self.mult_counter = AnimatedCounter(value=0, color=C.WHITE, font_size=24)

        # Action Buttons
        self.btn_run_info = Button(
            16, 352, 100, 110, "Inicio",
            bg_color=C.BTN_RED, hover_color=C.BTN_RED_HI, font_size=18,
            callback=lambda: self.manager.change_screen("main_menu")
        )
        self.btn_options = Button(
            16, 472, 100, 120, "Opciones",
            bg_color=C.BTN_ORANGE, hover_color=C.BTN_ORANGE_HI, font_size=17,
            callback=lambda: self.manager.change_screen("settings")
        )

        table_center_x = (310 + (DESIGN_W - 145)) // 2
        self.btn_play_hand = Button(
            table_center_x - 160, DESIGN_H - 95, 150, 44, "JUGAR MANO",
            bg_color=C.BTN_BLUE, hover_color=C.BTN_BLUE_HI, font_size=18,
            callback=self.start_play_hand
        )
        self.btn_discard = Button(
            table_center_x + 10, DESIGN_H - 95, 150, 44, "DESCARTAR",
            bg_color=C.BTN_RED, hover_color=C.BTN_RED_HI, font_size=18,
            callback=self.start_discard
        )

        self.btn_sort_val = Button(
            table_center_x - 138, DESIGN_H - 45, 105, 32, "Ord. Rango",
            bg_color=(205, 160, 50), hover_color=(230, 185, 70), text_color=C.BLACK, font_size=14,
            callback=self.sort_by_rank
        )
        self.btn_sort_suit = Button(
            table_center_x + 32, DESIGN_H - 45, 105, 32, "Ord. Palo",
            bg_color=(205, 160, 50), hover_color=(230, 185, 70), text_color=C.BLACK, font_size=14,
            callback=self.sort_by_suit
        )

        self.buttons = [
            self.btn_run_info, self.btn_options,
            self.btn_play_hand, self.btn_discard,
            self.btn_sort_val, self.btn_sort_suit
        ]

    def on_enter(self):
        self.scoring_state = self.IDLE
        self.played_card_sprites.clear()
        self.refresh_cards()
        self.refresh_jokers()

    def apply_boss_effects(self):
        bm = self.state.blind_manager
        is_boss = (bm.current_blind == "Boss")
        boss_name = bm.current_boss["name"] if is_boss else ""

        for card in self.state.hand:
            if is_boss and boss_name == "La Ventana" and card.is_face:
                card.debuffed = True
            elif is_boss and boss_name == "El Pilar" and (card.suit, card.rank) in self.state.played_cards_this_ante:
                card.debuffed = True
            else:
                card.debuffed = False

    def refresh_cards(self):
        self.apply_boss_effects()
        self.card_sprites.clear()
        hand = self.state.hand
        count = len(hand)
        if count == 0:
            return

        table_center_x = (310 + (DESIGN_W - 145)) // 2
        spacing = min(72, (DESIGN_W - 550) // max(count, 1))
        start_x = table_center_x - ((count * spacing) // 2)
        start_y = DESIGN_H - 265

        for i, card in enumerate(hand):
            cs = CardSprite(start_x + i * spacing, start_y, card, w=CARD_DISPLAY_W, h=CARD_DISPLAY_H)
            cs.is_selected = card in self.state.selected_cards
            self.card_sprites.append(cs)

    def refresh_jokers(self):
        self.joker_sprites.clear()
        jokers = self.state.jokers
        table_center_x = (310 + (DESIGN_W - 145)) // 2
        spacing = 88
        start_x = table_center_x - 210
        start_y = 23

        for i, joker in enumerate(jokers):
            js = JokerSprite(start_x + i * spacing, start_y, joker, w=68, h=92)
            self.joker_sprites.append(js)

    # ------------------------------------------------------------------
    # Action Triggers with REAL poker_clon logic
    # ------------------------------------------------------------------
    def start_play_hand(self):
        if self.scoring_state != self.IDLE or not self.state.selected_cards or self.state.hands_left <= 0:
            return

        # Store played cards for scoring context and track played cards this Ante
        self.played_cards = list(self.state.selected_cards)
        for c in self.played_cards:
            self.state.played_cards_this_ante.add((c.suit, c.rank))

        self.played_card_sprites = [cs for cs in self.card_sprites if cs.card in self.state.selected_cards]
        self.state.hands_left -= 1
        self.state.hands_played += 1

        # Check "El Anzuelo" boss effect (discards 2 random cards from hand on play)
        self.anzuelo_discard_sprites.clear()
        self.anzuelo_discard_cards.clear()
        bm = self.state.blind_manager
        if bm.current_blind == "Boss" and bm.current_boss["name"] == "El Anzuelo":
            remaining_in_hand = [c for c in self.state.hand if c not in self.state.selected_cards]
            if len(remaining_in_hand) >= 2:
                to_discard = random.sample(remaining_in_hand, 2)
            else:
                to_discard = list(remaining_in_hand)

            self.anzuelo_discard_cards = to_discard
            self.anzuelo_discard_sprites = [cs for cs in self.card_sprites if cs.card in to_discard]

            if to_discard:
                self.particles.emit_popup("¡El Anzuelo descarta 2 cartas!", DESIGN_W // 2, 200, C.MULT_RED)

        # Evaluate base chips and mult using REAL evaluator
        self.hand_name, base_chips, base_mult = evaluate_hand(self.played_cards)
        self.accumulated_chips = base_chips
        self.accumulated_mult = base_mult

        self.chip_counter.set_target(self.accumulated_chips)
        self.mult_counter.set_target(self.accumulated_mult)

        self.scoring_state = self.LIFT_PLAYED
        self.state_timer = 0.0

    def start_discard(self):
        if self.scoring_state != self.IDLE or not self.state.selected_cards or self.state.discards_left <= 0:
            return

        self.state.discards_left -= 1
        self.state.discards_used += 1
        self.scoring_state = self.DISCARDING
        self.state_timer = 0.0

    def sort_by_rank(self):
        if self.scoring_state == self.IDLE:
            self.state.current_sort_mode = "RANK"
            self.state.hand.sort(key=lambda c: (RANK_VALUES.get(c.rank, 0), c.suit_idx), reverse=True)
            self.state.selected_cards.clear()
            self.refresh_cards()

    def sort_by_suit(self):
        if self.scoring_state == self.IDLE:
            self.state.current_sort_mode = "SUIT"
            self.state.hand.sort(key=lambda c: (c.suit_idx, RANK_VALUES.get(c.rank, 0)), reverse=True)
            self.state.selected_cards.clear()
            self.refresh_cards()

    def on_cash_out_complete(self, total_earned: int):
        self.state.dollars += total_earned
        if self.state.ante >= 8 and self.state.blind_manager.current_blind == "Boss":
            self.manager.change_screen("win")
            return

        self.state.advance_blind()

        # Generate shop stock
        self.state._shop_stock = self.state.generate_shop()
        self.manager.change_screen("shop")

    # ------------------------------------------------------------------
    # Update Loop & State Machine with REAL scoring
    # ------------------------------------------------------------------
    def update(self, dt: float, mouse_pos: tuple[int, int]):
        self.shake.update(dt)
        self.particles.update(dt)
        self.chip_counter.update(dt)
        self.mult_counter.update(dt)
        self.round_modal.update(dt, mouse_pos)
        self.sound_manager.update(dt)

        if not self.round_modal.active:
            for btn in self.buttons:
                btn.update(dt, mouse_pos)

            topmost_hovered = False
            if self.scoring_state == self.IDLE:
                for cs in reversed(self.card_sprites):
                    hit_rect = cs.get_hit_rect()
                    if not topmost_hovered and hit_rect.collidepoint(mouse_pos) and cs.enabled:
                        cs.is_hovered = True
                        topmost_hovered = True
                    else:
                        cs.is_hovered = False
                    cs.update(dt, mouse_pos)
            else:
                for cs in self.card_sprites:
                    cs.is_hovered = False
                    cs.update(dt, mouse_pos)

                if self.anzuelo_discard_sprites:
                    for cs in self.anzuelo_discard_sprites:
                        cs.rect.centerx += int(dt * 900.0)
                        cs.rect.centery += int(dt * 900.0)

            joker_hovered = False
            for js in self.joker_sprites:
                js.update(dt, mouse_pos)
                if js.is_hovered:
                    desc = js.joker.description
                    desc_text = " ".join(desc) if isinstance(desc, list) else desc
                    self.tooltip.show(js.joker.name, desc_text, mouse_pos[0], mouse_pos[1])
                    joker_hovered = True

            if not joker_hovered:
                self.tooltip.hide()

        # -------------------------------------------------------------------
        # Scoring State Machine with REAL poker_clon logic
        # -------------------------------------------------------------------
        if self.scoring_state == self.LIFT_PLAYED:
            self.state_timer += dt
            for cs in self.played_card_sprites:
                cs.rect.centery += (280 - cs.rect.centery) * min(dt * 15.0, 1.0)

            if self.state_timer >= 0.50:
                self.scoring_state = self.SCORE_CARDS
                self.current_card_idx = 0
                self.state_timer = 0.0

        elif self.scoring_state == self.SCORE_CARDS:
            self.state_timer += dt
            if self.state_timer >= 0.45:
                if self.current_card_idx < len(self.played_card_sprites):
                    cs = self.played_card_sprites[self.current_card_idx]
                    # REAL card chip value
                    chips_gained = cs.card.chips
                    self.accumulated_chips += chips_gained
                    self.chip_counter.set_target(self.accumulated_chips)

                    cs.offset_y = -25.0
                    self.particles.emit_popup(f"+{chips_gained}", cs.rect.centerx, cs.rect.top - 10, C.CHIPS_BLUE)
                    self.sound_manager.play_chips()

                    self.current_card_idx += 1
                    self.state_timer = 0.0
                else:
                    # Move to Joker scoring
                    self.scoring_state = self.SCORE_JOKERS
                    self.current_joker_idx = 0
                    self.state_timer = 0.0

        elif self.scoring_state == self.SCORE_JOKERS:
            self.state_timer += dt
            if self.state_timer >= 0.45:
                if self.current_joker_idx < len(self.joker_sprites):
                    js = self.joker_sprites[self.current_joker_idx]
                    joker = js.joker

                    # REAL joker.apply() with context
                    context = {
                        "cards": self.played_cards,
                        "hand_name": self.hand_name,
                        "game": self.state,
                    }
                    old_chips, old_mult = self.accumulated_chips, self.accumulated_mult
                    new_chips, new_mult = joker.apply(old_chips, old_mult, context)

                    # Trigger animation, sound, and popup ONLY if joker condition is met
                    if new_mult > old_mult:
                        js.scale = 1.15
                        diff = new_mult - old_mult
                        desc_list = joker.description if isinstance(joker.description, list) else [joker.description]
                        is_x_joker = any("X" in line for line in desc_list)
                        if is_x_joker and old_mult > 0 and new_mult % old_mult == 0:
                            popup_text = f"X{new_mult // old_mult}"
                        else:
                            popup_text = f"+{diff} Mult"
                        self.particles.emit_popup(popup_text, js.rect.centerx, js.rect.bottom + 15, C.MULT_RED)
                        self.sound_manager.play_mult()
                    elif new_chips > old_chips:
                        js.scale = 1.15
                        diff = new_chips - old_chips
                        self.particles.emit_popup(f"+{diff} Fichas", js.rect.centerx, js.rect.bottom + 15, C.CHIPS_BLUE)
                        self.sound_manager.play_chips()

                    self.accumulated_chips = new_chips
                    self.accumulated_mult = new_mult
                    self.chip_counter.set_target(self.accumulated_chips)
                    self.mult_counter.set_target(self.accumulated_mult)

                    self.current_joker_idx += 1
                    self.state_timer = 0.0
                else:
                    self.scoring_state = self.CALCULATE
                    self.state_timer = 0.0

        elif self.scoring_state == self.CALCULATE:
            self.state_timer += dt
            if self.state_timer >= 0.45:
                earned_score = self.accumulated_chips * self.accumulated_mult
                self.state.current_score += earned_score

                self.shake.trigger(intensity=12.0, duration=0.5)
                self.particles.emit_burst(DESIGN_W // 2, DESIGN_H // 2, [C.CHIPS_BLUE, C.MULT_RED, C.MONEY_GOLD], count=45)

                # Remove played cards & Anzuelo discarded cards from hand
                for c in self.played_cards + self.anzuelo_discard_cards:
                    if c in self.state.hand:
                        self.state.hand.remove(c)
                self.state.selected_cards.clear()
                self.played_card_sprites.clear()
                self.played_cards.clear()
                self.anzuelo_discard_sprites.clear()
                self.anzuelo_discard_cards.clear()
                self.state.draw_to_hand()
                self.state._apply_current_sort()
                self.refresh_cards()

                # Check victory condition
                if self.state.current_score >= self.state.target_score:
                    info = self.state.blind_manager.get_blind_info()
                    self.round_modal.show(
                        blind_reward=info["reward"],
                        hands_left=self.state.hands_left,
                        discards_left=self.state.discards_left,
                        current_dollars=self.state.dollars
                    )

                    if self.state.blind_manager.ante >= 8:
                        self.sound_manager.play_win()

                elif self.state.hands_left <= 0:
                    self.sound_manager.play_game_over()
                    self.manager.change_screen("game_over")

                self.scoring_state = self.IDLE

        elif self.scoring_state == self.DISCARDING:
            self.state_timer += dt
            for cs in self.card_sprites:
                if cs.card in self.state.selected_cards:
                    cs.rect.centerx += int(dt * 900.0)
                    cs.rect.centery += int(dt * 900.0)

            if self.state_timer >= 0.3:
                for c in self.state.selected_cards:
                    if c in self.state.hand:
                        self.state.hand.remove(c)
                self.state.selected_cards.clear()
                self.state.draw_to_hand()
                self.state._apply_current_sort()
                self.refresh_cards()
                self.scoring_state = self.IDLE

        # Update Live Formula Preview when Idle
        if self.scoring_state == self.IDLE:
            if self.state.selected_cards:
                ht, bc, bm = evaluate_hand(self.state.selected_cards)
                card_c = sum(c.chips for c in self.state.selected_cards)
                self.chip_counter.set_target(bc + card_c)
                self.mult_counter.set_target(bm)
            else:
                self.chip_counter.set_target(0)
                self.mult_counter.set_target(0)

    def handle_event(self, event: pygame.event.Event):
        if self.round_modal.active:
            self.round_modal.handle_event(event)
            return

        if self.scoring_state != self.IDLE:
            return

        for btn in self.buttons:
            if btn.handle_event(event):
                return

        for cs in reversed(self.card_sprites):
            if cs.handle_event(event):
                if event.type == pygame.MOUSEBUTTONUP:
                    self.state.toggle_select(cs.card)
                    cs.is_selected = cs.card in self.state.selected_cards
                break

    def draw(self, surface: pygame.Surface, asset_mgr):
        sox, soy = self.shake.offset()
        view_surf = pygame.Surface((DESIGN_W, DESIGN_H), pygame.SRCALPHA)

        font_xs = asset_mgr.font(12)
        font_sm = asset_mgr.font(14)
        font_med = asset_mgr.font(18)
        font_lg = asset_mgr.font(24)
        font_xl = asset_mgr.font(30)

        # -------------------------------------------------------------------
        # 1. Full-Height Dark Sidebar Container (Wider 310px Layout)
        # -------------------------------------------------------------------
        sidebar_rect = pygame.Rect(0, 0, 310, DESIGN_H)
        pygame.draw.rect(view_surf, C.SIDEBAR_BG, sidebar_rect)
        pygame.draw.line(view_surf, C.SIDEBAR_BORDER, (310, 0), (310, DESIGN_H), 3)

        # A) Blind Panel (Score Target Only)
        outer_blind = pygame.Rect(16, 14, 278, 102)
        pygame.draw.rect(view_surf, (62, 55, 24), outer_blind, border_radius=8)
        pygame.draw.rect(view_surf, (30, 26, 12), outer_blind, width=2, border_radius=8)

        info = self.state.blind_manager.get_blind_info()
        blind_title_text = info["name"]
        b_header_rect = pygame.Rect(22, 6, 266, 32)
        pygame.draw.rect(view_surf, C.BLIND_GOLD, b_header_rect, border_radius=6)
        pygame.draw.rect(view_surf, (30, 20, 5), b_header_rect, width=2, border_radius=6)
        t_bname = font_med.render(blind_title_text, True, C.WHITE)
        view_surf.blit(t_bname, (b_header_rect.centerx - t_bname.get_width() // 2, b_header_rect.centery - t_bname.get_height() // 2))

        chip_img = asset_mgr.get_blind_chip(col=info["col"], row=info["row"], size=(56, 56))
        if chip_img:
            view_surf.blit(chip_img, (24, 46))

        targ_box = pygame.Rect(92, 42, 194, 66)
        pygame.draw.rect(view_surf, C.SIDEBAR_INNER, targ_box, border_radius=6)

        t_lbl = font_sm.render("Al menos", True, C.L_GREY)
        t_val = asset_mgr.font(32).render(f"{self.state.target_score:,}", True, C.MULT_RED)
        view_surf.blit(t_lbl, (100, 47))
        view_surf.blit(t_val, (100, 68))

        # A.2) Dedicated Reward Box (Below Blind Panel)
        rew_box = pygame.Rect(16, 122, 278, 44)
        pygame.draw.rect(view_surf, C.SIDEBAR_INNER, rew_box, border_radius=6)

        t_rew_lbl = font_sm.render("Recompensa", True, C.L_GREY)
        t_rew_val = asset_mgr.font(32).render(f"${info['reward']}", True, C.MONEY_GOLD)
        view_surf.blit(t_rew_lbl, (24, rew_box.centery - t_rew_lbl.get_height() // 2))
        view_surf.blit(t_rew_val, (rew_box.centerx - t_rew_val.get_width() // 2, rew_box.centery - t_rew_val.get_height() // 2))

        # B) Round Score Box
        rs_box = pygame.Rect(16, 172, 278, 44)
        pygame.draw.rect(view_surf, C.SIDEBAR_INNER, rs_box, border_radius=6)

        t_rs_lbl = font_sm.render("Puntaje ronda", True, C.L_GREY)
        t_rs_val = asset_mgr.font(32).render(f"{self.state.current_score:,}", True, C.WHITE)
        view_surf.blit(t_rs_lbl, (24, rs_box.centery - t_rs_lbl.get_height() // 2))
        view_surf.blit(t_rs_val, (rs_box.centerx - t_rs_val.get_width() // 2, rs_box.centery - t_rs_val.get_height() // 2))

        # C) Hand Title & Formula Box
        hand_panel = pygame.Rect(16, 222, 278, 136)
        pygame.draw.rect(view_surf, C.SIDEBAR_INNER, hand_panel, border_radius=8)

        if self.state.selected_cards:
            ht, _, _ = evaluate_hand(self.state.selected_cards)
            h_lvl = "niv.1"
        else:
            ht, h_lvl = "Selecciona cartas", ""

        t_ht = font_lg.render(ht, True, C.WHITE)
        t_hl = font_xs.render(h_lvl, True, C.GREY)
        view_surf.blit(t_ht, (hand_panel.centerx - (t_ht.get_width() + t_hl.get_width()) // 2, 230))
        if h_lvl:
            view_surf.blit(t_hl, (hand_panel.centerx + t_ht.get_width() // 2 + 4, 237))

        chips_box_rect = pygame.Rect(28, 274, 114, 70)
        mult_box_rect = pygame.Rect(168, 274, 114, 70)

        pygame.draw.rect(view_surf, C.CHIPS_BLUE, chips_box_rect, border_radius=8)
        pygame.draw.rect(view_surf, C.MULT_RED, mult_box_rect, border_radius=8)

        self.chip_counter.draw(view_surf, font_xl, center_rect=chips_box_rect)
        self.mult_counter.draw(view_surf, font_xl, center_rect=mult_box_rect)

        t_x = font_xl.render("x", True, C.MULT_RED)
        view_surf.blit(t_x, (148, 292))

        # D) Dense Bottom Info Grid
        for btn in [self.btn_run_info, self.btn_options]:
            btn.draw(view_surf, asset_mgr.font(17))

        h_box = pygame.Rect(126, 364, 80, 66)
        d_box = pygame.Rect(214, 364, 80, 66)

        pygame.draw.rect(view_surf, C.SIDEBAR_INNER, h_box, border_radius=6)
        pygame.draw.rect(view_surf, C.SIDEBAR_INNER, d_box, border_radius=6)

        t_h_lbl = font_sm.render("Manos", True, C.L_GREY)
        t_h_val = font_xl.render(str(self.state.hands_left), True, C.CHIPS_BLUE)
        view_surf.blit(t_h_lbl, (h_box.centerx - t_h_lbl.get_width() // 2, 368))
        view_surf.blit(t_h_val, (h_box.centerx - t_h_val.get_width() // 2, 390))

        t_d_lbl = font_sm.render("Descartes", True, C.L_GREY)
        t_d_val = font_xl.render(str(self.state.discards_left), True, C.MULT_RED)
        view_surf.blit(t_d_lbl, (d_box.centerx - t_d_lbl.get_width() // 2, 368))
        view_surf.blit(t_d_val, (d_box.centerx - t_d_val.get_width() // 2, 390))

        m_box = pygame.Rect(126, 436, 168, 74)
        pygame.draw.rect(view_surf, C.SIDEBAR_INNER, m_box, border_radius=6)
        t_m_val = asset_mgr.font(36).render(f"${self.state.dollars}", True, C.MONEY_GOLD)
        view_surf.blit(t_m_val, (m_box.centerx - t_m_val.get_width() // 2, m_box.centery - t_m_val.get_height() // 2))

        ante_box = pygame.Rect(126, 516, 80, 70)
        rnd_box = pygame.Rect(214, 516, 80, 70)

        pygame.draw.rect(view_surf, C.SIDEBAR_INNER, ante_box, border_radius=6)
        pygame.draw.rect(view_surf, C.SIDEBAR_INNER, rnd_box, border_radius=6)

        t_a_lbl = font_sm.render("Ante", True, C.L_GREY)
        t_a_val = font_lg.render(f"{self.state.ante} / 8", True, C.MONEY_GOLD)
        view_surf.blit(t_a_lbl, (ante_box.centerx - t_a_lbl.get_width() // 2, 521))
        view_surf.blit(t_a_val, (ante_box.centerx - t_a_val.get_width() // 2, 543))

        t_r_lbl = font_sm.render("Ronda", True, C.L_GREY)
        t_r_val = font_xl.render(str(self.state.round), True, C.MONEY_GOLD)
        view_surf.blit(t_r_lbl, (rnd_box.centerx - t_r_lbl.get_width() // 2, 521))
        view_surf.blit(t_r_val, (rnd_box.centerx - t_r_val.get_width() // 2, 543))

        # -------------------------------------------------------------------
        # 2. Top Middle Area (Centered Jokers Bar)
        # -------------------------------------------------------------------
        table_center_x = (310 + (DESIGN_W - 145)) // 2
        joker_ground = pygame.Rect(table_center_x - 240, 12, 480, 115)
        pygame.draw.rect(view_surf, (0, 0, 0, 50), joker_ground, border_radius=8)
        t_j_count = font_xs.render(f"{len(self.state.jokers)}/{self.state.max_jokers}", True, C.WHITE)
        view_surf.blit(t_j_count, (table_center_x - 233, 105))

        for js in self.joker_sprites:
            js.draw(view_surf, asset_mgr)

        # -------------------------------------------------------------------
        # 2.B Boss Blind Description Text (Effect only, Light Red)
        # -------------------------------------------------------------------
        if self.state.blind_manager.current_blind == "Boss":
            boss_info = self.state.blind_manager.current_boss
            b_desc = boss_info.get("desc", "").replace("\n", " ")

            font_boss_banner = asset_mgr.font(22)
            light_red = (255, 100, 105)

            t_shadow = font_boss_banner.render(b_desc, True, (0, 0, 0))
            t_boss_banner = font_boss_banner.render(b_desc, True, light_red)

            center_x = table_center_x
            center_y = 152
            tx = center_x - t_boss_banner.get_width() // 2
            ty = center_y - t_boss_banner.get_height() // 2

            view_surf.blit(t_shadow, (tx + 2, ty + 2))
            view_surf.blit(t_boss_banner, (tx, ty))

        # -------------------------------------------------------------------
        # 3. Deck Stack & Card Count Display
        # -------------------------------------------------------------------
        dw, dh = CARD_DISPLAY_W, CARD_DISPLAY_H
        deck_x = DESIGN_W - 145
        deck_y = DESIGN_H - 175

        card_back_img = asset_mgr.card_back if asset_mgr.card_back else None
        if card_back_img:
            scaled_back = pygame.transform.smoothscale(card_back_img, (dw, dh))
            for offset in range(3, -1, -1):
                view_surf.blit(scaled_back, (deck_x - offset * 1, deck_y - offset * 1))
        else:
            pygame.draw.rect(view_surf, C.MULT_RED, (deck_x, deck_y, dw, dh), border_radius=6)

        deck_count_str = f"{len(self.state.draw_pile)} / {len(self.state.deck)}"
        t_dcount = font_sm.render(deck_count_str, True, C.WHITE)
        view_surf.blit(t_dcount, (deck_x + dw // 2 - t_dcount.get_width() // 2, deck_y + dh + 5))

        selected_cnt_str = f"{len(self.state.selected_cards)} / {self.state.hand_size}"
        t_hand_cnt = font_sm.render(selected_cnt_str, True, C.WHITE)
        table_center_x = (310 + (DESIGN_W - 145)) // 2
        view_surf.blit(t_hand_cnt, (table_center_x - t_hand_cnt.get_width() // 2, DESIGN_H - 118))

        # -------------------------------------------------------------------
        # 4. Hand Cards & Action Buttons
        # -------------------------------------------------------------------
        for cs in self.card_sprites:
            cs.draw(view_surf, asset_mgr)

        for btn in [self.btn_play_hand, self.btn_discard, self.btn_sort_val, self.btn_sort_suit]:
            btn.draw(view_surf, asset_mgr.font(16))

        # Render particles & score text popups
        self.particles.draw(view_surf, font_med)
        self.tooltip.draw(view_surf, asset_mgr.font(18), asset_mgr.font(14))

        # Render RoundClearModal overlay when active
        self.round_modal.draw(view_surf, asset_mgr)

        # Blit view_surf with shake offset
        surface.blit(view_surf, (sox, soy))
