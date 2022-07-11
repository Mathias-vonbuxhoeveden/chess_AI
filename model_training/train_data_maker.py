import os
import chess.pgn
import numpy as np


def encode_board_data(board):

    """
    Function takes a board as input and returns an 8x8x6 array encoding of the board-position.
    """
    rock_positions = np.zeros(64)
    knight_positions = np.zeros(64)
    bishop_positions = np.zeros(64)
    queen_positions = np.zeros(64)
    king_positions = np.zeros(64)
    pawn_positions = np.zeros(64)

    for i in range(64):

        try:

            if board.piece_at(i).symbol() == 'R':
                rock_positions[i] = 1
            elif board.piece_at(i).symbol() == 'r':
                rock_positions[i] = -1
            elif board.piece_at(i).symbol() == 'N':
                knight_positions[i] = 1
            elif board.piece_at(i).symbol() == 'n':
                knight_positions[i] = -1
            elif board.piece_at(i).symbol() == 'B':
                bishop_positions[i] = 1
            elif board.piece_at(i).symbol() == 'b':
                bishop_positions[i] = -1
            elif board.piece_at(i).symbol() == 'Q':
                queen_positions[i] = 1
            elif board.piece_at(i).symbol() == 'q':
                queen_positions[i] = -1
            elif board.piece_at(i).symbol() == 'K':
                king_positions[i] = 1
            elif board.piece_at(i).symbol() == 'k':
                king_positions[i] = -1
            elif board.piece_at(i).symbol() == 'P':
                pawn_positions[i] = 1
            elif board.piece_at(i).symbol() == 'p':
                pawn_positions[i] = -1
        except:

            pass

    rock_positions = rock_positions.reshape(8,8)
    knight_positions = knight_positions.reshape(8,8)
    bishop_positions = bishop_positions.reshape(8,8)
    queen_positions = queen_positions.reshape(8,8)
    king_positions = king_positions.reshape(8,8)
    pawn_positions = pawn_positions.reshape(8,8)

    X = np.dstack([rock_positions,knight_positions,bishop_positions,queen_positions,king_positions,pawn_positions])

    return X


def fetch_from_square(from_square):

    """
    Function takes as input a chess.Move object and returns a one-hot-encoded array represeting the square that
    the piece moved from.
    """

    moved_from = np.zeros(64)
    moved_from[from_square] = 1

    return moved_from

def fetch_to_square(to_square):

    """
    Function takes as input a chess.Move object and returns a one-hot-encoded array represeting the square that
    the piece moved to.
    """

    moved_to = np.zeros(64)
    moved_to[to_square] = 1

    return moved_to

def main():

    print("Starting process!")
    X, y_move_from, y_move_to = [], [], []
    pgn = open(os.path.join("data", "ficsgamesdb_search_255906.pgn"))
    while True:
        game = chess.pgn.read_game(pgn)
        if game is None:
            break
        board = game.board()
        for move in game.mainline_moves():
            if board.turn == True:
                X.append(encode_board_data(board))
                y_move_from.append(fetch_from_square(move.from_square))
                y_move_to.append(fetch_to_square(move.to_square))
                board.push(move)
            else:
                X.append(encode_board_data(board.mirror()))
                y_move_from.append(fetch_from_square(chess.square_mirror(move.from_square)))
                y_move_to.append(fetch_to_square(chess.square_mirror(move.to_square)))
                board.push(move)
        print(f"Currently parsed {len(X)} examples")

    return X, y_move_from, y_move_to

if __name__ == "__main__":


 X, y_move_from, y_move_to = main()
 np.savez("data/dataset.npz", X, y_move_from, y_move_to)
