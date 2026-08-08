"""
Entidad representativa de una Carta individual de la baraja.
Merge de poker_clon/entities/card.py + campos de example/core/card.py para renderizado.
"""
from typing import Any
from settings import RANK_CHIPS, Sprite


# Mapeo de rangos largos (poker_clon) a índices de spritesheet (example)
RANK_SHORT = {
    '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7',
    '8': '8', '9': '9', '10': '10', 'Jack': 'J', 'Queen': 'Q', 'King': 'K', 'Ace': 'A',
}

SUITS = ['Hearts', 'Clubs', 'Diamonds', 'Spades']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']


class Card:
    """Clase que representa una carta de póker con su palo, rango y puntuación."""

    ES_RANKS = {'Jack': 'Jota', 'Queen': 'Reina', 'King': 'Rey', 'Ace': 'As'}
    ES_SUITS = {
        'Hearts': 'Corazones',
        'Diamonds': 'Diamantes',
        'Clubs': 'Tréboles',
        'Spades': 'Picas',
    }

    # Constantes de clase para compatibilidad con example
    SUITS = SUITS
    RANKS = RANKS

    def __init__(self, suit: str, rank: str):
        self.suit = suit
        self.rank = rank

        # Índices de spritesheet para renderizado visual
        self.suit_idx = SUITS.index(suit) if suit in SUITS else 0
        short_rank = RANK_SHORT.get(rank, rank)
        self.rank_idx = Sprite.RANK_ORDER.index(short_rank) if short_rank in Sprite.RANK_ORDER else 0

        # Propiedades de ejemplo para compatibilidad visual
        self.edition = "normal"
        self.enhancement = "none"
        self.seal = "none"
        self.debuffed = False

    @property
    def chips(self) -> int:
        """Retorna el valor base en fichas (Chips) de la carta."""
        if getattr(self, 'debuffed', False):
            return 0
        return RANK_CHIPS.get(self.rank, 0)

    @property
    def base_chips(self) -> int:
        """Alias para compatibilidad con example."""
        if self.enhancement == "stone":
            return 50
        c = self.chips
        if self.enhancement == "bonus":
            c += 30
        return c

    @property
    def is_face(self) -> bool:
        """Retorna True si la carta es una figura."""
        return self.rank in ['Jack', 'Queen', 'King']

    @property
    def display_name(self) -> str:
        """Retorna el nombre traducido para visualización en la interfaz."""
        rank_name = self.ES_RANKS.get(self.rank, self.rank)
        suit_name = self.ES_SUITS.get(self.suit, self.suit)
        return f"{rank_name} de {suit_name}"

    def __repr__(self) -> str:
        return self.display_name

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Card):
            return False
        return self.suit == other.suit and self.rank == other.rank

    def __hash__(self):
        return hash((self.suit, self.rank))
