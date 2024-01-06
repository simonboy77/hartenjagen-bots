import random # list shuffle
from math import floor

from game_util import *
from base_player import *

class GameManager:
    class PlayerState:
        def __init__(self, control):
            self.control = control
            self.hand = []
            self.pile = []

        def give_hand(self, hand):
            self.hand = hand

        def remove_from_hand(self, card):
            self.hand.remove(card)

        def add_to_pile(self, cards):
            for card in cards:
                self.pile.append(card)

        def count_and_return_pile(self) -> int:
            points = points_from_cards(self.pile)
            self.pile = []
            return points

        def get_name(self) -> str:
            return self.control.get_name()

        def get_card_amount(self) -> int:
            return len(self.hand)


#
    class GameState:
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
                        if totalScore > self.maxScore:
                            totalScore = self.maxScore
                            newMode = GameMode.GOING_DOWN
                        elif totalScore < 0:
                            totalScore = abs(totalScore)
                            newMode = GameMode.FINISHED

                        totalScores.append(totalScore)

                    self.rounds.append(self.RoundScore(totalScores, roundPoints, mode))

                print("New scores: " + str(self.get_last_round().totalScores))
                return newMode


        def __init__(self, playerCount, deckSize, maxScore):
            self.mode = GameMode.GOING_UP
            self.maxScore = maxScore

            self.firstPlayer = 0
            self.turnsPlayed = 0
            self.roundsPlayed = 0

            self.playerCount = playerCount
            self.cardsPerPlayer = floor(deckSize / self.playerCount)
            self.cardsInStock = deckSize - (self.cardsPerPlayer * self.playerCount)
            self.playedCards = []

            self.scoreBoard = self.ScoreBoard(self.playerCount, self.mode, self.maxScore)

        def get_current_player(self) -> int:
            movesPlayed = len(self.playedCards)
            curPlayer = self.firstPlayer + movesPlayed

            if curPlayer >= self.playerCount:
                curPlayer -= self.playerCount

            return curPlayer

        def get_winning_player(self) -> int:
            suite = self.playedCards[0].suite
            highestFace = self.playedCards[0].face
            winningPlayer = self.firstPlayer

            for cardId in range(1, self.playerCount):
                card = self.playedCards[cardId]
                if card.suite is suite and card.face > highestFace:
                    highestFace = card.face
                    winningPlayer = self.firstPlayer + cardId
                    if winningPlayer >= self.playerCount: winningPlayer -= self.playerCount

            return winningPlayer

        def is_end_of_turn(self) -> bool:
            return len(self.playedCards) >= self.playerCount

        def add_round(self, roundPoints):
            self.mode = self.scoreBoard.add_round(roundPoints, self.mode)

            if self.mode is GameMode.FINISHED:
                for playerId in range(0, self.playerCount):
                    if self.scoreBoard.get_player_score(playerId) == 0:
                        print(str(playerId) + " won after " + str(self.scoreBoard.get_rounds_played()) + " rounds")



    def __init__(self, playerCount):
        #TODO: Instead of passing playerCount, pass a list of BasePlayers, length is playerCount
        self.players = []
        self.deck = []

        for playerId in range(0, playerCount):
            self.players.append(self.PlayerState(BasePlayer()))

        for suite in Suite:
            for face in Face:
                self.deck.append(Card(suite, face))

        self.gameState = self.GameState(playerCount, len(self.deck), 50)

    def is_playing(self) -> bool:
        return self.gameState.mode is not GameMode.FINISHED

    def is_end_of_round(self) -> bool:
        for player in self.players:
            if player.get_card_amount() == 0:
                return True

        return False

    def start_round(self):
        print("Starting Round")

        random.shuffle(self.deck)
        cardsPerPlayer = floor(len(self.deck) / self.gameState.playerCount)
        remaining = len(self.deck) - (cardsPerPlayer * self.gameState.playerCount)

        for playerId in range(0, self.gameState.playerCount):
            firstCard = playerId * cardsPerPlayer
            lastCard = firstCard + cardsPerPlayer
            self.players[playerId].give_hand(self.deck[firstCard:lastCard])

    def end_round(self):
        self.gameState.roundsPlayed += 1
        self.gameState.turn = 0

        print("Round " + str(self.gameState.roundsPlayed))

        # Apply points
        playerPoints = []
        for playerId in range(0, self.gameState.playerCount):
            points = self.players[playerId].count_and_return_pile()
            playerPoints.append(points)

        self.gameState.add_round(playerPoints)

    def end_turn(self):
        winningPlayer = self.gameState.get_winning_player()

        self.players[winningPlayer].add_to_pile(self.gameState.playedCards)
        self.gameState.playedCards = []

        self.gameState.turnsPlayed += 1
        self.gameState.firstPlayer = winningPlayer

    def next_move(self):
        turn = self.gameState.turnsPlayed
        playedCards = self.gameState.playedCards
        curPlayer = self.players[self.gameState.get_current_player()]

        pickedCard = curPlayer.control.play_card(curPlayer.hand, playedCards, turn, self.gameState.mode)
        if(not is_legal_card(curPlayer.hand, pickedCard, playedCards, turn)):
            pickedCard = get_legal_cards(curPlayer.hand, playedCards, turn)[0]

        self.gameState.playedCards.append(pickedCard)
        curPlayer.remove_from_hand(pickedCard)

        if(self.gameState.is_end_of_turn()):
            self.end_turn()

            if self.is_end_of_round():
                self.end_round()

                if self.is_playing():
                    self.start_round()

    def start_game(self):
        print("Starting Game")

        self.gameState.roundsPlayed = 0
        self.start_round()

    def game_update(self) -> bool:
        if self.is_playing():
            self.next_move()

        return self.is_playing()

