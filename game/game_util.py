from enum import Enum
from enum import IntEnum
from dataclasses import dataclass

GameMode = Enum('GameMode', ['GOING_UP', 'GOING_DOWN', 'FINISHED'])
Suite = Enum('Suite', ['HEARTS', 'SPADES', 'DIAMONDS', 'CLUBS'])
Face = IntEnum('Face', ['SEVEN', 'EIGHT', 'NINE', 'TEN', 'JACK', 'QUEEN', 'KING', 'ACE'])

@dataclass
class Card:
    suite: Suite
    face: Face

    def __str__(self):
        return(str(self.face) + " of " + str(self.suite))


def contains_suite(hand, suite) -> bool:
    for heldCard in hand:
        if heldCard.suite == suite:
            return True

    return False

def contains_card(hand, card) -> bool:
    for heldCard in hand:
        if heldCard == card:
            return True

    return False

def get_highest_of_suite(hand, suite) -> Card:
    if contains_suite(hand, suite):
        highestFace = Face.SEVEN

        for heldCard in hand:
            if heldCard.face > highestFace:
                highestFace = heldCard.face

        return Card(suite, highestFace)

    raise Exception("You don't have any cards of " + str(suite))

def is_legal_card(hand, card, cardsOnTable, turn) -> bool:
    if card not in hand:
        return False
    elif len(cardsOnTable) > 0:
        playedSuite = cardsOnTable[0].suite

        if contains_suite(hand, playedSuite):
            return card.suite is playedSuite
        else:
            if contains_suite(hand, Suite.HEARTS):
                return card.suite is Suite.HEARTS
            elif contains_card(hand, Card(Suite.SPADES, Face.QUEEN)):
                return card == Card(Suite.SPADES, Face.QUEEN)
            else:
                return True
    elif turn == 0:
        if contains_suite(hand, Suite.DIAMONDS) or contains_suite(hand, Suite.CLUBS):
            return card.suite is not Suite.HEARTS and card.suite is not Suite.SPADES
        else: # TODO: Is this true?
            return True


    return True

def get_legal_cards(hand, cardsOnTable, turn) -> list:
    legalCards = []
    for card in hand:
        if is_legal_card(hand, card, cardsOnTable, turn):
            legalCards.append(card)

    if len(legalCards) == 0:
        print("Zero legal moves!")
        print("Turn: " + str(turn))
        print("Hand: " + str(hand))
        print("CardsOnTable: " + str(cardsOnTable))

    return legalCards

def points_from_cards(cards) -> int:
    points = 0

    for card in cards:
        if card.suite is Suite.HEARTS:
            points += 1
        elif card.suite is Suite.SPADES and card.face is Face.QUEEN:
            points += 8

    return points

@dataclass
class TurnInfo:
    myCards: []
    cardsOnTable: []
    playerCount: int
    currentTurn: int
    totalTurns: int
    mode: GameMode
    stockSize: int

class ScoreBoard:
    @dataclass
    class RoundScore:
        totalScores: []
        roundScores: []
        mode: GameMode

    def __init__(self, playerCount, mode, maxScore):
        self.playerCount = playerCount
        self.mode = mode
        self.maxScore = maxScore
        self.rounds = []

    def reset_scores(self):
        self.rounds = []

    def get_rounds_played(self) -> int:
        return len(self.rounds)

    def get_last_round(self) -> RoundScore:
        return self.rounds[self.get_rounds_played() - 1]

    def get_player_score(self, playerId) -> int:
        return self.get_last_round().totalScores[playerId]

    def add_round(self, roundPoints, mode) -> GameMode:
        newMode = mode

        if mode is GameMode.GOING_DOWN:
            for playerId in range(0, self.playerCount):
                roundPoints[playerId] = -roundPoints[playerId]

        if self.get_rounds_played() == 0:
            self.rounds.append(self.RoundScore(roundPoints, roundPoints, mode))
        else:
            totalScores = []
            lastRound = self.get_last_round()

            for playerId in range(0, self.playerCount):
                totalScore = lastRound.totalScores[playerId] + roundPoints[playerId]
                if totalScore >= self.maxScore:
                    totalScore = self.maxScore
                    newMode = GameMode.GOING_DOWN
                elif totalScore < 0:
                    totalScore = abs(totalScore)
                elif mode is GameMode.GOING_DOWN and totalScore == 0:
                    newMode = GameMode.FINISHED

                totalScores.append(totalScore)

            self.rounds.append(self.RoundScore(totalScores, roundPoints, mode))

        #print("New scores: " + str(self.get_last_round().totalScores))
        return newMode