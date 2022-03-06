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
            Submits a move to each of the recipients as a note.

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

    
    def search_records(self):
        '''
            Wrapper around search to retrieve all records (belong to or shared with) under client
            param
            -----
                * None
            Returns
            ------
                * All records (created or shared with) for the client
        '''
        result = self.client.search(Types.Search())
        records = []
        for record in result.records:
            print()
            records.append(record)
        return records

    def remove_all_records(self,shared_with: list=[]):
        '''
            Revokes access to all records of type 'move' and deletes records created by client
            param
            -------
                * shared_with (list): (optional) list of clients to ensure access is revoked from before deletion of records
                    * Note: would be nice if each record contains info about parties that share the record with client
            Returns
            -------  
                * None
        '''
        records = self.retrieve_all_records()
        # revoke access from all parties the record is shared with
        for party in shared_with:
            self.client.revoke('move',party['client_id'])
        for rec in records:
            self.client.delete(rec['record_id'],version=rec['version'])
        return