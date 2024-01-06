from game_manager import *

manager = GameManager(4)
manager.start_game()

while manager.game_update():
    continue