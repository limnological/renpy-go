init python:

    from __future__ import print_function

    import sys
    import random

    VERSION = '1.0'

    ###################################
    #
    #          Piece encoding
    #
    ###################################
    #
    # 0000 => 0    empty sqare
    # 0001 => 1    black stone
    # 0010 => 2    white stone
    # 0100 => 4    stone marker
    # 0111 => 7    offw_board square
    # 1000 => 8    liberty marker
    #
    # 0101 => 5    black stone marked
    # 0110 => 6    white stone marked
    #
    ###################################

    # 9x9 GO ban
    w_board_9x9 = [
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
    w_COORDS_9x9 = [
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
    w_board_13x13 = [
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
    w_COORDS_13x13 = [
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
    w_board_19x19 = [
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
    w_COORDS_19x19 = [
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

    # w_BOARDS lookup
    w_BOARDS = {
         '9': w_board_9x9,
        '13': w_board_13x13,
        '19': w_board_19x19
    }

    # w_COORDS lookup
    w_COORDS_ref = {
         '9': w_COORDS_9x9,
        '13': w_COORDS_13x13,
        '19': w_COORDS_19x19,
    }

    # stones
    EMPTY = 0
    BLACK = 1
    WHITE = 2
    MARKER = 4
    OFFBOARD = 7
    LIBERTY = 8

    # count
    w_liberties = []
    w_block = []

    w_ko_spot = -1
    w_edge_colours = []
    first_ai_move = True
    legal_moves = []

    # current w_board used
    #w_board = None
    #w_COORDS = None

    # GO ban size
    w_board_WIDTH = 0
    w_BOARD_RANGE = 0
    w_MARGIN = 2


    # set Go ban size
    def w_set_board_size(command):
        # hook global variables
        global w_board_WIDTH, w_BOARD_RANGE, w_board, w_COORDS, w_COORDS_ref, legal_moves, w_edge_colours, first_ai_move

        # parse the w_board size
        size = int(command.split()[-1])

        # throw error if w_board size is not supported
        if size not in [9, 13, 19]:
            print('? current w_board size not supported\n')
            return

        # calculate current w_board size
        w_board_WIDTH = size
        w_BOARD_RANGE = w_board_WIDTH + w_MARGIN
        w_board = w_BOARDS[str(size)]
        w_COORDS = w_COORDS_ref[str(size)]

        first_ai_move = True
        # store squares where legal moves can be made, the whole board at the start
        legal_moves = []
        for square_counter in range(len(w_board)):
            if (w_board[square_counter] == EMPTY):
                legal_moves.append(square_counter)

    # count w_liberties, save stone group w_COORDS
    def w_count(square, color):
        # init piece
        piece = w_board[square]

        # skip offw_board squares
        if piece == OFFBOARD: return

        # if there's a stone at square
        if piece and piece & color and (piece & MARKER) == 0:
            # save stone's coordinate
            w_block.append(square)

            # mark the stone
            w_board[square] |= MARKER

            # look for neighbours recursively
            w_count(square - w_BOARD_RANGE, color) # walk north
            w_count(square - 1, color)           # walk east
            w_count(square + w_BOARD_RANGE, color) # walk south
            w_count(square + 1, color)           # walk west

        # if the square is empty
        elif piece == EMPTY:
            # mark liberty
            w_board[square] |= LIBERTY

            # save liberty
            w_liberties.append(square)

    # test liberty edges, save liberty group coords, bordering colours
    def w_count_liberty(square):
        global w_edge_colours
        # init piece
        piece = w_board[square]
        # skip board edge squares
        if piece == OFFBOARD:
             return

        # if the square is empty
        elif (piece == EMPTY):
            ## save liberty
            #liberty_block_count.append(square)
            # mark the stone
            w_board[square] |= MARKER
            # recursive look for neighbours
            w_count_liberty(square - w_BOARD_RANGE) # N
            w_count_liberty(square - 1)           # E
            w_count_liberty(square + w_BOARD_RANGE) # S
            w_count_liberty(square + 1)           # W
            return

        # if there's a stone at square
        elif piece and (piece & MARKER) == 0:
            # add to liberty edge colours
            w_edge_colours.append(board[square])
        return

    # test if liberty has only edges of 1 colour (skip while first ai turn to stop passing)
    def w_test_edge_colours(square):
        global w_edge_colours, first_ai_move

        if (first_ai_move == True):
            return False
        w_count_liberty(square)
        if ((WHITE in w_edge_colours) and (BLACK not in w_edge_colours)):
            return True
        elif((BLACK in w_edge_colours) and (WHITE not in w_edge_colours)):
            return True
        else:
            return False

    # remove captured stones
    def w_clear_block(capturing_move = -1):
        global legal_moves, w_ko_spot, WHOSE_TURN

        if (WHOSE_TURN == "B"):
            clr = BLACK
        else:
            clr = WHITE

        # test if need to update ko situation
        # test if captured by 1 stone group by going through capturing stone surroundings
        no_capturing_group = True
        if (w_board[capturing_move - BOARD_RANGE] == clr):
            no_capturing_group = False
        elif (w_board[capturing_move - 1] == clr):
            no_capturing_group = False
        elif (w_board[capturing_move + BOARD_RANGE] == clr):
            no_capturing_group = False
        elif (w_board[capturing_move + 1] == clr):
            no_capturing_group = False
        # if 1 stone group capturing, update ko_spot
        if (no_capturing_group): #(len(w_block) == 1):
            w_ko_spot = w_block[0]

        for captured in w_block:
            w_board[captured] = EMPTY
            legal_moves.append(captured)

    # clear groups
    def w_clear_groups():
        # hook global variables
        global w_block, w_liberties, w_edge_colours

        # clear w_block and w_liberties lists
        w_block = []
        w_liberties = []
        w_edge_colours = []

    # restore the w_board after counting stones
    def w_restore_board():
        # clear groups
        w_clear_groups()

        # unmark stones
        for square in range(w_BOARD_RANGE * w_BOARD_RANGE):
            # restore piece if the square is on w_board
            if w_board[square] != OFFBOARD: w_board[square] &= 3

    # clear w_board
    def w_clear_board():
        global legal_moves, w_ko_spot, first_ai_move
        # clear groups
        w_clear_groups()

        for square in range(len(w_board)):
            if w_board[square] != OFFBOARD: w_board[square] = 0

        # reset variables
        w_ko_spot = -1
        first_ai_move = True
        legal_moves = []
        for square_counter in range(len(w_board)):
            if (w_board[square_counter] == EMPTY):
                legal_moves.append(square_counter)

    # make move on w_board
    def w_set_stone(square, color):
        global legal_moves, w_ko_spot
        w_ko_spot = -1
        # make move on w_board
        w_board[square] = color
        if (square in legal_moves):
            legal_moves.remove(square)

        # handle captures
        w_captures(3 - color)

    # generate random move
    def w_make_random_move(color):
        global legal_moves, w_edge_colours, first_ai_move
        # find empty random square

        # choose random legal move, pass if none exist
        if (0 == len(legal_moves)):
            return ''
        #random_square = random.choice(legal_moves) ##random.randrange(len(w_board))
        #while w_board[random_square] != EMPTY:
        #    random_square = random.randrange(len(w_board))


        # TODO: list of all good moves. good_moves = copy legal_moves, remove bad moves as found
        enemy_colour = -1
        if (color == WHITE):
            enemy_colour = BLACK
        else:
            enemy_colour = WHITE

        random_square = 0
        #good_moves = copy.deepcopy(legal_moves)
        #random.shuffle(good_moves) # randomize order
        not_good_move = True
        #for move in good_moves:
        counter = 0
        # test up to 50 moves
        while (not_good_move and (counter < 50)):
            counter = counter + 1
            # generate random move and test it
            move = random.choice(legal_moves)
            w_count_liberty(move)

            # if only one colour of surrounding stones, bad move: don't play
            if ((color in w_edge_colours) and (enemy_colour not in w_edge_colours) and (not first_ai_move)):
                w_restore_board()
                continue
            elif ((enemy_colour in w_edge_colours) and (color not in w_edge_colours) and (not first_ai_move)):
                w_restore_board()
                continue
            # otherwise "good move": play
            random_square = move
            w_restore_board()
            break
        if (counter == 50):
            return ''
        # make move
        w_set_stone(random_square, color)
        # count w_liberties
        w_count(random_square, color)

        # test suicide move
        if (len(w_liberties) < 2) :
            # restore w_board
            w_restore_board()

            # take off the stone
            w_board[random_square] = EMPTY

            # search for another move
            try:
                # return non suicide move
                return w_make_random_move(color)
            except:
                # pass the move
                return ''

        # restore w_board
        w_restore_board()

        # return the move
        # uncheck first move
        if (first_ai_move == True):
            first_ai_move = False
        return w_COORDS[random_square]

    # play command
    def w_play(command=""):
        global w_ko_spot
        # parse color
        color = BLACK if command.split()[1] == 'B' else WHITE

        # handle GUI pass move
        if command.split()[-1] == 'pass':
            w_ko_spot = -1
            return

        # parse square
        square_str = command.split()[-1]
        col = ord(square_str[0]) - ord('A') + 1 - (1 if ord(square_str[0]) > ord('I') else 0)
        row_count = int(square_str[1:]) if len(square_str[1:]) > 1 else ord(square_str[1:]) - ord('0')
        row = (w_BOARD_RANGE - 1) - row_count
        square = row * w_BOARD_RANGE + col

        # make GUI move
        w_set_stone(square, color)

    # handle captures
    def w_captures(color=EMPTY, capturing_move = -1):
        # loop over the w_board squares
        for square in range(len(w_board)):
            # init piece
            piece = w_board[square]

            # skip offw_board squares
            if piece == OFFBOARD: continue

            # if stone belongs to the given color
            if piece & color:
                # count w_liberties
                w_count(square, color)

                # if no w_liberties left remove the stones
                if len(w_liberties) == 0: w_clear_block(capturing_move)

                # restore the w_board
                w_restore_board()

    # edge detection
    def w_detect_edge(square):
        # loop over 4 directions
        for direction in [w_BOARD_RANGE, 1, -w_BOARD_RANGE, -1]:
            # indeed, it's the w_board edge
            if w_board[square + direction] == OFFBOARD: return 1

        # not, it's not the w_board edge
        return 0

    # find best liberty to extend/surround
    def w_evaluate(color):
        # max number of w_liberties found
        best_count = 0
        best_liberty = w_liberties[0]

        # loop over the w_liberties within the list
        for liberty in w_liberties:
            # put stone on w_board
            w_board[liberty] = color

            # count new w_liberties
            w_count(liberty, color)

            # found more w_liberties
            if len(w_liberties) > best_count and not detect_edge(liberty):
                best_liberty = liberty
                best_count = len(w_liberties)

            # restore w_board
            w_restore_board()

            # remove stone off w_board
            w_board[liberty] = EMPTY

        # return best liberty
        return best_liberty

    # generate move
    def w_genmove(color):
        global w_edge_colours, w_ko_spot, first_ai_move

        #return '' #NOTE: for passing testing
        #######################################################################
        #
        #    AI logic (first defense, then attack)
        #
        # 1. If opponent's group have only one liberty left
        #    then capture it
        #
        # 2. If the group of the side to move has only one liberty
        #    then save it by putting a stone there unless it's a w_board edge
        #
        # 3. If the group of the side to move has two w_liberties
        #    then choose the the one resulting in more w_liberties
        #
        # 4. If opponent's group have more than one liberty
        #    then try to surround it
        #
        # 5. Match patterns to build strong shape, if found any
        #    consider that instead of chasing the group
        #
        #######################################################################

        best_move = 0
        capture = 0
        save = 0
        defend = 0
        surround = 0
        pattern = 0

        while True:
            # capture opponent's group NOTE: added ko rule
            for square in range(len(w_board)):
                # init piece
                piece = w_board[square]

                # match opponent's group
                if piece & (3 - color):
                    # count w_liberties for opponent's group
                    w_count(square, (3 - color))

                    # if only 1 liberty left
                    if len(w_liberties) == 1:
                        target_square = w_liberties[0]
                        if (target_square != w_ko_spot):
                            # store the capture move
                            best_move = target_square
                            capture = target_square
                            break
                    # restore w_board
                    w_restore_board()
            if (best_move):
                w_restore_board()
                break

            # save own group
            for square in range(len(w_board)):
                # init piece
                piece = w_board[square]

                # match own group
                if piece & (color):
                    # count w_liberties for own group
                    w_count(square, (color))

                    # if only 1 liberty left
                    if len(w_liberties) == 1:
                        # store the save move
                        target_square = w_liberties[0]

                        # edge detection
                        if not w_detect_edge(target_square):
                            best_move = target_square
                            save = target_square
                            break

                    # restore w_board
                    w_restore_board()
            if (best_move):
                break

            # defend own group
            for square in range(len(w_board)):
                break # NOTE: skip for now, TODO: add liberties amount test instead?
                # init piece
                piece = w_board[square]

                # match own group
                if piece & (color):
                    # count w_liberties for own group
                    w_count(square, (color))

                    # if group has 2 liberties
                    if len(w_liberties) == 2:
                        # store the save move
                        best_liberty = w_evaluate(color)

                        ## if only one colour of surrounding stones, bad move: don't play
                        if (w_test_edge_colours(square)):
                            w_restore_board()
                            continue
                        best_move = best_liberty
                        defend = best_liberty
                        w_restore_board()
                        break

                    # restore w_board
                    w_restore_board()
            if (best_move):
                break

            # surround opponent's group
            for square in range(len(w_board)):
                break # NOTE: skip for now
                # init piece
                piece = w_board[square]

                # match opponent's group
                if piece & (3 - color):
                    # count liberties for own group
                    w_count(square, (3 - color))

                    # if group has more than 1 liberty
                    if len(w_liberties) > 1:
                        best_liberty = w_evaluate(3 - color)

                        ## if only one colour of surrounding stones, bad move: don't play
                        if (w_test_edge_colours(square)):
                            w_restore_board()
                            continue

                        best_move = best_liberty
                        surround = best_liberty

                        # try move
                        w_set_stone(best_move, color)
                        w_count(best_move, color)
                        legal = len(w_liberties)
                        w_restore_board()
                        w_board[best_move] = EMPTY
                        if not legal:
                            best_move = 0
                            continue
                        # else legal
                        break

                    # restore w_board
                    w_restore_board()
            if (best_move):
                break


            # pattern matching
            for square in range(len(w_board)):
                break # NOTE: skip for now
                # init piece
                piece = w_board[square]

                # skip offboard squares
                if piece == OFFBOARD: continue

                ## if only one colour of surrounding stones, bad move: don't play
                if (w_test_edge_colours(square)):
                    w_restore_board()
                    continue

                # pattern 1
                if piece & (3 - color):
                    target_one = square - w_BOARD_RANGE + 1
                    target_two = square - w_BOARD_RANGE - 1
                    if w_board[target_one] & color and w_board[target_two] & color:
                       best_move = square - w_BOARD_RANGE
                       pattern = best_move
                       break

                # pattern 2
                if piece & (3 - color):
                    target_one = square + 1
                    target_two = square - w_BOARD_RANGE - 1
                    if w_board[target_one] & color and w_board[target_two] & color:
                       best_move = square - w_BOARD_RANGE
                       pattern = best_move
                       break

                # pattern 3
                if piece & (3 - color):
                    target_one = square + 1
                    target_two = square - 1
                    if w_board[target_one] & color and w_board[target_two] & color:
                       best_move = square + w_BOARD_RANGE
                       pattern = best_move
                       break

                # pattern 4
                if piece & (3 - color):
                    target_one = square - w_BOARD_RANGE + 2
                    target_two = square - w_BOARD_RANGE - 1
                    if w_board[target_one] & color and w_board[target_two] & color:
                       best_move = square - w_BOARD_RANGE
                       pattern = best_move
                       break

                # pattern 5
                if piece & (3 - color):
                    target_one = square - w_BOARD_RANGE + 2
                    target_two = square - w_BOARD_RANGE - 2
                    if w_board[target_one] & color and w_board[target_two] & color:
                       best_move = square - w_BOARD_RANGE
                       pattern = best_move
                       break

                # pattern 6
                if piece & (3 - color):
                    target_one = square - 1
                    target_two = square + w_BOARD_RANGE - 2
                    if w_board[target_one] & color and w_board[target_two] & color:
                       best_move = square + w_BOARD_RANGE
                       pattern = best_move
                       break

                # pattern 7
                if piece & (3 - color):
                    target_one = square - w_BOARD_RANGE
                    target_two = square - w_BOARD_RANGE - 2
                    if w_board[target_one] & color and w_board[target_two] & color:
                       best_move = square - 1
                       pattern = best_move
                       break

            w_restore_board()
            break # exit while loop

        # found move
        if best_move:

            # randomize attack/defense actions
            random_action = random.randrange(2)

            # handle AI move priorities
            if not capture and not defend and not save: best_move = surround
            elif not capture and not save and defend: best_move = defend if random_action else surround
            elif not capture and not defend and save: best_move = save
            elif pattern: best_move = pattern
            if save: best_move = save
            if capture: best_move = capture

            # make move
            w_set_stone(best_move, color)
            # validate move
            w_count(best_move, color)
            # store w_liberties count
            legal = len(w_liberties)
            # restore w_board
            w_restore_board()
            # suicide move
            if not legal:
                # snap stone off the w_board
                w_board[best_move] = EMPTY
                #return ''
                ## consider random move instead #NOTE: removed to stop suicidal moves
                return w_make_random_move(color)

            # uncheck first move
            if (first_ai_move == True):
                first_ai_move = False

            return w_COORDS[best_move]

        # if starts with black
        return w_make_random_move(color)

    # GTP communcation protocol
    def w_gtp(command_str):
        if (True):
            # accept GUI command
            command = command_str
            ai_return = ""

            # handle commands
            if 'name' in command: print('= Wally\n')
            elif 'protocol_version' in command: print('= 1\n');
            elif 'version' in command: print('=', VERSION, '\n')
            elif 'list_commands' in command: print('= protocol_version\n')
            elif 'boardSize' in command: w_set_board_size(command); print('=\n')
            elif 'clear_board' in command: w_clear_board(); print('=\n')
            elif 'play' in command: w_play(command)
            elif 'genmove' in command: ai_return = w_genmove(BLACK if command.split()[-1] == 'B' else WHITE)
            elif 'quit' in command: pass #sys.exit()
            else: pass # skip unsupported commands

        return ai_return
