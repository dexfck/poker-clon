"""
Módulo de cálculo e integración del puntaje (Fichas x Multiplicador).
"""
from typing import Any, List, Tuple
from engine.poker_hands import evaluate_hand
from entities.card import Card


def calculate_score(
    played_cards: List[Card], game: Any
) -> Tuple[str, int, int, int]:
    """
    Calcula el puntaje final basado en:
    1. Fichas y Mult base de la mano de póker.
    2. Suma del valor individual de las cartas jugadas.
    3. Aplicación secuencial de los efectos de los Jokers.

    Retorna: (nombre_mano, fichas_finales, mult_final, puntaje_total)
    """
    hand_name, base_chips, base_mult = evaluate_hand(played_cards)

    t_chips = base_chips
    t_mult = base_mult

    for card in played_cards:
        t_chips += card.chips

    context = {
        "cards": played_cards,
        "hand_name": hand_name,
        "game": game,
    }

    for joker in game.jokers:
        t_chips, t_mult = joker.apply(t_chips, t_mult, context)

    total_score = t_chips * t_mult
    return hand_name, t_chips, t_mult, total_score
