# Author: mohamm-alsaid
# Date: 03/01/22

import argparse, pandas as pd
from clients import Clients,Moves
from member_handler import Handler
import os
# import e3db 
    
def check_option_is_valid(option:str, options:dict):
    keys = list(options.keys())
    # avoid casing issues, lower everything
    option = option.lower()
    if not option in keys:
        print(f'Invalid program input. input: {option} possible options: {keys}')
    return option in keys

def get_tozny_client_config(token=None,client=None):
    '''
        loads or creates configs
        param
        -----
            * token: token used to register client (in case it is new)
            * client: client's name to use when registering client (in case it is new)
        returns
        -----
            * config obj
    '''
    # try loading client from disk
    try:
        config = e3db.Config.load()
        print('Loaded configs from disk successfully')
    except FileNotFoundError:
        # assert we have needed params to register client
        assert not token is None, 'Token parameter is missing (None)! Needed for registration.'  
        assert not client is None, 'Client parameter is missing (None)! Needed for registration.'
        # generate pair
        public_key,private_key = e3db.Client.generate_keypair()

        # register client
        client_info = e3db.Client.register(token, client, public_key) # trying w/o creating client via dashboard (to see value)

        config = e3db.Config(
            client_info.client_id,
            client_info.api_key_id,
            client_info.api_secret,
            public_key, 
            private_key
        )
        # write to disk for future use
        config.write()
        print('Generate new configs successfully')
    return config

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
    # records = list(filter(lambda x: x['meta']['writer_id'],records))
    # df = pd.DataFrame(records)
    # df['writer_id'] = df['meta'].apply(lambda r: r['writer_id'])
    # df['writer_id'] = df['writer_id'].apply(lambda x: 'self' if x==handler.client.client_id else x)
    # df['move'] = df['data'].apply(dict.values)
    # df = df.drop(['meta','data'],axis=1)
    # df = df[['meta']['writer_id']]
    # print(df)
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
    print(moves)
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
    parser.add_argument('--creds', type=str, help='Relative path to creds directory (directory path with name)',default=None,required=True)
    parser.add_argument('--reset', type=bool, help='reset game (deletes all records of all previous rounds)',default=False)
    parser.add_argument('--display', type=bool, help='displays all records (written by an shared with) client',default=False)
    parser.add_argument('--declare', type=bool, help='Declare winner for round (only Clarence)',default=False)
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

    # @TODO: fix logic surrounding not submitting a move and only displaying things
    # Validate client option (running program as client is required)
    if not check_option_is_valid(client,possible_clients): 
        exit()

    # Validate move option (will short circuit if move is NoneType)
    if not move is None:
        if not check_option_is_valid(move,possible_moves):
            exit()

    # ----------------------------------------------------
    


    # ------------- grab token from environment ----------
    # key = 'TOZNY_TOKEN'
    # token = os.getenv(key)
    # ----------------------------------------------------
    
    handler = Handler(clients.retrieve_client_creds(client))

    # The judge can not submit a move!
    if not move is None:
        if client == 'clarence':
            print('Judge is not allowed to play.')
        else:
            handler.submit_record({"move":move},recipients=[ clients.retrieve_client_creds('clarence') ])

    if display:
        display_records(handler,clients)

    if declare:
        if not client == 'clarence':
            print(f"{client} not allowed to declare winner!")
        else:
            moves = display_records(handler,clients)
            # assert there are enough moves and each player has submitted a move 
            if len(moves) > 1 and len(set(map(lambda x: x[0],moves)))>1:
                winner = declare_winner(moves)
                
                # create record to declare winner shared with other players
                record = {"winner": winner[0], "submitted move": winner[-1]}

                # filter other players whom we shared records with (everyone but clarence)
                share_with = list(map(clients.retrieve_client_creds,filter(lambda x: x != client, possible_clients.keys())))

                print(record)
                handler.submit_record({"round winner": winner[0],"submitted move":winner[-1]},share_with)
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