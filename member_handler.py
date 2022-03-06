import json, sys, datetime as dt, hashlib, time
import e3db
from uuid import uuid4
from e3db import types as Types
# from e3db.types import Search as S
# from e3db_python import e3db 
# from e3db import types as E3dbTypes
# import e3db

class Handler:
    def __init__(self,creds):
        '''
            Handles e3db calls.
            Idea: represents a single handler for different players
            Params: 
                creds (dict): credentials for the client it represents. 
        '''
        self.creds = creds
        # use configs to create client
        self.client = e3db.Client(self.creds)
        return
    def get_client(self):
        '''
            Uses credentials to create a client object using creds as configs.
            Param
            --------
            Args: none
            Returns: Client (e3db client object)   
        '''
        return self.client
    def get_client_id(self):
        '''
            Returns clients ids. Used primarily for sharing purposes (between players & the judge).
        '''
        return self.client.client_id

    def submit_move(self,move: str, recipients: list, max_views = 3, expr:int = 3):
        '''
            Submits a move (encrypted) to each of the recipients as a note.

            Param
            ------
                * move (str): move to submit.
                * recipients (list): list of recipients to leave an encrypted note of the move to.
                * expr (int): number of days before move expires.
                * max_views (int): max number of views for move.  
            
            Returns 
            -------
                * Status of operation (bool). True if submission was sucessful, false otherwise. 
        '''
        # create record of move 
        record = {"data":move}
        
        
        writer_id = self.client.client_id # not needed

        # write record to server
        result = self.client.write(data=record,record_type='move')

        record_id = result.get_meta().record_id # not needed

        # share record with recipients (try to if not shared previously)
        for recipient in recipients:
            print(f"sharing record with {recipient['client_id']}....")

            try:
                # share with client
                self.client.share('move',recipient['client_id'])
            except Exception as e:
                print(e)

        return 

    def retrieve_all_records(self):
        results = self.client.query()
        records = []
        for i in results:
            if 'client_id' in i.get_data():
                continue
            r = i.get_data()
            r['record_id'] = i.get_meta().record_id
            r['version'] = i.get_meta().version
            records.append(r)
        return records
    def search_records(self):

        query = Types.Search(include_all_writers=True,include_data=True).match(condition='AND',record_types=['move'])
        result = self.client.search(query)
        for i in result.records:
            print(i.to_json())
        return

    def remove_all_records(self):
        records = self.retrieve_all_records()
        for rec in records:
            self.client.delete(rec['record_id'],version=rec['version'])
        return
