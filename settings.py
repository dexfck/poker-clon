"""
Poker2 - Settings & Constants
Merge de example/settings.py (paleta visual) + poker_clon/config/settings.py (lógica y textos).
"""
import os

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
RESOURCES_DIR = os.path.join(BASE_DIR, "resources")
TEXTURES_DIR = os.path.join(RESOURCES_DIR, "textures", "2x")
FONTS_DIR = os.path.join(RESOURCES_DIR, "fonts")
SOUNDS_DIR = os.path.join(RESOURCES_DIR, "sounds")

# Assets de poker_clon (para música sincronizada)
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
SOUND_DIR = os.path.join(ASSETS_DIR, "sound")

# ---------------------------------------------------------------------------
# Display
# ---------------------------------------------------------------------------
DESIGN_W = 1280
DESIGN_H = 720
FPS = 60

# Alias de compatibilidad
WINDOW_WIDTH = DESIGN_W
WINDOW_HEIGHT = DESIGN_H

# ---------------------------------------------------------------------------
# Volume Defaults
# ---------------------------------------------------------------------------
MUSIC_VOLUME = 0.4
SFX_VOLUME = 0.6

# ---------------------------------------------------------------------------
# Balatro Color Palette (RGB tuples)
# ---------------------------------------------------------------------------
class C:
    """All colors used across the UI."""
    # Backgrounds
    BG_DARK      = (27, 27, 47)
    BG_DARKER    = (15, 15, 26)
    BG_TABLE     = (26, 74, 52)

    # Scoring
    MULT_RED     = (254, 95, 85)
    CHIPS_BLUE   = (0, 157, 255)
    MONEY_GOLD   = (243, 185, 88)

    # UI accents
    GREEN        = (75, 194, 146)
    ORANGE       = (255, 154, 0)
    PURPLE       = (138, 99, 210)

    # Card colors
    CARD_WHITE   = (245, 245, 240)
    SUIT_RED     = (232, 83, 74)
    SUIT_CLUB    = (38, 117, 80)
    SUIT_DIAMOND = (232, 131, 61)
    SUIT_SPADE   = (57, 57, 94)

    # Sidebar HUD Chrome
    SIDEBAR_BG     = (34, 34, 36)
    SIDEBAR_INNER  = (22, 22, 24)
    SIDEBAR_BORDER = (220, 150, 35)
    BLIND_GOLD     = (200, 130, 25)

    # Panels / UI chrome
    PANEL_BG     = (42, 42, 61)
    PANEL_LIGHT  = (55, 55, 78)
    PANEL_BORDER = (70, 70, 100)
    PANEL_DARK   = (25, 25, 40)

    # Buttons
    BTN_BLUE       = (0, 120, 210)
    BTN_BLUE_HI    = (30, 150, 240)
    BTN_RED        = (190, 50, 50)
    BTN_RED_HI     = (230, 70, 70)
    BTN_GREEN      = (50, 150, 90)
    BTN_GREEN_HI   = (70, 185, 115)
    BTN_ORANGE     = (200, 120, 30)
    BTN_ORANGE_HI  = (240, 145, 45)
    BTN_DISABLED   = (75, 75, 85)

    # Text
    WHITE  = (255, 255, 255)
    BLACK  = (0, 0, 0)
    GREY   = (140, 140, 150)
    L_GREY = (200, 200, 210)
    D_GREY = (80, 80, 90)

    # Rarity colors
    COMMON   = (0, 120, 210)
    UNCOMMON = (75, 194, 146)
    RARE     = (254, 95, 85)
    LEGENDARY = (138, 99, 210)

    # Green felt vortex colors (float 0-1)
    VORTEX_1 = (0.08, 0.26, 0.17)
    VORTEX_2 = (0.04, 0.16, 0.10)
    VORTEX_3 = (0.12, 0.32, 0.20)

    # Boss blind background
    BOSS_1 = (0.25, 0.05, 0.08)
    BOSS_2 = (0.15, 0.02, 0.15)
    BOSS_3 = (0.30, 0.08, 0.04)

# Alias de compatibilidad con poker_clon
COLOR_WHITE = C.WHITE
COLOR_BLACK = C.BLACK
COLOR_MULT_RED = C.MULT_RED
COLOR_CHIPS_BLUE = C.CHIPS_BLUE

