import random # list shuffle
import math   # floor

from game_util import *
from base_player import *

class GameManager:
    class PlayerState:
        def __init__(self, score):
            self.control = BasePlayer()
            self.score = score
            self.hand = []
            self.pile = []

        def give_hand(self, hand):
            self.hand = hand

            print("Received hand:")
            for card in self.hand:
                print(str(card))

        def remove_from_hand(self, card):
            self.hand.remove(card)

        def add_to_pile(self, cards):
            for card in cards:
                pile.append(card)


    class GameState:
        def __init__(self, playerCount, deckSize):
            self.playing = False
            self.mode = GameMode.GOING_UP
            self.firstPlayer = 0
            self.turn = 0

            self.playerCount = playerCount
            self.cardsPerPlayer = math.floor(deckSize / self.playerCount)
            self.cardsInStock = deckSize - (self.cardsPerPlayer * self.playerCount)
            self.playedCards = []

        def get_current_player(self) -> int:
            curPlayer = self.firstPlayer + self.turn

            if curPlayer >= self.playerCount:
                curPlayer -= self.playerCount

            return curPlayer

        def get_winning_player(self) -> int:
            suite = self.playedCards[0].suite
            highestFace = self.playedCards[0].suite
            winningPlayer = self.firstPlayer

            for cardId in range(1, self.playerCount):
                card = self.playedCards[cardId]
                if card.suite is suite and card.face > highestFace:
                    highestFace = card.face
                    winningPlayer = self.firstPlayer + cardId
                    if winningPlayer >= self.playerCount: winningPlayer -= self.playerCount

            return winningPlayer


    def __init__(self, playerCount):
        self.players = []
        self.deck = []

        for playerId in range(0, playerCount):
            self.players.append(self.PlayerState(0))

        for suite in Suite:
            for face in Face:
                self.deck.append(Card(suite, face))

        self.gameState = self.GameState(playerCount, len(deck))

    def start_round(self):
        print("Starting Round")

        random.shuffle(self.deck)

        for card in self.deck:
            print(str(card))

        cardsPerPlayer = math.floor(len(self.deck) / self.playerCount)
        remaining = len(self.deck) - (cardsPerPlayer * self.playerCount)

        for playerId in range(0, self.playerCount):
            firstCard = playerId * cardsPerPlayer
            lastCard = firstCard + cardsPerPlayer
            self.players[playerId].give_hand(self.deck[firstCard:lastCard])

    def end_round(self):
        for player in self.players:
            points = points_from_cards(player.pile)
            player.pile = []

            if self.gameState.mode is Mode.GOING_UP:
                player.score += points

                if player.score >= 50:
                    self.gameState.mode = Mode.GOING_DOWN
            elif self.gameState.mode is Mode.GOING_DOWN:
                player.score -= points

                if player.score == 0:
                    self.gameState.playing = False
                elif player.score < 0:
                    player.score = abs(player.score)


    def end_turn(self):
        winningPlayer = self.gameState.get_winning_player()

        self.players[winningPlayer].add_to_pile(self.gameState.playedCards)
        self.gameState.playedCards = []

        gameState.turn = 0
        gameState.firstPlayer = winningPlayer

    def start_game(self):
        print("Starting Game")

        self.gameState.playing = True
        self.start_round()

    def game_update(self):
        print("Updating")

        turn = self.gameState.turn
        playedCards = self.gameState.playedCards
        curPlayer = self.players[self.gameState.get_current_player()]

        pickedCard = curPlayer.control.play(curPlayer.hand, playedCards, turn, self.gameState.mode)
        if(not is_legal_card(curPlayer.hand, pickedCard, playedCards, turn)):
            pickedCard = get_legal_cards(curPlayer.hand, playedCards, turn)[0]

        gameState.playedCards.append(pickedCard)
        curPlayer.remove_from_hand(pickedCard)
        gameState.turn += 1

        if(gameState.turn >= self.gameState.playerCount):
            end_round()

