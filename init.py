#! /bin/python
import os, e3db, json
from member_handler import get_tozny_client_config

clients = ['alicia', 'bruce', 'clarence']
directory = 'creds'
# check if direcotry exists
isExist = os.path.exists(directory)
if not isExist:
    # create creds folder
    os.mkdir(directory)
# change directory 
os.chdir(directory)




# # ------------- grab token from environment ----------
key = 'TOZNY_TOKEN'
token = os.getenv(key)
assert not token == None, "Token was not found in environment. Try exporting token before running script." 
# ----------------------------------------------------

for client in clients:
    print(f'\ngenerating keypair for {client}...',end='')
    config = get_tozny_client_config(token,client)
    print('done')
    
    fname = f"{client}.json"
    
    config_dict = config() # returns json
    
    print(f'\nWriting {client} configurations to {directory}/{fname}...',end='')
    json.dump(config_dict,open(f"{client}.json",'w'),indent=4)
    print('done')