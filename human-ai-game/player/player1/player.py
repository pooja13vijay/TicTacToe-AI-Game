import random

class Player:
  def __init__(self):
    pass

  def play(self, game_board_state, player_n):
    return random.choice([i for i in range(len(game_board_state)) if game_board_state[i] < 0])