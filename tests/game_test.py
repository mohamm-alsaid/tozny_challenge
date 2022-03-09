import unittest, json
from game import *

class TestClientsClass(unittest.TestCase):
    # -------------test check option is valid--------------
    def test_check_option_is_valid_success(self):
        pass
    def test_check_option_is_valid_fail(self):
        pass

    # -------------test declare winner--------------
    def test_declare_winner_success(self):
        # test draw, and rock vs paper
        pass
    def test_declare_winner_fail(self):
        # only one play submits a move, and no moves
        pass
    # -------------test reset game--------------
    def test_reset_game_success(self):
        # test play a round and assert all records deleted
        pass
    # -------------test display moves--------------
    def test_display_moves_success(self):
        # play a round
        # test it against search records for each play
        pass