"""
Evaluador de manos de póker y tabla de niveles/puntuaciones base.
"""
from collections import Counter
from typing import List, Tuple
from entities.card import Card
from settings import RANK_VALUES, HAND_LEVELS


def evaluate_hand(cards: List[Card]) -> Tuple[str, int, int]:
    """
    Evalúa una mano de hasta 5 cartas y devuelve la mejor jugada de póker.
    Retorna: (Nombre de la Mano, Fichas Base, Multiplicador Base)
    """
    if not cards:
        return "Carta alta", 0, 0

    ranks = [c.rank for c in cards]
    suits = [c.suit for c in cards]

    rank_counts = Counter(ranks)
    counts = sorted(rank_counts.values(), reverse=True)

    is_flush = len(set(suits)) == 1 and len(cards) == 5

    is_straight = False
    if len(cards) == 5 and len(set(ranks)) == 5:
        sorted_values = sorted([RANK_VALUES[r] for r in ranks])
        if sorted_values == list(range(sorted_values[0], sorted_values[0] + 5)):
            is_straight = True
        elif sorted_values == [2, 3, 4, 5, 14]:
            is_straight = True

    hand_type = "Carta alta"

    if is_flush and is_straight:
        hand_type = "Escalera de color"
    elif counts == [4, 1] or counts == [4]:
        hand_type = "Póker"
    elif counts == [3, 2]:
        hand_type = "Full"
    elif is_flush:
        hand_type = "Color"
    elif is_straight:
        hand_type = "Escalera"
    elif counts and counts[0] == 3:
        hand_type = "Trío"
    elif len(counts) >= 2 and counts[:2] == [2, 2]:
        hand_type = "Doble pareja"
    elif counts and counts[0] == 2:
        hand_type = "Pareja"

    base_chips, base_mult = HAND_LEVELS[hand_type]
    return hand_type, base_chips, base_mult
