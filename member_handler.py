import json, sys,e3db

class Handler:
    def __init__(self,creds_path = './'):
        '''
            Handles e3db calls.
            Idea: represents a single handler for different players
            Params: 
                creds_path : path + name of file (relative) for the member it is supposed to represent
                    * possible members: Alicia, Bruce, Clarence 
        '''
        try:
            self.creds = json.load(open(creds_path,'r'))
        except Exception as e:
            print('Issues opening the credentials file! Terminating...')
            print(e)
            return sys.exit(1)
        return
    def get_client(self):
        '''
            Creates move 
        '''
        # use configs to create client
        self.client = e3db.Client(self.creds)
        return self.client
