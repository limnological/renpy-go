# renpy-go
Boardgame Go minigame for Ren'Py

Player vs. player and player vs. ai modes. Board sizes 9x9 and 19x19.
The game can be run as a standalone or used as a minigame in another Ren'py game.


This project was heavily inspired by the Chess minigame for Ren'py at https://github.com/RuolinZheng08/renpy-chess
The Go ai currently used in this project is a modified version of https://github.com/maksimKorzh/wally,
It plays at around 25-30 kyu or total beginner level.


To integrate in your Ren'py project:
1. copy the 'go-engine' folder into your project's 'game' folder
2. copy the label 'go_minigame' from the 'script.rpy' file and call it as shown in the same file
3. the game result is returned by that label as "B", "W" or "D" for use in the broader game or for keeping track

![screenshot1](https://user-images.githubusercontent.com/101384203/180039126-67416a1b-9253-498d-b069-1c2d5bc1c0e1.png)


Future plans:
1. improving the scoring system, automatic dead group detection
2. implementing stronger ai
3. 13x13 board size
