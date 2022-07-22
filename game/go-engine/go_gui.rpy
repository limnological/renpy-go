
define IMAGE_PATH = 'go-engine/images/'
image HOVER_IMG = IMAGE_PATH + "hover.png"


## GRAPHICS
# board size
define SCREEN_WIDTH = 1280
define SCREEN_HEIGHT = 720
define BOARD_SIDE_START = {9:370, 19:0}
define BOARD_SIDE_LENS = {9:333, 19:703} #37*19 = 703 for clean int positions (19x19 board)
#define BOARD_SIDE_LEN = 703
# distance between intersections of board lines
define INTERSECTION_LEN = 37


# turn on debug testing graphics mode
define testing_mode = False


# GAME/BOARD VARIABLES
# both file and rank index from 0 to 18 by default (19x19 board)
define INDEX_MIN = 0
define INDEX_MAX = 18

# 'a' == left == index 0
define FILE_LETTERS = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't')

# UI colours
define COLOR_HOVER = '#434f63' # Hover
define COLOR_SELECTED = '#40e0d0aa' # Turquoise
define COLOR_PREV_MOVE = '#6a5acdaa' # SlateBlue
define COLOR_WHITE = '#fff'


# turn and points
define game_over = False
define scoring_done = False
define pass_counter = 0
##define points = {"B":0,"W":6.5}
define points_w = 6.5
define points_b = 0

define ko_spot = -1
define previous_move = -1
define result = "" # draw, win, loss for player, nothing in pvp

# ui text variables
define winner = ""
define messages = "" # for displaying any special/error messages


# ai commands
define command_str = "" # to ai
define ai_return = "" # from ai


