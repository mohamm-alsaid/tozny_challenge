# Author: mohamm-alsaid
# Date: 03/01/22

import argparse
from clients import Clients

def check_option_is_valid(option:str, options:dict):
    keys = list(options.keys())
    # avoid casing issues, lower everything
    option = option.lower()
    assert option in keys, f'Invalid program input. input: {option} possible options: {keys}'
    return option in keys


def main():
    # specify args args
    parser = argparse.ArgumentParser(description='Rock, Paper, Scissors Game.')
    parser.add_argument('--client', type=str, help='Clients for this game: <judge | alice | bruce>',default=None)
    # parse args
    args = parser.parse_args()
    client = args.client
    possible_clients = Clients.__members__

    check_option_is_valid(client,possible_clients) # always returns true if execution continues
    return

if __name__=="__main__":
    main()
    exit()