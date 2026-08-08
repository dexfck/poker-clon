"""
Shop Screen with real Joker purchasing using poker_clon economy.
"""
import random
import pygame
from ui.button import Button
from ui.panel import Panel
from ui.joker_sprite import JokerSprite
from ui.tooltip import Tooltip
from entities.joker import ALL_JOKERS
from engine.economy import get_joker_price
from settings import DESIGN_W, DESIGN_H, C, CARD_SHOP_W, CARD_SHOP_H


class ShopScreen:
    def __init__(self, manager, game_state, sound_manager=None):
        self.manager = manager
        self.state = game_state
        self.sound_manager = sound_manager
        self.tooltip = Tooltip()

        self.shop_items = []  # list of dicts: {'joker': JokerBase, 'price': int, 'sold': bool}
        self.joker_sprites = []

        self.btn_next = Button(
            DESIGN_W // 2 + 160, DESIGN_H - 75, 180, 50, "SIGUIENTE CIEGA",
            bg_color=C.BTN_GREEN, hover_color=C.BTN_GREEN_HI, font_size=20,
            callback=self.go_next
        )
        self.btn_reroll = Button(
            DESIGN_W // 2 - 90, DESIGN_H - 75, 180, 50, "RENOVAR ($5)",
            bg_color=C.BTN_ORANGE, hover_color=C.BTN_ORANGE_HI, font_size=20,
            callback=self.reroll
        )

        self.buy_buttons = []
        self.buttons = [self.btn_next, self.btn_reroll]

        self.sign_frame = 0
        self.sign_timer = 0.0

    def on_enter(self):
        if self.sound_manager:
            self.sound_manager.switch_music("shop")
        self.generate_shop()

    def generate_shop(self):
        self.shop_items.clear()
        self.joker_sprites.clear()
        self.buy_buttons.clear()

        for i in range(3):
            joker_class = random.choice(ALL_JOKERS)
            joker = joker_class()
            price = get_joker_price(joker)
            self.shop_items.append({'joker': joker, 'price': price, 'sold': False})

        # Create sprites and buy buttons for each shop item
        for i, item in enumerate(self.shop_items):
            x = DESIGN_W // 2 - 220 + i * 170
            y = DESIGN_H // 2 - 80
            js = JokerSprite(x, y, item['joker'], w=CARD_SHOP_W, h=CARD_SHOP_H)
            self.joker_sprites.append(js)

            buy_btn = Button(
                x, y + CARD_SHOP_H + 10, CARD_SHOP_W, 32,
                f"${item['price']}",
                bg_color=C.MONEY_GOLD, hover_color=C.ORANGE,
                text_color=C.BLACK, font_size=16,
                callback=lambda idx=i: self.buy_joker(idx)
            )
            self.buy_buttons.append(buy_btn)

    def buy_joker(self, idx):
        if idx >= len(self.shop_items):
            return
        item = self.shop_items[idx]
        if item['sold']:
            return
        if self.state.dollars < item['price']:
            return
        if len(self.state.jokers) >= self.state.max_jokers:
            return

        self.state.dollars -= item['price']
        self.state.jokers.append(item['joker'])
        item['sold'] = True

        if self.sound_manager:
            self.sound_manager.play_coin()

    def reroll(self):
        if self.state.dollars >= 5:
            self.state.dollars -= 5
            self.generate_shop()

    def go_next(self):
        if self.sound_manager:
            self.sound_manager.switch_music("ingame")
        self.manager.change_screen("blind_select")

    def update(self, dt: float, mouse_pos: tuple[int, int]):
        self.sign_timer += dt
        if self.sign_timer >= 0.2:
            self.sign_timer = 0.0
            self.sign_frame = (self.sign_frame + 1) % 4

        for btn in self.buttons:
            btn.update(dt, mouse_pos)
        for btn in self.buy_buttons:
            btn.update(dt, mouse_pos)
        any_hovered = False
        for js, item in zip(self.joker_sprites, self.shop_items):
            js.update(dt, mouse_pos)
            if js.is_hovered and not item['sold']:
                desc = js.joker.description
                desc_text = " ".join(desc) if isinstance(desc, list) else desc
                self.tooltip.show(js.joker.name, desc_text, mouse_pos[0], mouse_pos[1])
                any_hovered = True

        if not any_hovered:
            self.tooltip.hide()

    def handle_event(self, event: pygame.event.Event):
        for btn in self.buttons:
            btn.handle_event(event)
        for btn in self.buy_buttons:
            btn.handle_event(event)

    def draw(self, surface: pygame.Surface, asset_mgr):
        # Shop sign animation
        sign_img = asset_mgr.shop_sign_frames[self.sign_frame] if asset_mgr.shop_sign_frames else None
        if sign_img:
            scaled_sign = pygame.transform.smoothscale(sign_img, (280, 140))
            surface.blit(scaled_sign, (DESIGN_W // 2 - 140, 15))
        else:
            font_h = asset_mgr.font(44)
            txt = font_h.render("TIENDA", True, C.MONEY_GOLD)
            surface.blit(txt, (DESIGN_W // 2 - txt.get_width() // 2, 40))

        font_med = asset_mgr.font(18)
        font_lg = asset_mgr.font(24)

        # Money display
        money_rect = pygame.Rect(40, 40, 140, 50)
        Panel.draw_panel(surface, money_rect, bg_color=C.PANEL_DARK, border_color=C.MONEY_GOLD)
        t_money = font_lg.render(f"${self.state.dollars}", True, C.MONEY_GOLD)
        surface.blit(t_money, (money_rect.centerx - t_money.get_width() // 2, money_rect.centery - t_money.get_height() // 2))

        # Shop area panel
        shop_panel = pygame.Rect(DESIGN_W // 2 - 280, DESIGN_H // 2 - 130, 560, 310)
        Panel.draw_panel(surface, shop_panel, bg_color=C.PANEL_DARK)

        # Draw joker sprites and buy buttons
        for i, (js, item) in enumerate(zip(self.joker_sprites, self.shop_items)):
            if item['sold']:
                # Draw sold overlay
                sold_rect = pygame.Rect(js.rect.x, js.rect.y, js.rect.width, js.rect.height)
                pygame.draw.rect(surface, C.PANEL_DARK, sold_rect, border_radius=6)
                t_sold = font_med.render("VENDIDO", True, C.D_GREY)
                surface.blit(t_sold, (sold_rect.centerx - t_sold.get_width() // 2, sold_rect.centery - t_sold.get_height() // 2))
            else:
                js.draw(surface, asset_mgr)

        for i, (btn, item) in enumerate(zip(self.buy_buttons, self.shop_items)):
            if not item['sold']:
                can_afford = self.state.dollars >= item['price']
                btn.bg_color = C.MONEY_GOLD if can_afford else C.BTN_DISABLED
                btn.draw(surface, asset_mgr.font(16))

        # Joker count display
        t_jcount = font_med.render(f"Comodines: {len(self.state.jokers)}/{self.state.max_jokers}", True, C.WHITE)
        surface.blit(t_jcount, (DESIGN_W // 2 - t_jcount.get_width() // 2, shop_panel.bottom + 15))

        for btn in self.buttons:
            btn.draw(surface, asset_mgr.font(18))

        self.tooltip.draw(surface, asset_mgr.font(18), asset_mgr.font(14))