# squares/board encoding
init python:

    import copy
    import os
    import sys
    import pygame
    from collections import deque # track move history


    global WHOSE_TURN
    WHOSE_TURN = "B"

    # 9x9 GO ban
    board_9x9 = [
        7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
        7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7,
        7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7,
        7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7,
        7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7,
        7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7,
        7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7,
        7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7,
        7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7,
        7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7,
        7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7
    ]

    # 9x9 coordinates
    coords_9x9 = [
        'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX',
        'XX', 'A9', 'B9', 'C9', 'D9', 'E9', 'F9', 'G9', 'H9', 'J9', 'XX',
        'XX', 'A8', 'B8', 'C8', 'D8', 'E8', 'F8', 'G8', 'H8', 'J8', 'XX',
        'XX', 'A7', 'B7', 'C7', 'D7', 'E7', 'F7', 'G7', 'H7', 'J7', 'XX',
        'XX', 'A6', 'B6', 'C6', 'D6', 'E6', 'F6', 'G6', 'H6', 'J6', 'XX',
        'XX', 'A5', 'B5', 'C5', 'D5', 'E5', 'F5', 'G5', 'H5', 'J5', 'XX',
        'XX', 'A4', 'B4', 'C4', 'D4', 'E4', 'F4', 'G4', 'H4', 'J4', 'XX',
        'XX', 'A3', 'B3', 'C3', 'D3', 'E3', 'F3', 'G3', 'H3', 'J3', 'XX',
        'XX', 'A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'J2', 'XX',
        'XX', 'A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'J1', 'XX',
        'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX'
    ]

    # 13x13 GO ban
    board_13x13 = [
        7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
        7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7,
        7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7,
        7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7,
        7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7,
        7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7,
        7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7,
        7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7,
        7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7,
        7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7,
        7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7,
        7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7,
        7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7,
        7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7,
        7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7
    ]

    # 13x13 coordinates
    coords_13x13 = [
        'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX',
        'XX', 'A13','B13','C13','D13','E13','F13','G13','H13','J13','K13','L13','M13','N13','XX',
        'XX', 'A12','B12','C12','D12','E12','F12','G12','H12','J12','K12','L12','M12','N12','XX',
        'XX', 'A11','B11','C11','D11','E11','F11','G11','H11','J11','K11','L11','M11','N11','XX',
        'XX', 'A10','B10','C10','D10','E10','F10','G10','H10','J10','K10','L10','M10','N10','XX',
        'XX', 'A9', 'B9', 'C9', 'D9', 'E9', 'F9', 'G9', 'H9', 'J9', 'K9', 'L9', 'M9', 'N9', 'XX',
        'XX', 'A8', 'B8', 'C8', 'D8', 'E8', 'F8', 'G8', 'H8', 'J8', 'K8', 'L8', 'M8', 'N8', 'XX',
        'XX', 'A7', 'B7', 'C7', 'D7', 'E7', 'F7', 'G7', 'H7', 'J7', 'K7', 'L7', 'M7', 'N7', 'XX',
        'XX', 'A6', 'B6', 'C6', 'D6', 'E6', 'F6', 'G6', 'H6', 'J6', 'K6', 'L6', 'M6', 'N6', 'XX',
        'XX', 'A5', 'B5', 'C5', 'D5', 'E5', 'F5', 'G5', 'H5', 'J5', 'K5', 'L5', 'M5', 'N5', 'XX',
        'XX', 'A4', 'B4', 'C4', 'D4', 'E4', 'F4', 'G4', 'H4', 'J4', 'K4', 'L4', 'M4', 'N4', 'XX',
        'XX', 'A3', 'B3', 'C3', 'D3', 'E3', 'F3', 'G3', 'H3', 'J3', 'K3', 'L3', 'M3', 'N3', 'XX',
        'XX', 'A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'J2', 'K2', 'L2', 'M2', 'N2', 'XX',
        'XX', 'A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'J1', 'K1', 'L1', 'M1', 'N1', 'XX',
        'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX'
    ]



    # 19x19 GO ban
    board_19x19 = [
        7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7,
        7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7,
        7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7,
        7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7,
        7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7,
        7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7,
        7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7,
        7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7,
        7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7,
        7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7,
        7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7,
        7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7,
        7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7,
        7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7,
        7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7,
        7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7,
        7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7,
        7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7,
        7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7,
        7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7,
        7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7
    ]

    # 19x19 coordinates
    coords_19x19 = [
        'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX',
        'XX', 'A19','B19','C19','D19','E19','F19','G19','H19','J19','K19','L19','M19','N19','O19','P19','Q19','R19','S19','T19','XX',
        'XX', 'A18','B18','C18','D18','E18','F18','G18','H18','J18','K18','L18','M18','N18','O18','P18','Q18','R18','S18','T18','XX',
        'XX', 'A17','B17','C17','D17','E17','F17','G17','H17','J17','K17','L17','M17','N17','O17','P17','Q17','R17','S17','T17','XX',
        'XX', 'A16','B16','C16','D16','E16','F16','G16','H16','J16','K16','L16','M16','N16','O16','P16','Q16','R16','S16','T16','XX',
        'XX', 'A15','B15','C15','D15','E15','F15','G15','H15','J15','K15','L15','M15','N15','O15','P15','Q15','R15','S15','T15','XX',
        'XX', 'A14','B14','C14','D14','E14','F14','G14','H14','J14','K14','L14','M14','N14','O14','P14','Q14','R14','S14','T14','XX',
        'XX', 'A13','B13','C13','D13','E13','F13','G13','H13','J13','K13','L13','M13','N13','O13','P13','Q13','R13','S13','T13','XX',
        'XX', 'A12','B12','C12','D12','E12','F12','G12','H12','J12','K12','L12','M12','N12','O12','P12','Q12','R12','S12','T12','XX',
        'XX', 'A11','B11','C11','D11','E11','F11','G11','H11','J11','K11','L11','M11','N11','O11','P11','Q11','R11','S11','T11','XX',
        'XX', 'A10','B10','C10','D10','E10','F10','G10','H10','J10','K10','L10','M10','N10','O10','P10','Q10','R10','S10','T10','XX',
        'XX', 'A9', 'B9', 'C9', 'D9', 'E9', 'F9', 'G9', 'H9', 'J9', 'K9', 'L9', 'M9', 'N9', 'O9', 'P9', 'Q9', 'R9', 'S9', 'T9', 'XX',
        'XX', 'A8', 'B8', 'C8', 'D8', 'E8', 'F8', 'G8', 'H8', 'J8', 'K8', 'L8', 'M8', 'N8', 'O8', 'P8', 'Q8', 'R8', 'S8', 'T8', 'XX',
        'XX', 'A7', 'B7', 'C7', 'D7', 'E7', 'F7', 'G7', 'H7', 'J7', 'K7', 'L7', 'M7', 'N7', 'O7', 'P7', 'Q7', 'R7', 'S7', 'T7', 'XX',
        'XX', 'A6', 'B6', 'C6', 'D6', 'E6', 'F6', 'G6', 'H6', 'J6', 'K6', 'L6', 'M6', 'N6', 'O6', 'P6', 'Q6', 'R6', 'S6', 'T6', 'XX',
        'XX', 'A5', 'B5', 'C5', 'D5', 'E5', 'F5', 'G5', 'H5', 'J5', 'K5', 'L5', 'M5', 'N5', 'O5', 'P5', 'Q5', 'R5', 'S5', 'T5', 'XX',
        'XX', 'A4', 'B4', 'C4', 'D4', 'E4', 'F4', 'G4', 'H4', 'J4', 'K4', 'L4', 'M4', 'N4', 'O4', 'P4', 'Q4', 'R4', 'S4', 'T4', 'XX',
        'XX', 'A3', 'B3', 'C3', 'D3', 'E3', 'F3', 'G3', 'H3', 'J3', 'K3', 'L3', 'M3', 'N3', 'O3', 'P3', 'Q3', 'R3', 'S3', 'T3', 'XX',
        'XX', 'A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'J2', 'K2', 'L2', 'M2', 'N2', 'O2', 'P2', 'Q2', 'R2', 'S2', 'T2', 'XX',
        'XX', 'A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'J1', 'K1', 'L1', 'M1', 'N1', 'O1', 'P1', 'Q1', 'R1', 'S1', 'T1', 'XX',
        'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX', 'XX'
    ]

    # boards lookup
    BOARDS = {
         '9': board_9x9,
        '13': board_13x13,
        '19': board_19x19
    }

    # coords lookup
    COORDS = {
         '9': coords_9x9,
        '13': coords_13x13,
        '19': coords_19x19,
    }

    # stones
    EMPTY = 0
    BLACK = 1
    WHITE = 2
    MARKER = 4
    BOARDEDGE = 7
    LIBERTY = 8

    # count
    liberties = []
    block_count = []
    # count liberty
    liberty_block_count = []
    edge_colours = []

    # current board used
    board = BOARDS['19']
    coords = COORDS['19']

    # GO ban size
    BOARD_WIDTH = 0
    MARGIN = 2
    BOARD_RANGE = BOARD_WIDTH + MARGIN


    # set Go ban size (only 9,13,19 defined)
    def set_board_size(size = 19):
        # hook global variables
        global BOARD_WIDTH, BOARD_RANGE, board, coords, board_score_coords
        # calculate current board size
        BOARD_WIDTH = size
        BOARD_RANGE = BOARD_WIDTH + MARGIN
        board = BOARDS[str(size)]
        coords = COORDS[str(size)]

        # score counter as copy of board coords, not very smart solution
        board_score_coords = copy.deepcopy(board)

        # set ai board
        w_set_board_size(str(size))


    # game logic
    # count liberties, save stone group coords
    def count(square, played_color):
        # init piece
        piece = board[square]

        # skip board edge squares
        if piece == BOARDEDGE: return

        # if there's a stone at square
        if piece and piece & played_color and (piece & MARKER) == 0:
            # save stone's coordinate
            block_count.append(square)

            # mark the stone
            board[square] |= MARKER

            # recursive look for neighbours
            count(square - BOARD_RANGE, played_color) # N
            count(square - 1, played_color)           # E
            count(square + BOARD_RANGE, played_color) # S
            count(square + 1, played_color)           # W

        # if the square is empty
        elif piece == EMPTY:
            # mark liberty
            board[square] |= LIBERTY

            # save liberty
            liberties.append(square)

    # test liberty edges, save liberty group coords, bordering colours
    def count_liberty(square):
        global edge_colours, board_score_coords
        # init piece
        piece = board[square]
        # skip board edge squares
        if piece == BOARDEDGE:
             return

        # if the square is empty (or marker)
        elif (piece == EMPTY): # or (piece & MARKER) == 0):
            # mark liberty in board_score_coords
            board_score_coords[square] |= 8 # 8: 'neutral empty' for now, check edge colours at the end
            # save liberty
            liberty_block_count.append(square)
            # mark the stone
            board[square] |= MARKER
            # recursive look for neighbours
            count_liberty(square - BOARD_RANGE) # N
            count_liberty(square - 1)           # E
            count_liberty(square + BOARD_RANGE) # S
            count_liberty(square + 1)           # W
            return

        # if there's a stone at square
        elif piece and (piece & MARKER) == 0:
            # test if marked dead
            if (not ((board_score_coords[square] == 5) or (board_score_coords[square] == 6))):
                # add to liberty edge colour
                edge_colours.append(board[square])
                #return
        return

    # remove captured stones
    def clear_block(color = EMPTY, capturing_move=-1):
        global WHOSE_TURN, ko_spot, points_w, points_b
        if (WHOSE_TURN == "B"):
            clr = BLACK
        else:
            clr = WHITE

        #temp_block_count = copy.deepcopy(block_count)
        # test if need to update ko situation (1 stone group captured)
        if (len(block_count) == 1):
            # test if captured by 1 stone group by going through capturing stone surroundings
            no_capturing_group = True
            if (board[capturing_move - BOARD_RANGE] == clr):
                no_capturing_group = False
            elif (board[capturing_move - 1] == clr):
                no_capturing_group = False
            elif (board[capturing_move + BOARD_RANGE] == clr):
                no_capturing_group = False
            elif (board[capturing_move + 1] == clr):
                no_capturing_group = False
            # if 1 stone group capturing, update ko_spot
            if (no_capturing_group):
                ko_spot = block_count[0]

        for captured in block_count:
            board[captured] = EMPTY
            if (WHOSE_TURN == "B"):
                points_b = points_b + 1
            else:
                points_w = points_w + 1

    # clear groups
    def clear_groups():
        # hook global variables
        global block_count, liberties, liberty_block_count, edge_colours

        # clear block and liberties lists
        block_count = []
        liberties = []

        # score counting phase
        if (game_over):
            liberty_block_count = []
            edge_colours = []


    # restore and unmark the board after counting stones
    def restore_board():
        # clear groups
        clear_groups()

        # unmark stones
        for square in range(BOARD_RANGE * BOARD_RANGE):
            # restore piece if the square is on board
            if (board[square] != BOARDEDGE):
                board[square] &= 3 #NOTE: figure out why this
                #board[square] = EMPTY  #board[square] &= 3

    # clear board, restart game
    def clear_board():
        global game_over,scoring_done,result,WHOSE_TURN,board_score_coords,points_w, points_b, ko_spot, previous_move  #points
        # clear board
        clear_groups()
        for square in range(len(board)):
            if board[square] != BOARDEDGE: board[square] = 0

        # reset variables
        points_b = 0
        points_w = 6.5
        game_over = False
        scoring_done = False
        pass_counter = 0
        ko_spot = -1
        previous_move = -1
        WHOSE_TURN = "B"
        result = ""
        board_score_coords = copy.deepcopy(board)

        # clear ai board
        w_gtp("clear_board")

    # make move on board
    def set_stone(square, played_color):
        global ko_spot
        ko_spot = -1
        # make move on board
        board[square] = played_color

        # handle captures
        captures(3 - played_color, square)


    # play command
    def play_stone(command):
        global pass_counter, game_over, previous_move
        # parse color
        played_color = BLACK if command.split()[0] == 'B' else WHITE

        # pass move
        if command.split()[-1] == 'pass':
            pass_counter = pass_counter + 1
            if (pass_counter == 3):
                game_over = True
                count_score()
            return

        # parse square
        square_str = command.split()[-1]
        col = ord(square_str[0]) - ord('A') + 1 - (1 if ord(square_str[0]) > ord('I') else 0)
        row_count = int(square_str[1:]) if len(square_str[1:]) > 1 else ord(square_str[1:]) - ord('0')
        row = (BOARD_RANGE - 1) - row_count
        square = row * BOARD_RANGE + col

        # make move
        set_stone(square, played_color)
        # reset pass counter for game over
        pass_counter = 0
        previous_move = square


    # player pass turn function to be called from button
    def pass_turn():
        global ko_spot, previous_move
        previous_move = -1
        ko_spot = -1
        turn_change()
        play_stone(WHOSE_TURN + " pass")
        renpy.restart_interaction()


    # handle captures
    def captures(played_color = EMPTY, capturing_move=-1):
        # loop over the board squares
        for square in range(len(board)):
            # init piece
            piece = board[square]

            # skip board edge squares
            if piece == BOARDEDGE: continue

            # if stone belongs to the given color
            if piece & played_color:
                # count liberties
                count(square, played_color)

                # if no liberties left remove the stones
                if len(liberties) == 0: clear_block(played_color,capturing_move)

                # restore the board
                restore_board()

    # edge detection
    def detect_edge(square):
        # loop over 4 directions
        for direction in [BOARD_RANGE, 1, -BOARD_RANGE, -1]:
            # indeed, it's the board edge
            if board[square + direction] == BOARDEDGE: return 1

        # not, it's not the board edge
        return 0

    # find best liberty to extend/surround #NOTE: unused currently, for ai
    def evaluate(played_color):
        # max number of liberties found
        best_count = 0
        best_liberty = liberties[0]

        # loop over the liberties within the list
        for liberty in liberties:
            # put stone on board
            board[liberty] = played_color

            # count new liberties
            count(liberty, played_color)

            # found more liberties
            if len(liberties) > best_count and not detect_edge(liberty):
                best_liberty = liberty
                best_count = len(liberties)

            # restore board
            restore_board()

            # remove stone off board
            board[liberty] = EMPTY

        # return best liberty
        return best_liberty

    def test_liberty_move_legality(square, played_color):
        global messages, ko_spot

        # rules to check:

        # legal:
        # liberty of own group that won't lead to that groups death
        # liberty of enemy group that will be captured with this move

        # not legal:
        # liberty of own group that will lead to that groups death
        # liberty of enemy group that will not be captured with this move
        # illegal ko situations


        # name to num, representation of colour
        if (WHOSE_TURN == "B"):
            colour_num = BLACK
        else:
            colour_num = WHITE

        legal = False # guilty until proven innocent
        # the colour of the group in which liberty a move is being played
        liberty_colour = 0
        # the groups liberties count
        # 1 -> killing move, check colour
        # 2+ -> not killing move -> legal
        num_of_liberties = 0
        # loop over 4 directions
        for direction in [BOARD_RANGE, 1, -BOARD_RANGE, -1]:
            # skip the board edge until group stones found
            if board[square + direction] == BOARDEDGE:
                pass
            # stone found, note: might be touching multiple groups so don't stop looking
            else:
                # check colour
                liberty_colour = board[square + direction]
                # count liberties
                count(square + direction, liberty_colour)
                num_of_liberties = len(liberties)
                restore_board()

                # test if move is legal
                if num_of_liberties > 1:
                    if (liberty_colour == colour_num):

                        # test ko issues NOTE: unneeded here?
                        if (square == ko_spot):
                            # illegal ko move
                            messages = "Illegal Ko move."
                            renpy.restart_interaction()
                            return False

                        return True # legal since won't kill
                    elif (liberty_colour == EMPTY):
                        pass
                        #return True # legal since empty spot
                    elif ((liberty_colour == BLACK and colour_num == WHITE) or (liberty_colour == WHITE and colour_num == BLACK)):
                        pass #
                        #count(square, played_color)
                        #if (0 < len(liberties)):
                        #    restore_board()
                        #    return True # legal since played stone will have at least 1 liberty
                        #else:
                        #    restore_board()
                            #return False # not legal suicide move
                    else:
                        pass
                        #return False # not legal suicide move

                else: # 1 liberty
                    if (liberty_colour == colour_num):
                        #return False # not legal suicide move
                        pass
                    else:

                        # finally: test ko issues
                        if (square == ko_spot):
                            # illegal ko move
                            messages = "Illegal Ko move."
                            renpy.restart_interaction()
                            return False

                        return True # legal since will kill

                #break
        restore_board()
        return False # not legal

    # game over count score
    def count_score():
        global winner, points_w, points_b, board_score_coords, edge_colours, block_count, board #points

        # mark squares for counting in board_score_coords
        # 0 = not tested yet
        # 1 = black stone
        # 2 = white stone
        # 3 = empty black point: b+1
        # 4 = empty white point: w+1
        # 5 = white stone dead: b+2
        # 6 = black stone dead: w+2
        # 7 = boardedge
        # 8 empty, proven neutral


        # step 1: estimate dead groups, count_score()
        # step 2: player marks dead groups, recount_score
        # step 3: count points based on step 2 groups, count_score_done()


        # go through each spot looking for stones
        for square in range(BOARD_RANGE * BOARD_RANGE):
            # test position
            if ((board[square] != BOARDEDGE) and (board_score_coords[square] == 0)):
                # black stone
                if (board[square] == 1):
                    count(square, 1)
                    # test if has 2 eyes
                    #num_of_liberties = len(liberties)
                    for square in block_count:
                        board_score_coords[square] = 1 # assumed alive for now
                    restore_board() # reset any changes/markings made

                # white stone
                elif (board[square] == 2):
                    count(square, 2)
                    #num_of_liberties = len(liberties)
                    for square in block_count:
                        board_score_coords[square] = 2 # assumed alive for now
                    restore_board() # reset any changes/markings made

        # go through each spot looking for empty areas
        for square in range(BOARD_RANGE * BOARD_RANGE):
            # test position
            if ((board[square] != BOARDEDGE) and (board_score_coords[square] == 0)):
                # unhandled empty spot or group
                if (board[square] == 0):
                    count_liberty(square)
                    # if only black edges
                    if ((1 in edge_colours) and not (2 in edge_colours)):
                        for square in liberty_block_count:
                            board_score_coords[square] = 3 # surrounded by black
                    # if only white edges
                    elif ((2 in edge_colours) and not (1 in edge_colours)):
                        for square in liberty_block_count:
                            board_score_coords[square] = 4 # surrounded by white
                    # else remain neutral 8
                    restore_board() # reset any changes/markings made

        renpy.restart_interaction()
        return

    # recount score after marking dead groups
    def recount_score():
        global winner, points_w, points_b, board_score_coords, edge_colours, block_count, board #points

        # go through each spot looking for empty areas to score
        for square in range(BOARD_RANGE * BOARD_RANGE):
            # test position
            if ((board[square] != BOARDEDGE) and (board[square] == 0)):
                count_liberty(square)
                # if only black edges
                if ((1 in edge_colours) and not (2 in edge_colours)):
                    for square in liberty_block_count:
                        board_score_coords[square] = 3 # surrounded by black
                # if only white edges
                elif ((2 in edge_colours) and not (1 in edge_colours)):
                    for square in liberty_block_count:
                        board_score_coords[square] = 4 # surrounded by white
                # else remain neutral 8
            restore_board()
        restore_board() # reset any changes/markings made
        renpy.restart_interaction()
        return

    def count_score_done():
        global winner, points_w,points_b, board_score_coords, scoring_done, result #points
        # groups marked, count points
        for stone in board_score_coords:
            if (stone == 3):
                points_b = points_b + 1
            elif (stone == 4):
                points_w = points_w + 1
            elif (stone == 5):
                points_b = points_b + 2
            elif (stone == 6):
                points_w = points_w + 2
            # else: stone or neutral empty +-0

        # choose winner
        if (points_b > points_w):
            winner = "Black wins!"
            result = "B"
        elif (points_w > points_b):
            winner = "White wins!"
            result = "W"
        else:
            winner = "Draw!"
            result = "D"
        scoring_done = True
        renpy.restart_interaction()

    def resign():
        global game_over, winner, result, scoring_done, points_b, points_w, WHOSE_TURN
        game_over = True
        scoring_done = True
        points_b = 0
        points_w = 0
        if (WHOSE_TURN == "B"):
            winner = "White wins!"
            result = "W"
        else:
            winner = "Black wins!"
            result = "B"
        renpy.restart_interaction()


    ## Displaybles
    # mouse hover over spots displayable
    class HoverDisplayable(renpy.Displayable):
         #Highlights the hovered spot in green
        def __init__(self, board_size=19):
            super(HoverDisplayable, self).__init__()
            self.hover_coord = None
            hover_img = Image(IMAGE_PATH +"hover.png")
            self.hover_img = hover_img
            self.board_size = board_size

        def render(self, width, height, st, at):
            render = renpy.Render(width, height)
            if self.hover_coord:
                render.place(self.hover_img,
                    x=self.hover_coord[0], y=self.hover_coord[1],
                    width=INTERSECTION_LEN, height=INTERSECTION_LEN)
            return render

        def event(self, ev, x, y, st):
            if 0 < x < BOARD_SIDE_LENS[self.board_size] and BOARD_SIDE_START[self.board_size] < y < (BOARD_SIDE_START[self.board_size]+BOARD_SIDE_LENS[self.board_size]) and ev.type == pygame.MOUSEMOTION:
                self.hover_coord = round_coord(x, y)
                renpy.redraw(self, 0)

    # game displayable
    class goDisplayable(renpy.Displayable):
        """
        The main displayable for the go minigame
        If player_color is None, use Player vs. Player mode
        Else, use Player vs. ai mode
        """
        def __init__(self, player_color="none", board_size = 19):
            super(goDisplayable, self).__init__()

            self.player_color = player_color
            self.board_size = board_size

            # displayables
            self.selected_img = Solid(COLOR_SELECTED, xsize=INTERSECTION_LEN, ysize=INTERSECTION_LEN)
            self.highlight_img = Solid(COLOR_PREV_MOVE, xsize=INTERSECTION_LEN, ysize=INTERSECTION_LEN)


        def render(self, width, height, st, at):
            render = renpy.Render(width, height)
            renpy.restart_interaction() # force refresh the screen
            return render


        # handle click events
        def event(self, ev, x, y, st):
            global ko_spot, WHOSE_TURN, messages

            # AI's turn in Player vs. AI mode
            if (self.player_color != "ai") and (self.player_color != "none") and (WHOSE_TURN != self.player_color):
                legal_move = False
                while (not legal_move):
                    command_str = ("genmove "+ WHOSE_TURN)
                    ai_return = w_gtp(command_str)
                    # pass
                    if (ai_return == ''):
                        legal_move = True
                        pass_turn()
                        messages = "ai pass"
                        return

                    # parse square
                    square_str = ai_return
                    col = ord(square_str[0]) - ord('A') + 1 - (1 if ord(square_str[0]) > ord('I') else 0)
                    row_count = int(square_str[1:]) if len(square_str[1:]) > 1 else ord(square_str[1:]) - ord('0')
                    row = (BOARD_RANGE - 1) - row_count
                    square = row * BOARD_RANGE + col

                    legal_move = test_liberty_move_legality(square, WHOSE_TURN)
                    if (legal_move):
                        play_stone(WHOSE_TURN + " " + ai_return)
                        turn_change()
                        ### messages = ai_return # show prev move for testing
                        renpy.restart_interaction()
                        return

            # otherwise regular gameplay interaction
            if 0 < x < BOARD_SIDE_LENS[self.board_size] and BOARD_SIDE_START[self.board_size] < y < (BOARD_SIDE_START[self.board_size]+BOARD_SIDE_LENS[self.board_size]) and ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                # get coords based on mouse x, y
                played_stone_coords_x,played_stone_coords_y = coord_to_square((x,y))
                square = (played_stone_coords_y * BOARD_RANGE) + played_stone_coords_x
                square_coords = coords[square]

                ###
                #stones
                #EMPTY = 0
                #BLACK = 1
                #WHITE = 2
                #MARKER = 4
                #BOARDEDGE = 7
                #LIBERTY = 8
                ###

                # test move legality
                legal_move = False
                stone_num = get_stone_at(played_stone_coords_x,played_stone_coords_y)
                # test if spot occupied
                if (stone_num == 1 or stone_num == 2):
                    return

                # empty, non-liberty: go ahead
                legal_move = test_liberty_move_legality(square, WHOSE_TURN)

                if (legal_move):
                    if (WHOSE_TURN == "B"):
                        #ko_spot = -1 # clear ko
                        play_stone("B " + square_coords)
                        w_gtp("play B " + square_coords)
                        turn_change()
                    else:
                        #ko_spot = -1 # clear ko
                        play_stone("W " + square_coords)
                        w_gtp("play W " + square_coords)
                        turn_change()
                renpy.restart_interaction() # force refresh the screen


    # game over displayable
    class gameOverDisplayable(renpy.Displayable):
        """
        The game over displayable for choosing dead groups
        """
        def __init__(self, player_color="none", board_size=19):
            super(gameOverDisplayable, self).__init__()
            self.board_size = board_size

        def render(self, width, height, st, at):
            render = renpy.Render(width, height)
            renpy.restart_interaction() # force refresh the screen
            return render

        # handle click events
        def event(self, ev, x, y, st):
            if ((not scoring_done) and (0 < x < BOARD_SIDE_LENS[self.board_size]) and (BOARD_SIDE_START[self.board_size] < y < (BOARD_SIDE_START[self.board_size]+BOARD_SIDE_LENS[self.board_size])) and (ev.type == pygame.MOUSEBUTTONDOWN) and (ev.button == 1)):
                # get stone
                played_stone_coords_x,played_stone_coords_y = coord_to_square((x,y))
                square = (played_stone_coords_y * BOARD_RANGE) + played_stone_coords_x
                square_coords = coords[square]

                stone_num = get_stone_at(played_stone_coords_x,played_stone_coords_y)

                # mark squares for counting in board_score_coords
                # 0 = not tested yet
                # 1 = black stone
                # 2 = white stone
                # 3 = empty black point: b+1
                # 4 = empty white point: w+1
                # 5 = white stone dead: b+2
                # 6 = black stone dead: w+2
                # 7 = boardedge
                # 8 empty, proven neutral

                # black group
                if (stone_num == BLACK):
                    # count group
                    count(square, stone_num)
                    alive = board_score_coords[square]
                    # alive black group -> dead black group
                    if (alive == 1):
                        for a in block_count:
                            board_score_coords[a] = 6
                    # dead black group -> alive black group
                    else:
                        for a in block_count:
                            board_score_coords[a] = 1

                # white group
                elif (stone_num == WHITE):
                    # count group
                    count(square, stone_num)
                    alive = board_score_coords[square]
                    # alive white group -> dead white group
                    if (alive == 2):
                        for a in block_count:
                            board_score_coords[a] = 5
                    # dead white group -> alive white group
                    else:
                        for a in block_count:
                            board_score_coords[a] = 2
                # reset any changes/markings made
                restore_board()
                # call scoring for new situation
                recount_score()
                renpy.restart_interaction() # force refresh the screen


    # misc functions
    # turns change
    def turn_change():
        global WHOSE_TURN, messages
        messages = "" # clear special messages
        if (WHOSE_TURN == "B"):
            WHOSE_TURN = "W"
        elif (WHOSE_TURN == "W"):
            WHOSE_TURN = "B"


    # get stone colour / empty at spot
    def get_stone_at(file_idx, rank_idx):
            stone = board[rank_idx * BOARD_RANGE + file_idx]
            return stone

    # for drawing, computes cursor coord rounded to the upperleft coord of the current loc
    def round_coord(x, y):
        x_round = int(x / INTERSECTION_LEN) * INTERSECTION_LEN
        y_round = int(y / INTERSECTION_LEN) * INTERSECTION_LEN
        return (x_round, y_round)

    # rank and file -> draw position conversions, for drawing stones based on board info
    def indices_to_coord(file, rank):
        x = INTERSECTION_LEN * (file-1)
        y = INTERSECTION_LEN * (INDEX_MAX - (rank-1))
        return (x, y)

    # draw position -> rank and file conversions, for placing stone based on mouse click position
    def coord_to_square(coord):
        x, y = coord
        file = int(x / INTERSECTION_LEN)+1
        rank = int(INDEX_MAX - (y / INTERSECTION_LEN))+2 # rank 1 not working?
        if (y > 18*INTERSECTION_LEN): # ^ ugly solution, TODO: clean up later!
            rank = 1
        return file, rank

    # TODO: ai v ai make move
    def ai_play():
        global WHOSE_TURN, ai_return
        ctr = 1
        while ctr > 0:
            ctr = ctr - 1
            legal_move = False
            while (not legal_move):
                command_str = ("genmove "+ WHOSE_TURN)
                ai_return = w_gtp(command_str)

                # parse square
                square_str = ai_return
                col = ord(square_str[0]) - ord('A') + 1 - (1 if ord(square_str[0]) > ord('I') else 0)
                row_count = int(square_str[1:]) if len(square_str[1:]) > 1 else ord(square_str[1:]) - ord('0')
                row = (BOARD_RANGE - 1) - row_count
                square = row * BOARD_RANGE + col

                legal_move = test_liberty_move_legality(square, WHOSE_TURN)
                if (legal_move):
                    play_stone(WHOSE_TURN + " " + ai_return)
                    turn_change()
                    messages = ai_return # show prev move
                    renpy.restart_interaction()
        return

    def quit_engine():
        pass
        # NOTE: does not do anything with current ai since w_gtp not continuous process, only called when needed. Might be needed with other ai?
        # TODO: do some memory/variable cleanup here? delete w_ variables?
        #try:
        #    w_gtp('quit')
        #except SystemExit:
        #    pass

