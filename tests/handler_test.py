import unittest, json, uuid, time
from member_handler import *
from clients import Clients, AllClients

class TestHandlerClass(unittest.TestCase):
    # ---------------------------------------------------------------
    def test_submit_retireve_record_success(self):
        unique_key = str(uuid.uuid4())
        record = {unique_key:'test'}
        handler = Handler(Clients().retrieve_client_creds('clarence'))
        # submit record
        return_value = handler.submit_record(record,recipients=[])

        # delay for effect to reflect on server (1 sec)
        time.sleep(1)
        # retrieve records from server
        records = handler.search_records()
        # filter records (get only datas)
        records = list(map(lambda x: x['data'],records))
        self.assertEqual(record in records,True)
        index = records.index(record)
        self.assertEqual(records[index][unique_key],record[unique_key])
        return
    def test_submit_retireve_record_fail(self):
        record = {str(uuid.uuid4()):'test'}
        handler = Handler(Clients().retrieve_client_creds('clarence'))
        # submit record
        return_value = handler.submit_record(record,recipients=[])
        
        # delay for effect to reflect on server (1 sec)
        time.sleep(1)

        # generate a new record with a new random key
        record = {str(uuid.uuid4()):'test'}
        # retrieve records from server
        records = handler.search_records()
        # filter records (get only datas)
        records = list(map(lambda x: x['data'],records))
        self.assertEqual(record in records,False)
        return
    def test_remove_all_records_success(self):
        clients = Clients()
        # flush anything on the server for the client
        for c in AllClients.__members__:
            Handler(clients.retrieve_client_creds(c)).remove_all_records()
        num = 2
        handler = Handler(clients.retrieve_client_creds('clarence'))
        # all_clients = list(map(lambda x: Clients().retrieve_client_creds(x),AllClients.__members__))
        for i in range(num):
            record = {str(uuid.uuid4()):'test'}
            # submit record
            return_value = handler.submit_record(record,recipients=[])
        
        # give server time to propagate changes
        time.sleep(.8)
        records = handler.search_records()
        # assert submission took place
        self.assertEqual(len(records)>=num,True)
        handler.remove_all_records()

        # give server time to propagate changes
        time.sleep(.8)
        records = handler.search_records()
        for r in records:
            print(r['data'])
        self.assertEqual(len(records)==0,True)
        # ------- test removing records with empty log -----------
        records = handler.search_records()
        self.assertEqual(len(records)==0,True)
    def test_remove_all_records_fail(self):
        record = {'data':'test'}
        clients = Clients()
        # submit a record and share it with clarence
        bruce_handler = Handler(clients.retrieve_client_creds('bruce'))
        # submit and share a record with clarence
        bruce_handler.submit_record(record,recipients=[clients.retrieve_client_creds('clarence')])
        handler = Handler(clients.retrieve_client_creds('clarence'))
        # remove all records of clarence
        handler.remove_all_records()
        # give server a chance to update
        time.sleep(.5)
        # ensure record was not removed (not created by clarence & it shouldn't)
        records = handler.search_records()
        records = list(map(lambda x: x['data'],records))
        self.assertEqual(len(records)>= 1,True)
        self.assertEqual(record in records,True)
    # ---------------------------------------------------------------