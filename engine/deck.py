"""
Módulo para la representación y manipulación de la Baraja (Deck) de cartas.
"""
import random
from typing import List
from entities.card import Card, SUITS, RANKS


class Deck:
    """Representa la baraja estándar de 52 cartas."""

    def __init__(self):
        self.cards: List[Card] = self._generate_deck()
        self.shuffle()

    def _generate_deck(self) -> List[Card]:
        """Genera las 52 cartas ordenadas."""
        return [Card(suit, rank) for suit in SUITS for rank in RANKS]

    def shuffle(self) -> None:
        """Baraja aleatoriamente el mazo."""
        random.shuffle(self.cards)

    def draw(self, count: int = 1) -> List[Card]:
        """Roba una cantidad 'count' de cartas de la baraja."""
        drawn_cards = []
        for _ in range(count):
            if self.cards:
                drawn_cards.append(self.cards.pop(0))
        return drawn_cards

    def __len__(self) -> int:
        return len(self.cards)
