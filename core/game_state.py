"""
GameState integrado: estructura de example/core/game_state.py con lógica real de poker_clon.
Usa BlindManager, Deck, economía y Jokers con efectos reales.
"""
import random
from entities.card import Card, SUITS, RANKS
from entities.joker import ALL_JOKERS, JokerBase
from engine.blinds import BlindManager
from engine.deck import Deck
from engine.economy import calculate_round_reward, calculate_interest, get_joker_price
from settings import ANTE_SCORES, RANK_VALUES


class GameState:
    def __init__(self):
        self.reset_run()

    def reset_run(self, deck_idx=0):
        # Blind management (lógica real de poker_clon)
        self.blind_manager = BlindManager()
        self.ante = 1
        self.round = 1
        self.blind_state = "Small"  # 'Small', 'Big', 'Boss'

        # Economy
        self.dollars = 2

        # Hand limits
        self.hands_left = 4
        self.discards_left = 3
        self.max_hands = 4
        self.max_discards = 3
        self.hands_played = 0
        self.discards_used = 0

        # Score
        self.current_score = 0
        info = self.blind_manager.get_blind_info()
        self.target_score = info["target"]
        self.boss_name = self.blind_manager.current_boss["name"]

        # Inventory — Sin comodines al iniciar
        self.jokers: list[JokerBase] = []
        self.max_jokers = 5

        self.consumables = []
        self.max_consumables = 2
        self.vouchers = []

        # Build full 52-card deck usando Deck de poker_clon
        self.deck_obj = Deck()
        self.deck: list[Card] = list(self.deck_obj.cards) + list(self.deck_obj.cards[:0])  # referencia original

        self.draw_pile: list[Card] = list(self.deck_obj.cards)
        self.hand: list[Card] = []
        self.selected_cards: list[Card] = []
        self.hand_size = 8
        self.played_cards_this_ante: set[tuple[str, str]] = set()

        # Sort mode
        self.current_sort_mode = "RANK"

        self.shuffle_and_deal()

        # Earned rewards (para Round Clear Modal)
        self.earned_reward = 0
        self.earned_interest = 0

    def shuffle_and_deal(self):
        self.deck_obj = Deck()
        self.draw_pile = list(self.deck_obj.cards)
        self.deck = list(self.deck_obj.cards)
        self.hand = []
        self.selected_cards = []
        self.draw_to_hand()
        self._apply_current_sort()

    def draw_to_hand(self):
        needed = self.hand_size - len(self.hand)
        bm = self.blind_manager
        is_wheel = (bm.current_blind == "Boss" and bm.current_boss["name"] == "La Rueda")
        for _ in range(needed):
            if self.draw_pile:
                card = self.draw_pile.pop(0)
                card.is_face_down = (is_wheel and random.random() < 0.25)
                self.hand.append(card)

    def toggle_select(self, card: Card):
        if card in self.selected_cards:
            self.selected_cards.remove(card)
        else:
            if len(self.selected_cards) < 5:
                self.selected_cards.append(card)

    def advance_blind(self):
        """Avanza la ciega usando BlindManager real."""
        old_ante = self.ante
        self.blind_manager.advance_blind()
        self.blind_state = self.blind_manager.current_blind
        self.ante = self.blind_manager.ante
        self.boss_name = self.blind_manager.current_boss["name"]

        if self.ante != old_ante:
            self.played_cards_this_ante.clear()

        info = self.blind_manager.get_blind_info()
        self.target_score = info["target"]

        self.hands_left = self.max_hands
        self.discards_left = self.max_discards
        self.hands_played = 0
        self.discards_used = 0
        self.current_score = 0
        self.round += 1
        self.shuffle_and_deal()

    def reset_round(self):
        """Reinicia la mano y variables para una nueva ronda."""
        info = self.blind_manager.get_blind_info()
        self.target_score = info["target"]
        self.current_score = 0
        self.hands_played = 0
        self.hands_left = self.max_hands
        self.discards_used = 0
        self.discards_left = self.max_discards
        self.shuffle_and_deal()

    def generate_shop(self):
        """Genera jokers reales para la tienda."""
        shop_jokers = []
        for _ in range(2):
            joker_class = random.choice(ALL_JOKERS)
            joker = joker_class()
            price = get_joker_price(joker)
            shop_jokers.append({'joker': joker, 'price': price})
        return shop_jokers

    def calculate_round_rewards(self):
        """Calcula las recompensas de fin de ronda."""
        info = self.blind_manager.get_blind_info()
        self.earned_reward = calculate_round_reward(info["reward"], self.hands_left)
        self.earned_interest = calculate_interest(self.dollars)
        return self.earned_reward, self.earned_interest

    def collect_rewards(self):
        """Cobra las recompensas calculadas."""
        self.dollars += self.earned_reward + self.earned_interest

    def _apply_current_sort(self):
        """Aplica el criterio de ordenamiento activo."""
        if self.current_sort_mode == "RANK":
            self.hand.sort(key=lambda c: RANK_VALUES.get(c.rank, 0), reverse=True)
        elif self.current_sort_mode == "SUIT":
            self.hand.sort(key=lambda c: (c.suit, RANK_VALUES.get(c.rank, 0)), reverse=True)
