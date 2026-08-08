"""
Definición de comodines (Jokers) y sus efectos sobre la puntuación.
Copiado de poker_clon/entities/joker.py con adición de campos para renderizado visual.
"""
from typing import Any, Dict, List, Tuple


# Mapeo de raridad numérica a nombre
RARITY_NAMES = {1: "Common", 2: "Uncommon", 3: "Rare", 4: "Legendary"}


class JokerBase:
    """Clase base abstracta para todos los comodines del juego."""

    def __init__(
        self,
        name: str,
        description: List[str],
        col: int,
        row: int,
        rarity: int = 1,
    ):
        self.name = name
        self.description = description
        self.col = col
        self.row = row
        self.rarity = rarity

        # Campos para compatibilidad con el sistema visual de example
        self.sprite_idx = row * 10 + col  # Índice lineal en la spritesheet de jokers
        self.rarity_name = RARITY_NAMES.get(rarity, "Common")
        self.cost = 4 + (rarity - 1) * 2
        self.sell_value = max(1, self.cost // 2)
        self.edition = "normal"
        self.pinned = False

    def apply(
        self, chips: int, mult: int, context: Dict[str, Any]
    ) -> Tuple[int, int]:
        """Aplica el efecto del comodín sobre las fichas y multiplicador actuales."""
        return chips, mult


class Comodin(JokerBase):
    def __init__(self):
        super().__init__("Comodín", ["+4 Mult"], 0, 0, 1)

    def apply(self, chips: int, mult: int, context: Dict[str, Any]) -> Tuple[int, int]:
        return chips, mult + 4


class Avaricioso(JokerBase):
    def __init__(self):
        super().__init__(
            "Comodín Avaricioso", ["+3 Mult por", "carta jugada de Diamante"], 1, 0, 1
        )

    def apply(self, chips: int, mult: int, context: Dict[str, Any]) -> Tuple[int, int]:
        bonus = sum(3 for c in context['cards'] if c.suit == 'Diamonds' and not getattr(c, 'debuffed', False))
        return chips, mult + bonus


class Lujurioso(JokerBase):
    def __init__(self):
        super().__init__(
            "Comodín Lujurioso", ["+3 Mult por", "carta jugada de Corazones"], 2, 0, 1
        )

    def apply(self, chips: int, mult: int, context: Dict[str, Any]) -> Tuple[int, int]:
        bonus = sum(3 for c in context['cards'] if c.suit == 'Hearts' and not getattr(c, 'debuffed', False))
        return chips, mult + bonus


class Iracundo(JokerBase):
    def __init__(self):
        super().__init__(
            "Comodín Iracundo", ["+3 Mult por", "carta jugada de Picas"], 3, 0, 1
        )

    def apply(self, chips: int, mult: int, context: Dict[str, Any]) -> Tuple[int, int]:
        bonus = sum(3 for c in context['cards'] if c.suit == 'Spades' and not getattr(c, 'debuffed', False))
        return chips, mult + bonus


class Gloton(JokerBase):
    def __init__(self):
        super().__init__(
            "Comodín Glotón", ["+3 Mult por", "carta jugada de Tréboles"], 4, 0, 1
        )

    def apply(self, chips: int, mult: int, context: Dict[str, Any]) -> Tuple[int, int]:
        bonus = sum(3 for c in context['cards'] if c.suit == 'Clubs' and not getattr(c, 'debuffed', False))
        return chips, mult + bonus


class Alegre(JokerBase):
    def __init__(self):
        super().__init__(
            "Comodín Alegre", ["+8 Mult si la mano", "contiene una Pareja"], 5, 0, 1
        )

    def apply(self, chips: int, mult: int, context: Dict[str, Any]) -> Tuple[int, int]:
        if context['hand_name'] in ["Pareja", "Doble pareja", "Full", "Póker"]:
            return chips, mult + 8
        return chips, mult


class Loco(JokerBase):
    def __init__(self):
        super().__init__(
            "Comodín Loco", ["+12 Mult si la mano", "contiene un Trío"], 6, 0, 1
        )

    def apply(self, chips: int, mult: int, context: Dict[str, Any]) -> Tuple[int, int]:
        if context['hand_name'] in ["Trío", "Full", "Póker"]:
            return chips, mult + 12
        return chips, mult


class Furioso(JokerBase):
    def __init__(self):
        super().__init__(
            "Comodín Furioso", ["+10 Mult si la mano", "contiene Doble pareja"], 7, 0, 1
        )

    def apply(self, chips: int, mult: int, context: Dict[str, Any]) -> Tuple[int, int]:
        if context['hand_name'] == "Doble pareja":
            return chips, mult + 10
        return chips, mult


class LocoRemate(JokerBase):
    def __init__(self):
        super().__init__(
            "Comodín Loco de Remate",
            ["+12 Mult si la mano", "contiene una Escalera"],
            8,
            0,
            1,
        )

    def apply(self, chips: int, mult: int, context: Dict[str, Any]) -> Tuple[int, int]:
        if context['hand_name'] in ["Escalera", "Escalera de color", "Escalera real"]:
            return chips, mult + 12
        return chips, mult


class Gracioso(JokerBase):
    def __init__(self):
        super().__init__(
            "Comodín Gracioso", ["+10 Mult si la mano", "contiene Color"], 9, 0, 1
        )

    def apply(self, chips: int, mult: int, context: Dict[str, Any]) -> Tuple[int, int]:
        if context['hand_name'] in ["Color", "Escalera de color", "Escalera real"]:
            return chips, mult + 10
        return chips, mult


class Astuto(JokerBase):
    def __init__(self):
        super().__init__(
            "Comodín Astuto", ["+50 Fichas si la mano", "contiene Pareja"], 0, 1, 1
        )

    def apply(self, chips: int, mult: int, context: Dict[str, Any]) -> Tuple[int, int]:
        if context['hand_name'] in ["Pareja", "Doble pareja", "Full", "Póker"]:
            return chips + 50, mult
        return chips, mult


class Habil(JokerBase):
    def __init__(self):
        super().__init__(
            "Comodín Hábil", ["+100 Fichas si la mano", "contiene Trío"], 1, 1, 1
        )

    def apply(self, chips: int, mult: int, context: Dict[str, Any]) -> Tuple[int, int]:
        if context['hand_name'] in ["Trío", "Full", "Póker"]:
            return chips + 100, mult
        return chips, mult


class Inteligente(JokerBase):
    def __init__(self):
        super().__init__(
            "Comodín Inteligente",
            ["+80 Fichas si la mano", "contiene Doble pareja"],
            2,
            1,
            1,
        )

    def apply(self, chips: int, mult: int, context: Dict[str, Any]) -> Tuple[int, int]:
        if context['hand_name'] == "Doble pareja":
            return chips + 80, mult
        return chips, mult


class Tortuoso(JokerBase):
    def __init__(self):
        super().__init__(
            "Comodín Tortuoso", ["+100 Fichas si la mano", "contiene Escalera"], 3, 1, 1
        )

    def apply(self, chips: int, mult: int, context: Dict[str, Any]) -> Tuple[int, int]:
        if context['hand_name'] in ["Escalera", "Escalera de color", "Escalera real"]:
            return chips + 100, mult
        return chips, mult


class Ingenioso(JokerBase):
    def __init__(self):
        super().__init__(
            "Comodín Ingenioso", ["+80 Fichas si la mano", "contiene Color"], 4, 1, 1
        )

    def apply(self, chips: int, mult: int, context: Dict[str, Any]) -> Tuple[int, int]:
        if context['hand_name'] in ["Color", "Escalera de color", "Escalera real"]:
            return chips + 80, mult
        return chips, mult


class MedioComodin(JokerBase):
    def __init__(self):
        super().__init__(
            "Medio Comodín",
            ["+20 Mult si la mano", "jugada tiene 3", "o menos cartas"],
            5,
            1,
            1,
        )

    def apply(self, chips: int, mult: int, context: Dict[str, Any]) -> Tuple[int, int]:
        if len(context['cards']) <= 3:
            return chips, mult + 20
        return chips, mult


class GrosMichel(JokerBase):
    def __init__(self):
        super().__init__(
            "Gros Michel",
            ["+15 Mult", "1 probabilidad en 6 de", "destruirse al fin de ronda"],
            7,
            6,
            1,
        )

    def apply(self, chips: int, mult: int, context: Dict[str, Any]) -> Tuple[int, int]:
        return chips, mult + 15


class Cavendish(JokerBase):
    def __init__(self):
        super().__init__(
            "Cavendish",
            ["X3 Mult", "1 probabilidad en 1000 de", "destruirse al fin de ronda"],
            4,
            11,
            3,
        )

    def apply(self, chips: int, mult: int, context: Dict[str, Any]) -> Tuple[int, int]:
        return chips, mult * 3


class Estandarte(JokerBase):
    def __init__(self):
        super().__init__(
            "Estandarte", ["+30 Fichas por cada", "descarte restante"], 1, 2, 1
        )

    def apply(self, chips: int, mult: int, context: Dict[str, Any]) -> Tuple[int, int]:
        game = context['game']
        descartes = getattr(game, 'discards_left', 0)
        return chips + (30 * descartes), mult


class CumbreMistica(JokerBase):
    def __init__(self):
        super().__init__(
            "Cumbre Mística", ["+15 Mult cuando quedan", "0 descartes"], 2, 2, 1
        )

    def apply(self, chips: int, mult: int, context: Dict[str, Any]) -> Tuple[int, int]:
        game = context['game']
        if getattr(game, 'discards_left', 0) <= 0:
            return chips, mult + 15
        return chips, mult


class Acrobata(JokerBase):
    def __init__(self):
        super().__init__(
            "Acróbata", ["X3 Mult en la última", "mano de la ronda"], 5, 14, 2
        )

    def apply(self, chips: int, mult: int, context: Dict[str, Any]) -> Tuple[int, int]:
        game = context['game']
        if getattr(game, 'hands_left', 0) <= 0:
            return chips, mult * 3
        return chips, mult


class Equis(JokerBase):
    def __init__(self):
        super().__init__(
            "Comodín Equis", ["+4 Mult por cada carta", "jugada de rango par"], 8, 3, 1
        )

    def apply(self, chips: int, mult: int, context: Dict[str, Any]) -> Tuple[int, int]:
        pares = ['2', '4', '6', '8', '10']
        bonus = sum(4 for c in context['cards'] if c.rank in pares and not getattr(c, 'debuffed', False))
        return chips, mult + bonus


class Impar(JokerBase):
    def __init__(self):
        super().__init__(
            "Comodín Impar",
            ["+30 Fichas por cada carta", "jugada impar"],
            9,
            3,
            1,
        )

    def apply(self, chips: int, mult: int, context: Dict[str, Any]) -> Tuple[int, int]:
        impares = ['Ace', '3', '5', '7', '9']
        bonus = sum(30 for c in context['cards'] if c.rank in impares and not getattr(c, 'debuffed', False))
        return chips + bonus, mult


class RostroSonriente(JokerBase):
    def __init__(self):
        super().__init__(
            "Rostro Sonriente",
            ["+5 Mult por cada carta", "jugada de figura"],
            6,
            15,
            1,
        )

    def apply(self, chips: int, mult: int, context: Dict[str, Any]) -> Tuple[int, int]:
        figuras = ['Jack', 'Queen', 'King']
        bonus = sum(5 for c in context['cards'] if c.rank in figuras and not getattr(c, 'debuffed', False))
        return chips, mult + bonus


class Abstracto(JokerBase):
    def __init__(self):
        super().__init__(
            "Comodín Abstracto",
            ["+3 Mult por cada", "comodín poseído"],
            4,
            3,
            1,
        )

    def apply(self, chips: int, mult: int, context: Dict[str, Any]) -> Tuple[int, int]:
        game = context['game']
        jokers_count = len(game.jokers)
        return chips, mult + (3 * jokers_count)


ALL_JOKERS = [
    Comodin,
    Avaricioso,
    Lujurioso,
    Iracundo,
    Gloton,
    Alegre,
    Loco,
    Furioso,
    LocoRemate,
    Gracioso,
    Astuto,
    Habil,
    Inteligente,
    Tortuoso,
    Ingenioso,
    MedioComodin,
    GrosMichel,
    Cavendish,
    Estandarte,
    CumbreMistica,
    Acrobata,
    Equis,
    Impar,
    RostroSonriente,
    Abstracto,
]
