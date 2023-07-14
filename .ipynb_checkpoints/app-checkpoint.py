from flask import Flask, send_from_directory, request, jsonify
from flask_cors import CORS, cross_origin
from chess import square_mirror, Board, Move
from keras.models import load_model 
import numpy as np


class predict_pro_move:
    
    """
    Class for predicting professional chess-player move
    """

    def __init__(self):
        self.move_to_network = load_model("move_to_network.h5")
        self.piece_selector_network = load_model("piece_selector_network.h5")

    def encode_board_data(self, board):

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
        X = X.reshape(1,8,8,6)
        return X


    def predict(self, board):
        if board.turn == True:
            board_input = board.copy()
        else:
            board_input = board.mirror()
        X = self.encode_board_data(board_input)
        piece_selector_prob = list(np.squeeze(self.piece_selector_network.predict(X)))
        move_to_probs = list(np.squeeze(self.move_to_network.predict(X)))
        legal_moves = list(board_input.legal_moves)
        from_square = legal_moves[0].from_square

        for move in legal_moves:
            if piece_selector_prob[move.from_square] > piece_selector_prob[from_square]:
                from_square = move.from_square

        legal_to_moves = []
        for move in legal_moves:
            if move.from_square == from_square:
                legal_to_moves.append(move.to_square)

        to_square = legal_to_moves[0]
        for move in legal_to_moves:
            if move_to_probs[move] > move_to_probs[to_square]:
                to_square = move

        if board.turn == True:
            return from_square, to_square
        else:
            return square_mirror(from_square), square_mirror(to_square)

def load_models():

    global model
    model = predict_pro_move()


app=Flask(__name__,static_folder='client/build',static_url_path='')
load_models()
cors = CORS(app)
@app.route("/members", methods = ['POST'])
@cross_origin()




def members():
    try:
        data = request.json
        chess_board = Board(data)
        from_square, to_square = model.predict(chess_board)
        move = Move(from_square=from_square, to_square=to_square)
        computer_move = {"from": move.uci()[0:2], "to": move.uci()[2:]}
        return jsonify(computer_move)
    except:
        return jsonify("c5")


@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == "__main__":
    app.run(debug=True)
