#! /bin/python3

# Author: mohamm-alsaid
# Date: 03/01/22
import argparse, pandas as pd, os
from clients import Clients,Moves
from member_handler import Handler
    
def check_option_is_valid(option:str, options:dict):
    keys = list(options.keys())
    # avoid casing issues, lower everything
    option = option.lower()
    if not option in keys:
        print(f'Invalid program input. input: {option} possible options: {keys}')
    return option in keys

def reset_game(clients):
    print('-'*25,'\n')
    for client in clients.members:
        print('remove all records for: ',client)
        handler = Handler(clients.retrieve_client_creds(client))
        ids = list(map(clients.retrieve_client_creds,clients.members))
        handler.remove_all_records(shared_with=ids)

def display_records(handler,clients):
    records = handler.search_records()
    submitted_moves = []
    if len(records) == 0:
        print('No records to display.')

    for r in records:
        date = r['meta']['created'].split('.')[0]
        move = r['data']
        writer = clients.reverse_lookup_client_id(r['meta']['writer_id'])
        if 'winner' in move.keys() and move['winner'] == handler.client.client_id:
            move['winner'] = 'self!'
        elif 'winner' in move.keys():
            move['winner'] = 'Other player :('
        print(f"\n({date})\t@{writer}\n\tsubmitted:\t{move}")

        submitted_moves.append((writer,move))
    return submitted_moves

def declare_winner(moves):
    '''
        Uses the submmited moves to decide who won the round. 
        Note: it uses the first submitted moves from each player ONLY
        
        Param
        ------
            * moves: a list of tuples (writer,move) of submitted moves
        Return
        ------
            * ID of round winner
    '''
    moves_dict = {k:v['move'] for k,v in moves}
    
    # assume draw before starting
    winner = 'draw'     
    # only grab first two (there won't be any more since ID will be overwritten in case of collision)
    k1,k2 = list(moves_dict.keys())[:2]
    v1,v2 = Moves[moves_dict[k1]].value,Moves[moves_dict[k2]].value
    # draw case (not necessary but for readability)
    if v1==v2:
        return (winner,moves_dict[k1]) # both moves are the same
    else:
        # pick winner
        if v1 > v2 and (v1-v2) <= 1:
            winner = k1
        else:
            winner = k2 
    return (winner,moves_dict[winner])

def main():
    # specify args args
    parser = argparse.ArgumentParser(description='Rock, Paper, Scissors Game.')
    parser.add_argument('--client', type=str, help='Clients for this game: <clarence | alice | bruce>',default='clarence',required=True)
    parser.add_argument('--creds', type=str, help='Relative path to creds directory (directory path with name)',default='./creds')
    parser.add_argument('--reset', type=bool, 
        help='reset game (deletes all records of all previous rounds)',
        default=False,action=argparse.BooleanOptionalAction)
    parser.add_argument('--display', type=bool, 
        help='displays all records (written by an shared with) client',
        default=False,action=argparse.BooleanOptionalAction)
    parser.add_argument('--declare', type=bool, 
        help='Declare winner for round (only Clarence)',
        default=False,action=argparse.BooleanOptionalAction)
    # it is possible for a client not to make a move (check the game winner or any of the judge's actions)
    # so it doesn't need to be a required program argument
    parser.add_argument('--move', type=str, help='Make a move: <rock | paper | scissors>',default=None,required=False)
    
    # parse args
    args = parser.parse_args()
    client = args.client
    move = args.move
    creds_path = args.creds
    reset = args.reset
    display = args.display
    declare = args.declare

    # grab possible options (used for use input checking)
    clients = Clients(creds_path=creds_path)
    possible_clients = clients.members
    possible_moves = Moves.__members__

    # ------------------- validate input ----------------- 
    # creds is not checked (could be validated by checking whether client's name is in the file path)
    # but this relies on naming the creds files such that they indicate which member keys belong to --> not sure its good
    # Validate client option (running program as client is required)
    if not check_option_is_valid(client,possible_clients): 
        exit()

    # Validate move option (will short circuit if move is NoneType)
    if not move is None:
        if not check_option_is_valid(move,possible_moves):
            exit()

    # ----------------------------------------------------
    
    handler = Handler(clients.retrieve_client_creds(client))

    # The judge can not submit a move!
    if not move is None:
        if client == 'clarence':
            print('Judge is not allowed to play.')
        else:
            share_with = [clients.retrieve_client_creds('clarence')]
            # not really in efficient but simplist way
            records = display_records(handler,clients)
            if len(records) < 1:
                # check if other player has submitted a move
                opponent_name = next(filter(lambda x: x!= client and x!='clarence',possible_clients.keys()))
                opponent_handler = Handler(clients.retrieve_client_creds(opponent_name))
                opponent_records = opponent_handler.search_records()
                if len(opponent_records) > 0:
                    share_with.append(clients.retrieve_client_creds(opponent_name))
                # print(opponent_name,len(opponent_records))
                handler.submit_record({"move":move},recipients=share_with)
            else:
                print('only 1 move per player is alowed (no overwritting)')

    if display:
        display_records(handler,clients)

    if declare:
        if not client == 'clarence':
            print(f"{client} not allowed to declare winner!")
        else:
            moves = display_records(handler,clients)
            # assert there are enough moves and each player has submitted a move 
            if len(moves) > 1 and len(set(map(lambda x: x[0],moves)))>1:
                if len(set(map(lambda x: x[0],moves)))<=2:
                    winner = declare_winner(moves)
                    
                    # create record to declare winner shared with other players
                    record = {"winner": winner[0], "submitted move": winner[-1]}

                    # filter other players whom we shared records with (everyone but clarence)
                    share_with = list(map(clients.retrieve_client_creds,filter(lambda x: x != client, possible_clients.keys())))

                    print(record)
                    handler.submit_record({"round winner": winner[0],"submitted move":winner[-1]},share_with)
                else:
                    print('Round winner has already been declared')
            else:
                print("Not enough moves from all players")

    # It is possible for a client to submit a move
    if reset:
        if not client == 'clarence':
            print('Only judge is allowed to reset game.')
        else:
            reset_game(clients)
    
    return

if __name__=="__main__":
    main()
    exit()