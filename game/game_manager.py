import random # random starting player

from game_state import *

class GameManager:
    def __init__(self, playerBrains, maxScore):
        self.gameState = GameState(playerBrains, maxScore)
        self.playerWins = []

        for playerId in range(0, len(playerBrains)):
            self.playerWins.append(0)

    def is_playing(self) -> bool:
        return self.gameState.mode is not GameMode.FINISHED

    def print_player_wins(self):
        for playerId in range(0, len(self.playerWins)):
            playerName = self.gameState.get_player(playerId).get_name()
            print(playerName + " has " + str(self.playerWins[playerId]) + " wins")

    def start_game(self):
        print("Starting Game")

        self.gameState.reset_game()
        self.start_round()

    def start_round(self):
        self.gameState.shuffle_and_divide_deck()
        self.gameState.rotate_round_starter()
        self.gameState.turnStarter = self.gameState.roundStarter
        self.gameState.turn = 0

        #print("\nStarting Round " + str(self.gameState.roundsPlayed) + " with " + str(self.gameState.roundStarter))

    def end_round(self):
        self.gameState.roundsPlayed += 1

        # Apply points
        playerPoints = []
        for playerId in range(0, self.gameState.playerCount):
            points = self.gameState.players[playerId].count_and_clear_pile()
            playerPoints.append(points)

        #print("Results: " + str(playerPoints))
        self.gameState.add_round(playerPoints)

        if self.gameState.mode is GameMode.FINISHED:
            for playerId in range(0, self.gameState.playerCount):
                if self.gameState.get_player_score(playerId) == 0:
                    player = self.gameState.get_player(playerId)
                    roundsPlayed = self.gameState.scoreBoard.get_rounds_played()
                    self.playerWins[playerId] += 1

                    print(player.get_name() + " won after " + str(roundsPlayed) + " rounds")


    def end_turn(self):
        turnWinner = self.gameState.get_turn_winner()
        turnWinner.add_to_pile(self.gameState.cardsOnTable)

        self.gameState.give_stock_to_player(turnWinner)
        self.gameState.cardsOnTable = []
        self.gameState.turnsPlayed += 1
        self.gameState.firstPlayer = turnWinner

    def next_move(self):
        movingPlayer = self.gameState.get_moving_player()
        legalCards = self.gameState.get_next_legal_moves()
        pickedCard = self.gameState.get_next_move()

        if(pickedCard not in legalCards):
            pickedCard = legalCards[0]

        self.gameState.cardsOnTable.append(pickedCard)
        movingPlayer.remove_from_hand(pickedCard)

        if(self.gameState.is_end_of_turn()):
            self.end_turn()

            if self.gameState.is_end_of_round():
                self.end_round()

                if self.is_playing():
                    self.start_round()

    def game_update(self) -> bool:
        if self.is_playing():
            self.next_move()

        return self.is_playing()

