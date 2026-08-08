"""
Módulo de gestión de Ciegas (Small, Big y Boss Blinds) y progreso de Antes.
"""
import random
from typing import Any, Dict

BOSS_BLINDS = [
    {
        "name": "El Anzuelo",
        "desc": "Descarta 2 cartas aleatorias\npor mano jugada.",
        "row": 2,
        "col": 0,
    },
    {
        "name": "El Pilar",
        "desc": "Las cartas jugadas en este\nAnte están debilitadas.",
        "row": 2,
        "col": 1,
    },
    {
        "name": "La Rueda",
        "desc": "1 de cada 7 cartas\nse roba boca abajo.",
        "row": 2,
        "col": 2,
    },
    {"name": "El Muro", "desc": "Ciega extra grande.", "row": 2, "col": 3},
    {
        "name": "La Ventana",
        "desc": "Todas las figuras están\ndebilitadas.",
        "row": 3,
        "col": 0,
    },
]


class BlindManager:
    """Gestiona el progreso por Ante y el estado de la ciega actual."""

    def __init__(self):
        self.ante = 1
        self.current_blind = "Small"  # Small, Big, Boss
        self.current_boss = random.choice(BOSS_BLINDS)

        self.base_scores = {
            1: 300,
            2: 800,
            3: 2000,
            4: 5000,
            5: 11000,
            6: 20000,
            7: 35000,
            8: 50000,
        }

    def get_blind_info(self) -> Dict[str, Any]:
        """Retorna la información y requisitos de la ciega actual."""
        base = self.base_scores.get(self.ante, self.base_scores[8] * (self.ante - 7))

        if self.current_blind == "Small":
            return {
                "name": "Ciega Pequeña",
                "target": base,
                "reward": 3,
                "color": (50, 100, 220),
                "row": 0,
                "col": 0,
                "desc": None,
            }
        elif self.current_blind == "Big":
            return {
                "name": "Ciega Grande",
                "target": int(base * 1.5),
                "reward": 4,
                "color": (220, 190, 40),
                "row": 1,
                "col": 0,
                "desc": None,
            }
        else:
            mult = 4 if self.current_boss["name"] == "El Muro" else 2
            return {
                "name": self.current_boss["name"],
                "target": base * mult,
                "reward": 5,
                "color": (220, 50, 50),
                "row": self.current_boss["row"],
                "col": self.current_boss["col"],
                "desc": self.current_boss["desc"],
            }

    def advance_blind(self) -> None:
        """Avanza a la siguiente ciega o al siguiente Ante."""
        if self.current_blind == "Small":
            self.current_blind = "Big"
        elif self.current_blind == "Big":
            self.current_blind = "Boss"
        else:
            self.current_blind = "Small"
            self.ante += 1
            self.current_boss = random.choice(BOSS_BLINDS)
