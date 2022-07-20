# The script of the game goes in this file.

define mc = Character("You")

# The game starts here.
label start:

    # set bg image
    scene bg_background1
    $ board_size_int = 19

    while True:
        "Set board size:"
        menu:
            "9x9":
                $ board_size_int = 9
            "19x19":
                $ board_size_int = 19
        "Choose colour:"
        menu:
            "play as black":
                call go_minigame(board_size_int, "B")
            "play as white":
                call go_minigame(board_size_int, "W")
            "local multiplayer":
                call go_minigame(board_size_int, "none")
            #"ai vs ai":
            #    call playing_go(19, "normal", "ai", "May")
    # This ends the game.
    return

label go_minigame(size = 19, colour = "B"):
    default position_9 = Position(xpos = -6, ypos = 370-14)
    # disable menus and rollback for go minigame
    $ renpy.block_rollback()
    $ _game_menu_screen = None
    $ quick_menu = False

    #choose board size
    $ set_board_size(size)

    # set up any handicap stones or other starting position by adding stones here TODO: label or function to input a list of moves for this
    # feed move to both ui and ai
    ##$ play_stone("B K10")
    ##$ w_gtp("play B K10")

    if (colour == "none"):
        # pVp
        call screen draw_board("none", size)
    elif (colour == "B"):
        # pVai, player as black
        call screen draw_board("B", size)
    elif (colour == "W"):
        # pVai, player as white
        call screen draw_board("W", size)
    #elif (colour == "ai"):
        # aiVaiW
        #call screen draw_board("ai", size)

    # screen returns winner/draw: "B","W","D"
    $ game_result = _return
    if (game_result == "B"):
        "game result black wins!"
    elif (game_result == "W"):
        "game result white wins!"
    else:
        "game result draw"
    return

    # game done

    # re-enable stuff after game
    $ _game_menu_screen = 'save'
    $ renpy.block_rollback()
    $ renpy.checkpoint()
