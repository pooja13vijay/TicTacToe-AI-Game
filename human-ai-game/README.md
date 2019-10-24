**Section A: Run the program**

To run the program:

1. Extract this folder.
2. Use Python3 with flask library installed.
3. Open terminal or command prompt (this can be achieved by selecting *open with terminal* with the button next to the environment name in Anaconda) and change to this directory.
4. If you are in Windows,
    ```
    set FLASK_APP=main.py
    ```
    if you are in Linux or MacOS,
    ```
    export FLASK_APP=main.py
    ```
5. Then, run it with
    ```
    flask run
    ```
6. You will see the following line among other lines
    ```
    * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
    ```
    it could be on a different port if your port `5000` is occupied.
7. Open the url in your browser.
8. If you see the tic-tac-toe game with *Game info* and *Log* on the right hand side, you have a working copy of the program that you can use to test your tic-tac-toe AI.

**Section B: Install `flask` library with Python3**

To use Python3 with flask library installed:

*The following steps assume the use of Anaconda*

1. You can either use the `base` environment or create a new environment with `Python 3.x`.
2. In Anaconda Navigator > Environments > *Select the environment you are going to use* > check if `flask` is installed
3. If `flask` is not installed, change to the list of uninstalled modules, search for `flask`, and install it.

**Section C: Use AI in the program**

Two dummy "AI" players are created to demonstrate the usage of this program.

1. Click on the **fourth** button (*choose players*) to select if player 1 and 2 are humans or AIs.
2. If AI is selected as the player 1, the **fifth** button (*trigger start*) need to be clicked to initiate the game. (This is only for initiation. This button does not need to be clicked during the game play. The AI will be called automatically.)

**Section D: Implement your AI in the program**

The folder structure of this program is
```
- player <-- you only need to care about this folder and its sub-folders
  - player1
  - player2
- static
  - frontend.css
  - frontend.html
  - frontend.js
- main.py
- README.md
```

Each sub-folder under `player` corresponds to one AI.

To test your AI with this program:

1. Create a new folder under `player` with a name consists of no space and no symbols other than underscore (_).
2. Under the new folder, there should be a `player.py` python file that holds the class `Player` with method `play()`. You can view folder for the dummy "AI" players for reference.
3. Reload your page in your browser, you should now be able to see your AI shown in the list of AI players available.

This folder that you should submit is in the same format as the folder you just created. 
* The folder name should be alphanumeric with no space and no symbols other than underscore (_).
* The python file to hold your `Player` class should be named `player.py`.
* Add another text file in the folder when you submit to list your group name, group icon, and group members. Check the file `group members.txt` under `player1` and `player2` for samples.
