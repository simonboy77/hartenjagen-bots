from game_manager import *

brains = [ BaseBrain(0), BaseBrain(1), BaseBrain(2), SuperSmartyPants(3) ]

manager = GameManager(brains, 50)

gamesPlayed = 0
while gamesPlayed < 5000:
    manager.start_game()

    while manager.game_update():
        pass

    gamesPlayed += 1

manager.print_player_wins()