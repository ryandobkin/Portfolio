# Author: Ryan Dobkin
# GitHub Username: ryandobkin
# Date: 8/17/23
# Description: Initializes and tracks the movements of an altered version of Chess.


class ChessVar:
    """
    Handles an instance of an altered version of chess.
    """
    def __init__(self):
        self._piece_list = []
        self._board_grid = []
        self._current_turn = 'white'
        self._gs = 'UNFINISHED'
        self._placeholder = self.initialize()

    def initialize(self):
        """
        Initializes an instance of the chess board by creating ChessPiece objects that represent actual board
        pieces and adding them to the self._piece_list list. Returns True.
        """
        self._piece_list.append(ChessPiece('king', 'white', 'a1'))
        self._piece_list.append(ChessPiece('rook', 'white', 'a2'))
        self._piece_list.append(ChessPiece('bishop', 'white', 'b1'))
        self._piece_list.append(ChessPiece('bishop', 'white', 'b2'))
        self._piece_list.append(ChessPiece('knight', 'white', 'c1'))
        self._piece_list.append(ChessPiece('knight', 'white', 'c2'))

        self._piece_list.append(ChessPiece('king', 'black', 'h1'))
        self._piece_list.append(ChessPiece('rook', 'black', 'h2'))
        self._piece_list.append(ChessPiece('bishop', 'black', 'g1'))
        self._piece_list.append(ChessPiece('bishop', 'black', 'g2'))
        self._piece_list.append(ChessPiece('knight', 'black', 'f1'))
        self._piece_list.append(ChessPiece('knight', 'black', 'f2'))
        return True

    def get_game_state(self):
        """
        Checks if either king has reached row 8. Returns unfinished if checked on white turn. If black turn,
        checks if either or both pieces is in the win state and returns the appropriate win status.
        """
        win_row = ['a8', 'b8', 'c8', 'd8', 'e8', 'f8', 'g8', 'h8']
        w_won = 0
        b_won = 0
        if self._current_turn == 'white' and self._gs == 'UNFINISHED':
            return 'UNFINISHED'
        for x in self._piece_list:
            if x.get_type() == 'king':
                if x.get_location() in win_row:
                    if x.get_color() == 'white':
                        w_won = 1
                    elif x.get_color() == 'black':
                        b_won = 1
        if w_won == 1 and b_won == 1:
            print('TIE')
            self._gs = 'TIE'
            return 'TIE'
        elif w_won == 1 and b_won == 0:
            print('WHITE_WON')
            self._gs = 'TIE'
            return 'WHITE_WON'
        elif w_won == 0 and b_won == 1:
            print('BLACK_WON')
            self._gs = 'BLACK_WON'
            return 'BLACK_WON'
        else:
            self._gs = 'UNFINISHED'
            return 'UNFINISHED'

    def in_check(self, chess_piece, move_to):
        """
        Takes as a parameter a passed chess_piece object and the location that it is set to move to.
        Returns True (in check, therefore invalid move) if:
        1. If the move_to location is the opponents king
        2. If the move_to location sets up a check for the opposite color
        3. If the move_to location sets up a check for the current color
        4. If moving king, checks if any opposing colors pieces have a valid and legal move to move_to location
        """
        opp_king = None
        curr_king = None
        temp_cords = chess_piece.get_location()
        if self._current_turn == 'white':
            opp_turn = 'black'
        else:
            opp_turn = 'white'

        for x in self._piece_list:
            if x.get_type() == 'king' and x.get_color() == opp_turn:
                opp_king = x
                continue
        for x in self._piece_list:
            if x.get_type() == 'king' and x.get_color() == self._current_turn:
                curr_king = x
                continue
        if move_to == opp_king.get_location():
            # checks if the desired move_to is the opponents king
            return True
        else:
            legal_check_a = self.check_if_legal(self._current_turn, move_to, opp_king.get_location(), chess_piece)
            # checks if it's a legal move for my piece, after being moved to an open spot, to put opp_turn in check
            if legal_check_a is True:
                return True

            # checks to see if, after moving the piece, opp_king piece will be in check
            for current_piece in self._piece_list:
                if current_piece.get_color() == self._current_turn:
                    legal = self.check_if_legal(self._current_turn, current_piece.get_location(),
                                                opp_king.get_location(),  current_piece)
                    chess_piece.set_location(move_to)
                    legal_2 = self.check_if_legal(self._current_turn, current_piece.get_location(),
                                                opp_king.get_location(), current_piece)
                    chess_piece.set_location(temp_cords)
                    if legal is True or legal_2 is True:
                        return True

            # checks to see if, after moving the piece, curr_king piece will be in check
            for current_piece in self._piece_list:
                if current_piece.get_color() == opp_turn:
                    legal = self.check_if_legal(opp_turn, current_piece.get_location(),
                                                curr_king.get_location(), current_piece)
                    chess_piece.set_location(move_to)
                    legal_2 = self.check_if_legal(opp_turn, current_piece.get_location(),
                                                  curr_king.get_location(), current_piece)
                    chess_piece.set_location(temp_cords)
                    if legal is True or legal_2 is True:
                        return True
        return False

    def make_move(self, to_move, move_to):
        """
        Takes as a parameter the piece to move location and the piece move to location.
        Checks if the move is legal(check_if_legal())[which calls piece_mover()], moving into check(in_check()),
        if needs to 'eat' piece(piece_eater()), and updates game state(get_game_state()) and color(update_color()).
        Returns True if the move was successful, otherwise returns False.
        """
        for chess_piece in self._piece_list:
            if chess_piece.get_location() == to_move:
                legal = self.check_if_legal(self._current_turn, to_move, move_to, chess_piece)
                check = self.in_check(chess_piece, move_to)
                if legal is True and check is False:
                    self.piece_eater(move_to)
                    chess_piece.set_location(str(move_to))
                    if self.get_game_state() == 'UNFINISHED':
                        self.update_color()
                        return True
                    else:
                        self.update_color()
                        return False
        self.update_color()
        return False

    def update_color(self):
        """Takes no parameters. Is called when the turn is to be changed. Gets the current value of the private
        class data member self._current_turn and changes it to the opposite color of current."""
        if self._current_turn == 'white':
            self._current_turn = 'black'
        else:
            self._current_turn = 'white'

    def piece_mover(self, to_move, move_to, chess_piece):
        """
        Takes as a parameter the location of the piece to be moved and the intended final movement location, as well
        as the piece to be moved.
        If the move is valid, sets the location of the object to the new location and returns true.
        Checks if the location has line of sight with the piece to be moved. Does not apply to king and knight.
        Checks if the piece can move in a valid way for the given to_move and move_to locations.
        """
        x_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        y_list = ['1', '2', '3', '4', '5', '6', '7', '8']
        e1 = move_to[0]
        e2 = move_to[1]
        j1 = to_move[0]
        j2 = to_move[1]
        xe_token = -1
        ye_token = -1
        xj_token = -1
        yj_token = -1

        for x in x_list:
            xe_token += 1
            if e1 == x:
                break
        for y in y_list:
            ye_token += 1
            if e2 == y:
                break

        for x in x_list:
            xj_token += 1
            if j1 == x:
                break
        for y in y_list:
            yj_token += 1
            if j2 == y:
                break

        # ROOK LOS
        r_los = 0
        for x in range(8):
            if r_los is True or r_los is False:
                break

            if xj_token > xe_token:
                if xj_token-x >= 0:
                    for _ in self._piece_list:
                        if _.get_location()[1] == y_list[yj_token]:
                            if _.get_location()[0] == x_list[xj_token - x] and x != 0:
                                r_los = False
                                break
                    if x_list[xe_token] == x_list[xj_token-x]:
                        r_los = True
                        break

            elif xj_token < xe_token:
                if xj_token+x < 8:
                    for _ in self._piece_list:
                        if _.get_location()[1] == y_list[yj_token]:
                            if _.get_location()[0] == x_list[xj_token + x] and x != 0:
                                r_los = False
                                break
                    if x_list[xe_token] == x_list[xj_token+x]:
                        r_los = True
                        break

            elif yj_token > ye_token:
                if yj_token-x >= 0:
                    for _ in self._piece_list:
                        if _.get_location()[0] == x_list[xj_token]:
                            if _.get_location()[1] == y_list[yj_token - x] and x != 0:
                                r_los = False
                                break
                    if y_list[ye_token] == y_list[yj_token-x]:
                        r_los = True
                        break

            elif yj_token < ye_token:
                if yj_token+x < 8:
                    for _ in self._piece_list:
                        if _.get_location()[0] == x_list[xj_token]:
                            if _.get_location()[1] == y_list[yj_token + x] and x != 0:
                                r_los = False
                                break
                    if y_list[ye_token] == y_list[yj_token+x]:
                        r_los = True
                        break

        #BISHOP LOS
        b_los = 0
        for x in range(8):
            if b_los is True or b_los is False:
                break

            if xe_token > xj_token and ye_token > yj_token:
                # +x +y
                if xj_token + x < 8 and yj_token + x < 8:
                    for _ in self._piece_list:
                        if _.get_location() == x_list[xj_token+x] + y_list[yj_token+x] and x != 0:
                            b_los = False
                            break
                    if x_list[xe_token] == x_list[xj_token+x] and y_list[ye_token] == y_list[yj_token+x]:
                        b_los = True
                        break

            elif xe_token > xj_token and ye_token < yj_token:
                # +x -y
                if xj_token + x < 8 and yj_token - x >= 0:
                    for _ in self._piece_list:
                        if _.get_location() == x_list[xj_token + x] + y_list[yj_token - x] and x != 0:
                            b_los = False
                            break
                    if x_list[xe_token] == x_list[xj_token + x] and y_list[ye_token] == y_list[yj_token - x]:
                        b_los = True
                        break

            elif xe_token < xj_token and ye_token > yj_token:
                # -x +y
                if xj_token - x >= 0 and yj_token + x < 8:
                    for _ in self._piece_list:
                        if _.get_location() == x_list[xj_token - x] + y_list[yj_token + x] and x != 0:
                            b_los = False
                            break
                    if x_list[xe_token] == x_list[xj_token - x] and y_list[ye_token] == y_list[yj_token + x]:
                        b_los = True
                        break

            elif xe_token < xj_token and ye_token < yj_token:
                # -x -y
                if xj_token - x >= 0 and yj_token - x >= 0:
                    for _ in self._piece_list:
                        if _.get_location() == x_list[xj_token - x] + y_list[yj_token - x] and x != 0:
                            b_los = False
                            break
                    if x_list[xe_token] == x_list[xj_token - x] and y_list[ye_token] == y_list[yj_token - x]:
                        b_los = True
                        break

        if chess_piece.get_type() == 'king':
            if xj_token - 1 >= 0:
                if e1 == x_list[xj_token - 1]:
                    if e2 == y_list[yj_token]:
                        return True
                    if yj_token - 1 >= 0:
                        if e2 == y_list[yj_token - 1]:
                            return True
                    if yj_token + 1 < 8:
                        if e2 == y_list[yj_token + 1]:
                            return True
            if xj_token + 1 < 8:
                if e1 == x_list[xj_token + 1]:
                    if e2 == y_list[yj_token]:
                        return True
                    if yj_token - 1 >= 0:
                        if e2 == y_list[yj_token - 1]:
                            return True
                    if yj_token + 1 < 8:
                        if e2 == y_list[yj_token + 1]:
                            return True
            if xj_token == xe_token:
                if e2 == y_list[yj_token]:
                    return True
                if yj_token - 1 >= 0:
                    if e2 == y_list[yj_token - 1]:
                        return True
                if yj_token + 1 < 8:
                    if e2 == y_list[yj_token + 1]:
                        return True
            else:
                return False

        if chess_piece.get_type() == 'rook':
            if (e1 == j1 and e2 != j2) or (e1 != j1 and e2 == j2):
                if r_los is True:
                    return True
            return False

        if chess_piece.get_type() == 'bishop':
            for x in range(8):
                if x + xj_token < 8 and x + yj_token < 8:
                    if e1 == x_list[xj_token + x] and e2 == y_list[yj_token + x]:
                        if b_los is True:
                            return True
                if xj_token - x >= 0 and yj_token - x >= 0:
                    if e1 == x_list[xj_token - x] and e2 == y_list[yj_token - x]:
                        if b_los is True:
                            return True
                if xj_token + x < 8 and yj_token - x >= 0:
                    if e1 == x_list[xj_token + x] and e2 == y_list[yj_token - x]:
                        if b_los is True:
                            return True
                if xj_token - x >= 0 and yj_token + x < 8:
                    if e1 == x_list[xj_token - x] and e2 == y_list[yj_token + x]:
                        if b_los is True:
                            return True
            return False

        if chess_piece.get_type() == 'knight':
            if xj_token + 2 < 8:
                if x_list[xj_token + 2] == x_list[xe_token]:
                    if y_list[yj_token + 1] == y_list[ye_token] and yj_token + 1 < 8:
                        return True
                    if y_list[yj_token - 1] == y_list[ye_token] and yj_token - 1 >= 0:
                        return True
            if xj_token - 2 >= 0:
                if x_list[xj_token - 2] == x_list[xe_token] and xj_token - 2 >= 0:
                    if y_list[yj_token + 1] == y_list[ye_token] and yj_token + 1 < 8:
                        return True
                    if y_list[yj_token - 1] == y_list[ye_token] and yj_token - 1 >= 0:
                        return True

            if yj_token + 2 < 8:
                if y_list[yj_token + 2] == y_list[ye_token] and yj_token + 2 < 8:
                    if x_list[xj_token + 1] == x_list[xe_token] and xj_token + 1 < 8:
                        return True
                    if x_list[xj_token - 1] == x_list[xe_token] and xj_token - 1 >= 0:
                        return True
            if yj_token - 2 >= 0:
                if y_list[yj_token - 2] == y_list[ye_token] and yj_token - 2 < 8:
                    if x_list[xj_token + 1] == x_list[xe_token] and xj_token + 1 < 8:
                        return True
                    if x_list[yj_token - 1] == x_list[xe_token] and xj_token - 1 >= 0:
                        return True
        return False

    def piece_eater(self, move_to):
        for x in self._piece_list:
            if x.get_location() == move_to:
                self._piece_list.remove(x)
                return True
        return False

    def check_if_legal(self, color, to_move, move_to, chess_piece):
        """
        Checks to see if the move is legal by checking if move is:
        1. Intended for a piece of the same color as self._current_turn
        2. to_move is a valid piece on the board
        3. If moving to the location of another of self._current_turn's pieces
        4. In the bounds of the board
        5. self.piece_mover() returns True
        """
        x_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        y_list = ['1', '2', '3', '4', '5', '6', '7', '8']
        e1 = move_to[0]
        e2 = move_to[1]

        if color != chess_piece.get_color():
            return False
        elif e1 not in x_list:
            return False
        elif e2 not in y_list:
            return False
        else:
            return self.piece_mover(to_move, move_to, chess_piece)

    def print_text_board(self):
        """
        Creates a printable text version of the board. Using sub-method get_iden(), updates the board every time
        this method is called.
        """

        def get_iden(cords, color, p_type):
            """
            Takes the location, color, and type of piece in the active piece list to be iterated through as parameters.
            Edits the grid created in print_text_board, sets the 'locations' to the piece identifiers.
            Char[0] w means white piece, b means black. Char[1] k = king, r = rook, n = knight, b = bishop.
            '[]' is an empty space.
            """
            piece_color = 'a'
            piece_type = 'a'
            col = -1
            row = -1
            new_cords = cords.strip('\"')

            if new_cords[0] == 'a':
                col = 0
            elif new_cords[0] == 'b':
                col = 1
            elif new_cords[0] == 'c':
                col = 2
            elif new_cords[0] == 'd':
                col = 3
            elif new_cords[0] == 'e':
                col = 4
            elif new_cords[0] == 'f':
                col = 5
            elif new_cords[0] == 'g':
                col = 6
            elif new_cords[0] == 'h':
                col = 7
            else:
                col = -1

            if new_cords[1] == '1':
                row = 7
            elif new_cords[1] == '2':
                row = 6
            elif new_cords[1] == '3':
                row = 5
            elif new_cords[1] == '4':
                row = 4
            elif new_cords[1] == '5':
                row = 3
            elif new_cords[1] == '6':
                row = 2
            elif new_cords[1] == '7':
                row = 1
            elif new_cords[1] == '8':
                row = 0
            else:
                row = -1

            if color == 'white':
                piece_color = 'w'
            elif color == 'black':
                piece_color = 'b'

            if p_type == 'king':
                piece_type = 'k'
            elif p_type == 'rook':
                piece_type = 'r'
            elif p_type == 'bishop':
                piece_type = 'b'
            elif p_type == 'knight':
                piece_type = 'n'

            piece_name = (piece_color + piece_type)
            self._board_grid[row][col] = piece_name
            return

        self._board_grid = [['[]']*8 for _ in range(8)]

        for x in self._piece_list:
            get_iden(x.get_location(), x.get_color(), x.get_type())

        for _ in self._board_grid:
            print(_)


