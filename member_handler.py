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
    
    def submit_record(self, record: dict, recipients: list):
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
                * None. 
        '''

        # # share record with recipients (try to if not shared previously)
        for recipient in recipients:
            print(f"sharing record with {recipient['client_id']}....")

            try:
                # share with client
                self.client.share(record_type='move',reader_id=recipient['client_id'])
            except e3db.exceptions.APIError as e:
                print('record type was already shared')
        
        # write record to server
        result = self.client.write(data=record,record_type='move')
        print('records were written to server successfully')
        
        return  

    def search_records(self):
        '''
            Wrapper around search to retrieve all records (belonging to or shared with) the client
            param
            -----
                * None
            Returns
            ------
                * All records (created or shared with) for the client
        '''

        # include all writers is crucial here. Without it, the server only returns records belonging to current client (matching client_id)
        result = self.client.search(Types.Search(include_all_writers=True, include_data=True).match(record_types=['move']))
        records = []
        for record in result.records:
            records.append(record.to_json())
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
        records = self.search_records()

        # revoke access from all parties the record is shared with
        for party in shared_with:
            self.client.revoke('move',party['client_id'])
        for rec in records:
            if rec['meta']['writer_id']==self.client.client_id:
                self.client.delete(rec['meta']['record_id'],rec['meta']['version'])
        return
    