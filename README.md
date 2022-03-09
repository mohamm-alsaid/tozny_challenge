# TOZNY Challenge
## What/Motivation
This is a Rock, Paper, Scissors game. It is a small project to experiment with developing simple application with ToznyStory python SDK [e3db-python](https://github.com/tozny/e3db-python).<br/>This is a simple project to examine my python proficiency and ability to work with/use Tozny SDK.

---
## Set up
The following two steps create __3__ clients (alicia, bruce, and clarence) and register them. 
1. Ensure all requirements are installed: `pip3 install -r requirements.txt`
2. Ensure the token is exported. Use `export TOZNY_TOKEN='....your token...'` to export your token as an environment variable.
3. Initialize environment, run init script `python3 init.py`
    * Or you can run it as executable: `chmod +x init.py && ./init.py`

Their configuration (all __3__ of them) will be stored in the `./creds` directory (relative to the current directory).

---
## Play game
The followings are options/flags players can use to do various things in the game.
* Display: `--display`. 
    * Defualt is `False`.
    * Example: `./game.py --client <client> --display`

* Reset (clarence only): `--reset`
    * Defualt is `False`.
    * Only clarence (judge) is allowed to reset the game.
    * Example: `./game.py --client clarence --reset`

* Submit move: `--submit_move <rock | paper | scissors>`
    * Only players are allowed to submit moves (`alicia` and `bruce`)
    * Example: `./game.py --client bruce --move rock`

* Declare (clarence only): `--declare`
    * Defualt is `False`.
    * Only clarence (judge) is allowed to declare the game winner.
    * Example: `./game.py --client clarence --declare`

* Creds (in case a different path/ or directory name is used): `--creds < creds | or different path/directory>`
    * Default is `./creds`
    * If default location is used, there is not need to specify the location:
        * Example: `./game.py --client <client> --move paper paper`
    * Otherwise, one needs to specify the location:
        * Example: `./game.py --client bruce --display --creds ./dir1/other_creds/`

---
## Examples of how to run the program
To run the program, use: `python3 game.py --move rock --client alicia`

If changed into executable, it is less verbose: `./game.py --move scissors --client bruce`
* To change the game into executable, use: `chmod +x game.py`
* One can then use the short examples above.
---
## Test
To run a particular unit tests, use: `python3 -m unittest tests.<name_of_test>`

To run all unit tests, use: `python3 -m unittests tests/*.py`
### Provided tests
* `game_test`: Tests the methods and logic of game
    * To run: `python3 -m unittests tests.game_test`
* `clients_test`: Tests the methods and logic in `Clients` class
    * To run: `python3 -m unittests tests.clients_test`
* `handler_test`: Tests the methods and logic in `Handler` class
    * To run: `python3 -m unittests tests.hanlder_test`
>__Note__: The tests run slow as there are many interactions of TONZY servers. <br/>This is not ideal for unit tests as tests shouldn't take several seconds to run (at least for a project this small).

---
## Resources
[1]- [Tonzy's Python SDK](https://github.com/tozny/e3db-python/)

[2]- [Tozny Dashboard](https://dashboard.tozny.com/register)

[3]- [TozStore Tutorials](https://www.youtube.com/playlist?list=PLVZ9ZKXxhcjR8clQEhWSoUYLaAwAtNy-B)