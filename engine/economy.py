"""
Módulo de cálculo de economía (Recompensas por ronda, intereses, precios de tienda).
"""
from typing import Any


def calculate_round_reward(blind_reward: int, remaining_hands: int) -> int:
    """Calcula la recompensa ganada al superar una ciega."""
    return blind_reward + remaining_hands


def calculate_interest(money: int) -> int:
    """Calcula el interés ganado al final de la ronda ($1 por cada $5, máximo $5)."""
    return min(money // 5, 5)


def get_joker_price(joker: Any) -> int:
    """Retorna el precio de un comodín en la tienda."""
    if hasattr(joker, 'cost'):
        return joker.cost
    return 4
