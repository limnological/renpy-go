# renpy-go
Boardgame Go minigame for Ren'Py
 
Player vs. player and player vs. ai modes. Board sizes 9x9 and 19x19.
The game can be run as a standalone or used as a minigame in another Ren'py game.
 
The Go ai used in this project is a modified version of https://github.com/maksimKorzh/wally


To integrate in your Ren'py project:
1. copy the 'go-engine' folder into your project's 'game' folder 
2. copy the label 'go_minigame' from the 'script.rpy' file and call it as shown in the same file
3. the game result is returned by that label as "B", "W" or "D" for use in the broader game or for keeping track