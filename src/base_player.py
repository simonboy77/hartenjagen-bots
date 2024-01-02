from game_util import *

class BasePlayer:
    def __init__(self):
        print("init player")

    # TODO Add comments for each parameter
    def play_card(self, hand, playedCards, turn, mode) -> Card:
        return get_legal_cards(hand, playedCards, turn)[0]

    def get_name(self) -> str:
        return "Base Player"

    def get_author(self) -> str:
        return "Simon"