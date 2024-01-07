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


class SuperSmartyPants(BaseBrain):
    def play_card(self, turnInfo, scoreBoard) -> Card:
        legalCards = get_legal_cards(turnInfo.myCards, turnInfo.cardsOnTable, turnInfo.currentTurn)
        pickedCard = legalCards[0]

        if turnInfo.mode is GameMode.GOING_UP:
            pickedCard = self.play_upwards(turnInfo, scoreBoard, legalCards)
        elif turnInfo.mode is GameMode.GOING_DOWN:
            pickedCard =  self.play_downwards(turnInfo, scoreBoard, legalCards)

        return pickedCard

    def play_upwards(self, turnInfo, scoreBoard, legalCards) -> Card:
        pickedCard = legalCards[0]
        moveNum = len(turnInfo.cardsOnTable)

        lowestFace = legalCards[0].face
        for legalCard in legalCards:
            if legalCard.face < lowestFace:
                lowestFace = legalCard.face
                pickedCard = legalCard

    def play_downwards(self, turnInfo, scoreBoard, legalCards) -> Card:
        pickedCard = legalCards[0]
        moveNum = len(turnInfo.cardsOnTable)

        highestFace = legalCards[0].face
        for legalCard in legalCards:
            if legalCard.face > highestFace:
                highestFace = legalCard.face
                pickedCard = legalCard

    def turn_result(self, cardsOnTable, winnerId):
        self.piles[winnerId]

        pass

    def get_name(self) -> str:
        return "SuperSmartyPants"

    def get_author(self) -> str:
        return "Simon"