class ChessPiece:
    """
    Acts as an object representation of a chess piece. Holds piece type, color, and location.
    """
    def __init__(self, piece_type, color, location):
        self._type = piece_type
        self._color = color
        self._cords = location

    def get_type(self):
        """
        Returns the type of piece. Can be 'king', 'rook', 'bishop', or 'knight'.
        """
        return self._type

    def get_color(self):
        """
        Returns color of piece. Either 'white', or 'black'.
        """
        return self._color

    def get_location(self):
        """
        Returns the location of the given chess piece in algebraic chess notation (c6, d2, etc.).
        """
        return self._cords

    def set_location(self, new_cords):
        """
        Takes a location as a parameter. Sets the location of a chess piece object to the passed location.
        """
        self._cords = new_cords


def game_state():
    """
    Acts as a console input-based player for the game. Automatically run when __name__ == '__main__'.
    """
    my_game = ChessVar()
    my_game.print_text_board()
    print("Move by entering algebraic notation i.e. b2, c3")
    while my_game.get_game_state() == 'UNFINISHED':
        print("WHITE_TURN:")
        move_input = input()
        if my_game.make_move((move_input[0] + move_input[1]), (move_input[4] + move_input[5])) is False:
            print("ILLEGAL")
        my_game.print_text_board()
        print("BLACK_TURN:")
        move_input = input()
        if my_game.make_move((move_input[0] + move_input[1]), (move_input[4] + move_input[5])) is False:
            print("ILLEGAL")
        my_game.print_text_board()


def main():
    try:
        game_state()
    except KeyboardInterrupt:
        print("Program Interrupted")


if __name__ == '__main__':
    main()

