from game_util import *

class BaseBrain:
    def __init__(self, playerId):
        print("Starting " + self.get_name() + " by " + self.get_author())
        self.id = playerId

    # <turnInfo>   Instance of TurnInfo class
    # <scoreBoard> Instance of ScoreBoard class (game_util.py)
    def play_card(self, turnInfo, scoreBoard) -> Card:
        legalCards = get_legal_cards(turnInfo.myCards, turnInfo.cardsOnTable, turnInfo.currentTurn)
        return legalCards[0]

    def turn_result(self, cardsOnTable, winnerId):
        pass

    def get_name(self) -> str:
        return "Example Player"

    def get_author(self) -> str:
        return "Example Author"
