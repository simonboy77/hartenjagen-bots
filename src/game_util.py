from enum import Enum
from dataclasses import dataclass

GameMode = Enum('GameMode', ['GOING_UP', 'GOING_DOWN'])
Suite = Enum('Suite', ['HEARTS', 'SPADES', 'DIAMONDS', 'CLUBS'])
Face = Enum('Face', ['SEVEN', 'EIGHT', 'NINE', 'TEN', 'JACK', 'QUEEN', 'KING', 'ACE'])

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

def is_legal_card(hand, card, playedCards, turn) -> bool:
    if card not in hand:
        return False
    elif len(playedCards) > 0:
        playedSuite = playedCards[0].suite

        if contains_suite(hand, playedSuite):
            return card.suite is playedSuite
        else:
            if contains_suite(hand, Suite.Hearts):
                return card.suite is Suite.Hearts
            elif contains_card(hand, Card(Suite.Spades, Face.QUEEN)):
                return card == Card(Suite.Spades, Face.QUEEN)
            else:
                return True
    elif turn == 0:
        return card.suite is not Suite.HEARTS and card.suite is not Suite.SPADES

    return True

def get_legal_cards(hand, playedCards, turn) -> list:
    legalCards = []
    for card in hand:
        if is_legal_card(hand, card, playedCards, turn):
            legalCards.append(card)

    print("legalCards: " + str(legalCards))
    return legalCards

def points_from_cards(cards) -> int:
    points = 0

    for card in cards:
        if card.suite is Suite.Hearts:
            points += 1
        elif card.suite is Suite.SPADES and card.face is Face.QUEEN

    return points