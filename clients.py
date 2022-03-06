from enum import Enum
import json, sys
class AllClients(Enum):
    '''
        Enum for the different possible clients. 
        Might come in handy later
    '''
    alicia = 0
    bruce = 1
    clarence = 2
     
class Moves(Enum):
    '''
        Enum for the different possible moves. 
    '''
    rock = 0
    paper = 1
    scissors = 2


class Clients:
    def __init__(self,creds_path='./'):
        '''
        Idea: represents a single handler for different players
        params
        ------
        creds_path : path where credentials are stored for all clients involved
                    * possible members: Alicia, Bruce, Clarence
        '''
        self.all_clients = AllClients.__members__
        self.members = {}
        
        print('---> ',creds_path)
        try:
            for client in self.all_clients:
                # read member and their creds
                creds = json.load(open(f'{creds_path}/{client}.json','r'))
                self.members[client] = creds
        except Exception as e:
            print('Issues opening a credentials file! Terminating...')
            print(e)
            return sys.exit(1)
        return
    def retrieve_client_creds(self,client):
        '''
            Retrieves the credentials for the given client.
            Param
            -----
                * Client: name of client given client.

            Return
            ------
                * dict of stored creds for the give client. 
        '''
        return self.members[client]

