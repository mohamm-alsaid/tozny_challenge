#! /bin/python
import os, e3db, json

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
    public_key,private_key = e3db.Client.generate_keypair()
    print('done')
    client_info = e3db.Client.register(token, client, public_key)
    config = e3db.Config(
        client_info.client_id,
        client_info.api_key_id,
        client_info.api_secret,
        public_key,
        private_key
    )
    # config.write(profile='test.json')
    fname = f"{client}.json"
    config_dict = config.load()
    print(f'\nWriting {client} configurations to {directory}/{fname}...',end='')
    json.dump(config_dict,open(f"{client}.json",'w'),indent=4)
    print('done')