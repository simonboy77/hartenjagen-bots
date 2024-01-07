import random # list shuffle
from math import floor

from brains import *

class PlayerState:
    def __init__(self, brain):
        self.brain = brain
        self.hand = []
        self.pile = []

    def give_hand(self, hand):
        self.hand = hand

    def remove_from_hand(self, card):
        self.hand.remove(card)

    def play_card(self, turnInfo, scoreBoard) -> Card:
        turnInfo.myCards = self.hand
        self.brain.play_card(turnInfo, scoreBoard)

    def get_legal_cards(self, cardsOnTable, turn) -> list:
        return get_legal_cards(self.hand, cardsOnTable, turn)

    def add_to_pile(self, cards):
        for card in cards:
            self.pile.append(card)

    def count_and_clear_pile(self) -> int:
        points = points_from_cards(self.pile)
        self.pile = []
        return points

    def get_name(self) -> str:
        return self.brain.get_name()

    def get_card_amount(self) -> int:
        return len(self.hand)


class GameState:
    mode = GameMode.GOING_UP
    turnStarter = 0
    turnsPlayed = 0
    roundStarter = 0
    roundsPlayed = 0
    cardsOnTable = []

    def __init__(self, playerBrains, maxScore):
        self.maxScore = maxScore

        self.players = []
        for playerId in range(0, len(playerBrains)):
            self.players.append(PlayerState(playerBrains[playerId]))

        self.deck = []
        for suite in Suite:
            for face in Face:
                self.deck.append(Card(suite, face))

        self.playerCount = len(self.players)
        self.cardsPerPlayer = floor(len(self.deck) / self.playerCount)
        self.cardsInStock = len(self.deck) - (self.cardsPerPlayer * self.playerCount)

        self.scoreBoard = ScoreBoard(self.playerCount, self.mode, self.maxScore)
        self.reset_game()

    def reset_game(self):
        self.mode = GameMode.GOING_UP

        self.turnStarter = 0
        self.turnsPlayed = 0

        self.roundStarter = 0
        self.roundsPlayed = 0

        self.cardsOnTable = []

        self.scoreBoard.reset_scores()

    def shuffle_and_divide_deck(self):
        random.shuffle(self.deck)
        self.cardsInStock = len(self.deck) - (self.cardsPerPlayer * self.playerCount)

        for playerId in range(0, self.playerCount):
            firstCard = playerId * self.cardsPerPlayer
            lastCard = firstCard + self.cardsPerPlayer
            self.players[playerId].give_hand(self.deck[firstCard:lastCard])

    def get_player(self, playerId) -> PlayerState:
        return self.players[playerId]

    def get_player_score(self, playerId) -> int:
        return self.scoreBoard.get_player_score(playerId)

    def get_moving_player(self) -> PlayerState:
        movesPlayed = len(self.cardsOnTable)
        curPlayer = self.turnStarter + movesPlayed

        if curPlayer >= self.playerCount:
            curPlayer -= self.playerCount

        return self.players[curPlayer]

    def get_next_move(self) -> Card:
        movingPlayer = self.get_moving_player()
        turnInfo = TurnInfo([], self.cardsOnTable, self.playerCount, self.turnsPlayed, self.cardsPerPlayer, self.mode, self.cardsInStock)

        return movingPlayer.play_card(turnInfo, self.scoreBoard)

    def get_next_legal_moves(self) -> list:
        movingPlayer = self.get_moving_player()
        return movingPlayer.get_legal_cards(self.cardsOnTable, self.turnsPlayed)

    def rotate_round_starter(self):
        self.roundStarter += 1

        if self.roundStarter >= self.playerCount:
            self.roundStarter = 0

    def get_turn_winner(self) -> PlayerState:
        suite = self.cardsOnTable[0].suite
        highestFace = self.cardsOnTable[0].face
        turnWinner = self.turnStarter

        for cardId in range(1, self.playerCount):
            card = self.cardsOnTable[cardId]
            if card.suite is suite and card.face > highestFace:
                highestFace = card.face
                turnWinner = self.turnStarter + cardId
                if turnWinner >= self.playerCount: turnWinner -= self.playerCount

        return self.players[turnWinner]

    def give_stock_to_player(self, player):
        if self.cardsInStock:
            stockStart = self.cardsPerPlayer * self.playerCount
            player.add_to_pile(self.deck[stockStart:])

        self.cardsInStock = 0

    def is_end_of_turn(self) -> bool:
        return len(self.cardsOnTable) >= self.playerCount

    def is_end_of_round(self) -> bool:
        for player in self.players:
            if player.get_card_amount() == 0:
                return True

        return False

    def add_round(self, roundPoints):
        self.mode = self.scoreBoard.add_round(roundPoints, self.mode)