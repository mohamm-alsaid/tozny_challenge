import unittest, json
from clients import Clients, AllClients, Moves

class TestClientsClass(unittest.TestCase):
    # ------------------test retrieve_client_creds-------------------
    def test_retreive_creds_success(self):
        client_name = 'bruce'
        # grab creds through clients
        client_creds = Clients().retrieve_client_creds(client_name)
        
        # grab creds manually
        with open(f'./creds/{client_name}.json','r') as f:
            creds = json.load(f)
        self.assertEqual(creds,client_creds)
    def test_retreive_creds_fail(self):
        client_name = 'random_name'
        creds = None
        # grab creds through clients (incorrect client name throughs exception)
        try:
            creds = Clients().retrieve_client_creds(client_name)
        except KeyError:
            pass
        self.assertEqual(creds,None) # still remains None
        return

    def test_retreive_creds_fail(self):
        clients_names = ('bruce','alicia')
        # grab file through clients (bruce)
        client_creds = Clients().retrieve_client_creds(clients_names[0])
        
        # grab creds manually (alicia)
        with open(f'./creds/{clients_names[-1]}.json','r') as f:
            creds = json.load(f)
        self.assertNotEqual(creds,client_creds) # Obtains other client
        return

    # ---------------------------------------------------------------

    # -----------------test reverse client_id look up------------------

    def test_reverse_lookup_client_id_success(self):
        clients = Clients()
        names = ['bruce', 'alicia', 'clarence']

        # iterate over clients names
        for name in names:
            # grab creds through clients
            client = clients.retrieve_client_creds(name)
            returned_name = clients.reverse_lookup_client_id(client['client_id'])
            self.assertEqual(returned_name,name)
        return
    def test_reverse_lookup_client_id_fail(self):
        clients = Clients()
        name = 'random'
        returned_name = None
        creds = None

        try:
            returned_name = clients.reverse_lookup_client_id(name)
        except KeyError:
            pass
        self.assertNotEqual(returned_name,name)
        self.assertEqual(returned_name,None)
        self.assertEqual(creds,None)
        return
    # -----------------------------------------------------------------

class TestAllClientsClass(unittest.TestCase):
    # ------------------test AllClients Enum ---------------------
    def test_clients_names_success(self):
        clients = AllClients
        names = sorted(['bruce','alicia', 'clarence']) # because I am too lazy to sort it :)

        for i in range(len(names)):
            exists = names[i] in clients.__members__
            value = clients[names[i]].value
            self.assertEqual(exists,True)
            self.assertEqual(value,i)
        return
    def test_clients_names_fail(self):
        clients = AllClients
        value = None
        try:
            returned_value = clients['random'].value
        except (KeyError,ValueError):
            pass
        self.assertEqual(value,None)
        return

    # ---------------------------------------------------------------

class TestMovesClass(unittest.TestCase):
    # ------------------test AllClients Enum ---------------------
    def test_moves_enum_success(self):
        moves = Moves
        moves = sorted(['rock','paper', 'scissors']) # because I am too lazy to sort it :)

        for i in range(len(test_moves_enum_success)):
            exists = test_moves_enum_success[i] in moves.__members__
            value = clients[test_moves_enum_success[i]].value
            self.assertEqual(exists,True)
            self.assertEqual(value,i)
        return
    def test_moves_enum_success(self):
        moves = Moves
        value = None
        try:
            returned_value = moves['lizard'].value
        except (KeyError,ValueError):
            pass
        self.assertEqual(value,None)
        return

    # ---------------------------------------------------------------