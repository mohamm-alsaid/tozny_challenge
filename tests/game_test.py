import unittest, json, numpy as np, time
from game import *

class TestGame(unittest.TestCase):
    # -------------test check option is valid--------------
    def test_check_option_is_valid_success(self):
        options = {str(k):k for k in range(20)}
        option = str(np.random.randint(0,20))
        valid = check_option_is_valid(option,options)
        self.assertEqual(valid,True)   
        return
    def test_check_option_is_valid_fail(self):
        options = {str(k):k for k in range(20)}
        option = str(np.random.randint(20,30))

        valid = check_option_is_valid(option,options)
        self.assertEqual(valid,False)
        return
    # -------------test declare winner--------------
    def test_declare_winner_success(self):
        # test draw, and rock vs paper
        # -------- draw --------
        clients = Clients()
        reset_game(clients) # start fresh
        record = {'move':'rock'}
        alicia_handler = Handler(clients.retrieve_client_creds('alicia'))
        bruce_handler = Handler(clients.retrieve_client_creds('bruce'))
        clarence = clients.retrieve_client_creds('clarence')
        clarence_handler = Handler(clarence)

        alicia_handler.submit_record(record,[clarence])
        bruce_handler.submit_record(record,[clarence])
        # wait for server to process
        time.sleep(1) # too long for a unit test
        moves = clarence_handler.search_records()
        moves = display_records(clarence_handler,clients)
        winner = declare_winner(moves)
        self.assertEqual(winner[0],'draw')
        self.assertEqual(winner[-1],'rock')
        # ----------rock (bruce) vs paper (alicia)---------
        reset_game(clients)
        second_record = {'move':'paper'}
        bruce_handler.submit_record(record,[clarence])
        alicia_handler.submit_record(second_record,[clarence])
        # wait for server to process
        time.sleep(1) # too long for a unit test
        moves = clarence_handler.search_records()
        moves = display_records(clarence_handler,clients)
        winner = declare_winner(moves)
        self.assertEqual(winner[0],'alicia')
        self.assertEqual(winner[-1],'paper')
        # -------------------------------------------------
        return
    def test_declare_winner_fail(self):
        # only one play submits a move, and no moves
        clients = Clients()
        reset_game(clients) # start fresh
        record = {'move':'rock'}
        alicia_handler = Handler(clients.retrieve_client_creds('alicia'))
        clarence = clients.retrieve_client_creds('clarence')
        clarence_handler = Handler(clarence)
        # ------- no moves submitted -------
        moves = clarence_handler.search_records()
        moves = display_records(clarence_handler,clients)
        winner = declare_winner(moves)
        self.assertEqual(winner[0],None)
        self.assertEqual(winner[-1],None)
        # ------------- one move only ------
        alicia_handler.submit_record(record,[clarence])
        # wait for server to process
        time.sleep(1) # too long for a unit test
        moves = clarence_handler.search_records()
        moves = display_records(clarence_handler,clients)
        winner = declare_winner(moves)
        self.assertEqual(winner[0],None)
        self.assertEqual(winner[-1],None)
        # ---------------------------------
        return
    # -------------test reset game--------------
    def test_reset_game_success(self):
        # test play a round and assert all records deleted
        clients = Clients()
        # Submit a couple of records
        record = {'test':'test'}
        bruce = Handler(clients.retrieve_client_creds('bruce'))
        bruce.submit_record(record,[])
        reset_game(clients)
        # wait for changes to take effect
        time.sleep(1) # pretty long for a unit test
        records = bruce.search_records()
        self.assertEqual(len(records),0)
        return
    # -------------test display moves--------------
    def test_display_moves_success(self):
        # play a round
        # test it against search records for each play
        clients = Clients()
        reset_game(clients) # clear all records (start fresh)
        record = {'move':'rock'}
        alicia_handler = Handler(clients.retrieve_client_creds('alicia'))
        bruce_handler = Handler(clients.retrieve_client_creds('bruce'))
        clarence = clients.retrieve_client_creds('clarence')
        clarence_handler = Handler(clarence)

        moves = clarence_handler.search_records()
        moves = display_records(clarence_handler,clients)
        self.assertEqual(len(moves),0)
        
        # alicia submits first
        alicia_handler.submit_record(record,[clarence])
        # wait for server to process
        time.sleep(1) # too long for a unit test
        moves = clarence_handler.search_records()
        moves = display_records(clarence_handler,clients)
        self.assertEqual(len(moves),1)

        # bruce submits second
        alicia_handler.submit_record(record,[clarence])
        # wait for server to process
        time.sleep(1) # too long for a unit test
        moves = clarence_handler.search_records()
        moves = display_records(clarence_handler,clients)
        self.assertEqual(len(moves),2)
        return