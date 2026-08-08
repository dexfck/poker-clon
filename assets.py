"""
Poker2 - Asset Manager
Loads and slices all sprite sheets, fonts, and sounds.
Basado en example/assets.py con paths adaptados.
"""
import os
import pygame
from PIL import Image
from settings import TEXTURES_DIR, FONTS_DIR, SOUNDS_DIR, Sprite, CARD_DISPLAY_W, CARD_DISPLAY_H


class FallbackFont:
    """Safe fallback font renderer when SDL_ttf / pygame.font is unavailable."""

    def __init__(self, size):
        self.pt_size = size

    def render(self, text, antialias, color, background=None):
        w = max(len(text) * (self.pt_size // 2 + 1), 1)
        h = max(self.pt_size, 1)
        surf = pygame.Surface((w, h), pygame.SRCALPHA)
        if background:
            surf.fill(background)
        for i, char in enumerate(text):
            cx = i * (self.pt_size // 2 + 1)
            pygame.draw.rect(surf, color, (cx, 2, self.pt_size // 2, h - 4), width=1)
        return surf

    def size(self, text):
        return (len(text) * (self.pt_size // 2 + 1), self.pt_size)


class AssetManager:
    """Centralised asset loader — call load() after pygame.display is initialised."""

    def __init__(self):
        self.cards = {}
        self.jokers = []
        self.tarots = []
        self.enhancers = []
        self.vouchers = []
        self.boosters = []
        self.blind_chips = []
        self.blind_chips_cache = {}
        self.blind_sheet_surf = None
        self.chips = []
        self.tags = []
        self.shop_sign_frames = []
        self.stickers = []
        self.card_back = None
        self.logo = None
        self.logo_alt = None
        self.font_path = os.path.join(FONTS_DIR, "m6x11plus.ttf")
        self.fonts = {}
        self.sounds = {}
        self._loaded = False

    def load(self):
        """Must be called after pygame.display.set_mode()."""
        if self._loaded:
            return
        try:
            if hasattr(pygame, 'font') and not pygame.font.get_init():
                pygame.font.init()
        except Exception:
            pass

        self._load_spritesheets()
        self._load_logo()
        self._load_sounds()
        self._loaded = True

    def font(self, size: int):
        """Return cached font at the requested pixel size."""
        if size not in self.fonts:
            try:
                self.fonts[size] = pygame.font.Font(self.font_path, size)
            except Exception:
                try:
                    self.fonts[size] = pygame.font.SysFont("monospace", size, bold=True)
                except Exception:
                    self.fonts[size] = FallbackFont(size)
        return self.fonts[size]

    def get_card(self, suit_row: int, rank_col: int, size=None):
        key = (suit_row, rank_col)
        surf = self.cards.get(key)
        if surf is None:
            return None
        if size and size != (surf.get_width(), surf.get_height()):
            return pygame.transform.smoothscale(surf, size)
        return surf

    def get_joker(self, index: int, size=None):
        if index < 0 or index >= len(self.jokers):
            return None
        surf = self.jokers[index]
        if size:
            return pygame.transform.smoothscale(surf, size)
        return surf

    def get_tarot(self, index: int, size=None):
        if index < 0 or index >= len(self.tarots):
            return None
        surf = self.tarots[index]
        if size:
            return pygame.transform.smoothscale(surf, size)
        return surf

    def get_voucher(self, index: int, size=None):
        if index < 0 or index >= len(self.vouchers):
            return None
        surf = self.vouchers[index]
        if size:
            return pygame.transform.smoothscale(surf, size)
        return surf

    def get_booster(self, index: int, size=None):
        if index < 0 or index >= len(self.boosters):
            return None
        surf = self.boosters[index]
        if size:
            return pygame.transform.smoothscale(surf, size)
        return surf

    def get_blind_chip(self, col=0, row=0, size=None):
        if isinstance(col, tuple):
            col, row = col[0], col[1]
        if isinstance(row, tuple):
            size = row
            row = 0
            if col == 1:
                row = 1
            elif col == 2:
                row = 2

        key = (col, row)
        if key not in self.blind_chips_cache:
            if hasattr(self, 'blind_sheet_surf') and self.blind_sheet_surf:
                x = col * 68
                y = row * 68
                if x + 68 <= self.blind_sheet_surf.get_width() and y + 68 <= self.blind_sheet_surf.get_height():
                    self.blind_chips_cache[key] = self.blind_sheet_surf.subsurface(pygame.Rect(x, y, 68, 68)).copy()
                else:
                    return None
            else:
                return None

        surf = self.blind_chips_cache.get(key)
        if surf and size and size != (surf.get_width(), surf.get_height()):
            return pygame.transform.smoothscale(surf, size)
        return surf

    def play_sound(self, name: str, volume: float = 0.5):
        if name in self.sounds and self.sounds[name]:
            try:
                self.sounds[name].set_volume(volume)
                self.sounds[name].play()
            except Exception:
                pass

    def _load_image(self, filename: str) -> pygame.Surface:
        path = os.path.join(TEXTURES_DIR, filename)
        if not os.path.exists(path):
            return pygame.Surface((1, 1), pygame.SRCALPHA)

        try:
            pil_img = Image.open(path).convert("RGBA")
            data = pil_img.tobytes()
            size = pil_img.size
            return pygame.image.fromstring(data, size, "RGBA").convert_alpha()
        except Exception:
            return pygame.Surface((1, 1), pygame.SRCALPHA)

    def _slice_grid(self, sheet: pygame.Surface, cols: int, rows: int,
                    tw: int, th: int) -> list:
        tiles = []
        for r in range(rows):
            for c in range(cols):
                rect = pygame.Rect(c * tw, r * th, tw, th)
                tile = sheet.subsurface(rect).copy()
                tiles.append(tile)
        return tiles

    def _load_spritesheets(self):
        S = Sprite

        # --- Playing cards (8BitDeck_opt2.png - High Contrast) ---
        deck_sheet = self._load_image("8BitDeck_opt2.png")
        if deck_sheet.get_width() <= 1:
            deck_sheet = self._load_image("8BitDeck.png")
        for row in range(S.DECK_ROWS):
            for col in range(S.DECK_COLS):
                rect = pygame.Rect(col * S.CARD_W, row * S.CARD_H,
                                   S.CARD_W, S.CARD_H)
                self.cards[(row, col)] = deck_sheet.subsurface(rect).copy()

        # --- Jokers ---
        joker_sheet = self._load_image("Jokers.png")
        self.jokers = self._slice_grid(joker_sheet, S.JOKER_COLS,
                                       S.JOKER_ROWS, S.CARD_W, S.CARD_H)

        # --- Tarots / Planets / Spectrals ---
        tarot_sheet = self._load_image("Tarots.png")
        self.tarots = self._slice_grid(tarot_sheet, S.TAROT_COLS,
                                       S.TAROT_ROWS, S.CARD_W, S.CARD_H)

        # --- Enhancers ---
        enh_sheet = self._load_image("Enhancers.png")
        self.enhancers = self._slice_grid(enh_sheet, S.ENH_COLS,
                                          S.ENH_ROWS, S.CARD_W, S.CARD_H)
        if self.enhancers:
            self.card_back = self.enhancers[0]

        # --- Vouchers ---
        voucher_sheet = self._load_image("Vouchers.png")
        self.vouchers = self._slice_grid(voucher_sheet, S.VOUCHER_COLS,
                                         S.VOUCHER_ROWS, S.CARD_W, S.CARD_H)

        # --- Boosters ---
        booster_sheet = self._load_image("boosters.png")
        self.boosters = self._slice_grid(booster_sheet, S.BOOSTER_COLS,
                                         S.BOOSTER_ROWS, S.CARD_W, S.CARD_H)

        # --- Blind chips ---
        self.blind_sheet_surf = self._load_image("BlindChips.png")

        # --- Poker chips ---
        chip_sheet = self._load_image("chips.png")
        self.chips = self._slice_grid(chip_sheet, S.CHIP_COLS, S.CHIP_ROWS,
                                      S.CHIP_SIZE, S.CHIP_SIZE)

        # --- Tags ---
        tag_sheet = self._load_image("tags.png")
        self.tags = self._slice_grid(tag_sheet, S.TAG_COLS, S.TAG_ROWS,
                                     S.TAG_W, S.TAG_H)

        # --- Shop sign animation ---
        sign_sheet = self._load_image("ShopSignAnimation.png")
        for i in range(S.SHOP_SIGN_FRAMES):
            rect = pygame.Rect(i * S.SHOP_SIGN_W, 0,
                               S.SHOP_SIGN_W, S.SHOP_SIGN_H)
            self.shop_sign_frames.append(sign_sheet.subsurface(rect).copy())

        # --- Stickers ---
        stk_sheet = self._load_image("stickers.png")
        self.stickers = self._slice_grid(stk_sheet, S.STICKER_COLS,
                                         S.STICKER_ROWS, S.CARD_W, S.CARD_H)

    def _load_logo(self):
        self.logo = self._load_image("balatro.png")
        self.logo_alt = self._load_image("balatro_alt.png")

    def _load_sounds(self):
        if not os.path.isdir(SOUNDS_DIR):
            return
        for fn in os.listdir(SOUNDS_DIR):
            if fn.endswith(".ogg"):
                name = fn[:-4]
                path = os.path.join(SOUNDS_DIR, fn)
                try:
                    if hasattr(pygame, 'mixer') and pygame.mixer.get_init():
                        self.sounds[name] = pygame.mixer.Sound(path)
                except Exception:
                    pass