# draw game screen
screen draw_board(player_colour="none", board_size=19):
    # init diplayables

    # 9x9 board position
    ###$ position_9 = Position(xpos = 167, yoffset = -15)

    default stone_draw_position = (0,0)
    default hover_displayable = HoverDisplayable(board_size)
    default goDisplayable = goDisplayable(player_colour,board_size)
    default gameOverDisplayable = gameOverDisplayable(player_colour,board_size)
    text "Black:[points_b] White:[points_w]" size 40 xpos 760 ypos 400 color "#000"


    # board images
    if (board_size == 9):
        #show IMAGE_PATH + "go_board9.png" at position_9 as go_board9 #left
        add IMAGE_PATH + "go_board9.png" at position_9 ##xpos 167 yoffset -15

    elif (board_size == 19):
        add IMAGE_PATH + "go_board.png" at topleft


    # game text and ui
    if (not game_over):
        if (WHOSE_TURN == "B"):
            $ current_colour = "Black"
        elif (WHOSE_TURN == "W"):
            $ current_colour = "White"
        text "[current_colour] to move" size 40 xpos 760 ypos 360 color "#000"
        text "[messages]" size 40 xpos 760 ypos 320 color "#000"
        if (player_colour == "ai"):
            imagebutton auto IMAGE_PATH + " button_restart_%s.png" xalign 0.8 yalign 0.1 action [ai_play]
        if (WHOSE_TURN == player_colour or player_colour == "none" ):
            imagebutton auto IMAGE_PATH +"button_resign_%s.png" xalign 0.8 yalign 0.1 action [resign, renpy.restart_interaction]
            imagebutton auto IMAGE_PATH +"button_restart_%s.png" xalign 0.8 yalign 0.2 action [clear_board, renpy.restart_interaction]
            imagebutton auto IMAGE_PATH +"button_pass_%s.png" xalign 0.8 yalign 0.3 action [pass_turn, renpy.restart_interaction]
    # game over text
    else:
        if (not scoring_done):
            imagebutton auto IMAGE_PATH +"button_done_%s.png" xalign 0.8 yalign 0.1 action [count_score_done, renpy.restart_interaction]
        else:
            # exit minigame and clear everything
            imagebutton auto IMAGE_PATH +"button_exit_%s.png" xalign 0.8 yalign 0.1 action [quit_engine, clear_board, Return(result), renpy.restart_interaction]
            imagebutton auto IMAGE_PATH +"button_restart_%s.png" xalign 0.8 yalign 0.2 action [clear_board, renpy.restart_interaction]
            text "[winner]" size 60 xpos 760 ypos 340 color "#000"

    if (True): # was  if (not game_over):  before TODO: delete
        fixed xpos 0:
            #add Image(IMG_CHESSBOARD)
            add hover_displayable # hover loc over chosen spot
            if (not game_over):
                if (player_colour == "ai"):
                    pass
                else:
                    add goDisplayable # stones
            else:
                add gameOverDisplayable # choose dead stones

        # loop over board rows
        for row in range(BOARD_RANGE):
            # loop over board columns
            for col in range(BOARD_RANGE):
                # init square
                $ square = row * BOARD_RANGE + col
                # init stone
                $ stone = board[square]
                $ w_stone = w_board[square] # NOTE: for testing ai board
                $ stone_draw_position = indices_to_coord(col,row)

                # higlight previous move
                if (square == previous_move):
                    add IMAGE_PATH + "prev_move.png" xpos stone_draw_position[0] ypos stone_draw_position[1]
                # show stones + area control in scoring
                if (stone == 1):
                    add IMAGE_PATH + "piece_b.png" xpos stone_draw_position[0] ypos stone_draw_position[1]
                    if (game_over):
                        # test if stone alive
                        if ((board_score_coords[square] == 6)):
                            add IMAGE_PATH + "captured_black.png" xpos stone_draw_position[0] ypos stone_draw_position[1]
                elif (stone == 2):
                    add IMAGE_PATH + "piece_w.png" xpos stone_draw_position[0] ypos stone_draw_position[1]
                    if (game_over):
                        # test if stone alive
                        if (board_score_coords[square] == 5):
                            add IMAGE_PATH + "captured_white.png" xpos stone_draw_position[0] ypos stone_draw_position[1]
                elif ((board_score_coords[square] == 4)):
                    add IMAGE_PATH + "captured_black.png" xpos stone_draw_position[0] ypos stone_draw_position[1]
                elif ((board_score_coords[square] == 3)):
                    add IMAGE_PATH + "captured_white.png" xpos stone_draw_position[0] ypos stone_draw_position[1]

                # bug testing graphics
                if ((not game_over) and (testing_mode)):
                    # different stone in ai and ui board error
                    if (w_stone != stone):
                        add IMAGE_PATH + "testing/error_img.png" xpos stone_draw_position[0] ypos stone_draw_position[1]
                    # show ko positions
                    if (ko_spot == square):
                        add IMAGE_PATH + "testing/ko_b.png" xpos stone_draw_position[0] ypos stone_draw_position[1]
                    if (w_ko_spot == square):
                        add IMAGE_PATH + "testing/ko_w.png" xpos stone_draw_position[0] ypos stone_draw_position[1]