# ---------------------------------------------------------------------------
# Sprite-sheet tile sizes
# ---------------------------------------------------------------------------
class Sprite:
    CARD_W   = 142
    CARD_H   = 190

    DECK_COLS = 13
    DECK_ROWS = 4
    RANK_ORDER = ['2','3','4','5','6','7','8','9','10','J','Q','K','A']
    SUIT_ORDER = ['Hearts','Clubs','Diamonds','Spades']

    JOKER_COLS = 10
    JOKER_ROWS = 16

    TAROT_COLS = 10
    TAROT_ROWS = 6

    ENH_COLS = 7
    ENH_ROWS = 5

    VOUCHER_COLS = 9
    VOUCHER_ROWS = 4

    BOOSTER_COLS = 4
    BOOSTER_ROWS = 9

    BLIND_CHIP_W = 68
    BLIND_CHIP_H = 68
    BLIND_COLS   = 14

    CHIP_SIZE = 58
    CHIP_COLS = 5
    CHIP_ROWS = 2

    TAG_W    = 58
    TAG_H    = 68
    TAG_COLS = 7
    TAG_ROWS = 5

    SHOP_SIGN_W = 226
    SHOP_SIGN_H = 114
    SHOP_SIGN_FRAMES = 4

    STICKER_COLS = 5
    STICKER_ROWS = 3

# ---------------------------------------------------------------------------
# UI layout constants
# ---------------------------------------------------------------------------
CARD_DISPLAY_W = 98
CARD_DISPLAY_H = 130

CARD_SHOP_W = 110
CARD_SHOP_H = 148

CARD_SMALL_W = 53
CARD_SMALL_H = 71

LEFT_PANEL_W = 260

# Sprite settings de poker_clon (para compatibilidad)
CARD_WIDTH = 71
CARD_HEIGHT = 95

# ---------------------------------------------------------------------------
# Textos UI (Español)
# ---------------------------------------------------------------------------
TXT_PLAY_HAND = "Jugar mano"
TXT_DISCARD = "Descartar"
TXT_SORT_RANK = "Rango"
TXT_SORT_SUIT = "Palo"
TXT_SCORE = "Fichas"
TXT_HANDS = "Manos"
TXT_DISCARDS = "Descartes"
TXT_GAME_OVER = "FIN DE LA PARTIDA"
TXT_ROUND_WON = "¡CIEGA SUPERADA!"
TXT_FINAL_SCORE = "Puntaje Final"
TXT_SHOP = "Tienda"
TXT_REROLL = "Renovar"
TXT_NEXT = "Siguiente Ciega"

# ---------------------------------------------------------------------------
# Poker hand definitions (en español, valores de poker_clon)
# ---------------------------------------------------------------------------
HAND_LEVELS = {
    "Escalera de color": (100, 8),
    "Póker": (60, 7),
    "Full": (40, 4),
    "Color": (35, 4),
    "Escalera": (30, 4),
    "Trío": (30, 3),
    "Doble pareja": (20, 2),
    "Pareja": (10, 2),
    "Carta alta": (5, 1),
}

RANK_CHIPS = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
    '8': 8, '9': 9, '10': 10, 'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11,
}

RANK_VALUES = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
    '8': 8, '9': 9, '10': 10, 'Jack': 11, 'Queen': 12, 'King': 13, 'Ace': 14,
}

# ---------------------------------------------------------------------------
# Ante score progression
# ---------------------------------------------------------------------------
ANTE_SCORES = {
    1: (300,   450,   800),
    2: (800,   1200,  2000),
    3: (2800,  4000,  6000),
    4: (6000,  9000,  14000),
    5: (12000, 18000, 28000),
    6: (24000, 36000, 56000),
    7: (50000, 75000, 110000),
    8: (110000, 160000, 240000),
}

# ---------------------------------------------------------------------------
# Names lists (for example design compatibility)
# ---------------------------------------------------------------------------
JOKER_NAMES = [
    "Comodín", "Comodín Avaricioso", "Comodín Lujurioso", "Comodín Iracundo",
    "Comodín Glotón", "Comodín Alegre", "Comodín Loco", "Comodín Furioso",
    "Comodín Loco de Remate", "Comodín Gracioso", "Comodín Astuto", "Comodín Hábil",
    "Comodín Inteligente", "Comodín Tortuoso", "Comodín Ingenioso", "Medio Comodín",
    "Joker Stencil", "Four Fingers", "Mime", "Credit Card",
    "Ceremonial Dagger", "Estandarte", "Cumbre Mística", "Marble Joker",
]

BOSS_BLIND_NAMES = [
    "El Anzuelo", "El Pilar", "La Rueda", "El Muro", "La Ventana",
]

DECK_INFO = [
    ("Red Deck",      "+1 Descarte por ronda"),
    ("Blue Deck",     "+1 Mano por ronda"),
    ("Yellow Deck",   "Empiezas con $10 extra"),
    ("Green Deck",    "Sin interés. $1 por mano restante, $1 por descarte restante"),
]

VOUCHER_NAMES = [
    "Overstock", "Clearance Sale", "Hone", "Reroll Surplus",
    "Crystal Ball", "Telescope", "Nacho Tong", "Recyclomancy",
    "Overstock Plus", "Liquidation", "Glow Up", "Reroll Glut",
    "Omen Globe", "Observatory", "Wasteful", "Tarot Tycoon",
    "Planet Tycoon", "Money Tree", "Antimatter", "Illusion",
    "Petroglyph", "Retcon", "Palette", "Paint Brush",
]
