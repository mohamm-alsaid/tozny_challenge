# TOZNY Challenge
## What
This is a Rock, Paper, Scissors game. It is a small project to expirement with developing simple application with ToznyStory python SDK [e3db-python](https://github.com/tozny/e3db-python) 
## Motivation
This is simple a project to examine my python proficiancy and ability to work/use with Tozny SDK.

## Set up
The following two steps create __3__ clients (alicia, bruce, and clarence) and register them. 

1. Ensure token is exported. Use: `export TOZNY_TOKEN='....your token...'` to export your token as an environment variable.
2. Initialize environment, run init script `python3 init.py`
    * Or you can run it as executable: `chmod +x init.py && ./init.py`

Their configuration (all __3__ of them) will be stored in `./creds` directory (relative to the current directory).

## Play game
The followings are options or flags players can use to do various things in the game.
* Display: `--display <True | False>`. 
    * Defualt is `False`, so no need to use this flag if silent mode is wanted.
* Reset (clarence only): `--reset <True | False>`
    * Defualt is `False`.
    * Only clarence (judge) is allowed to reset the game.
* Submit move: `--submit_move <rock | paper | scissors>`
* Declare (clarence only): `--declare <True | False>`
    * Defualt is `False`.
    * Only clarence (judge) is allowed to declare the game winner.
* Creds (in case a different path/ or directory name is used): `--creds < creds | or different path/directory>`
    * Default is `./creds`
## Examples of how to run the program
To run the program use: `python3 rock_paper_scissors.py --move rock --client alicia --creds ./.creds/alicia`
