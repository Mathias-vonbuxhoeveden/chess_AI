from flask import Flask, request
from flask import jsonify
import json
import chess
import random


app=Flask(__name__,static_folder='client/build',static_url_path='')

@app.route("/members", methods = ['POST'])
def members():
    try:
        data = request.json
        chess_board = chess.Board(data)
        legal_moves = list(chess_board.legal_moves)
        move = random.choice(legal_moves)
        from_square = move.uci()[0:2]
        to_square_square = move.uci()[2:]
        computer_move = {"from": from_square, "to": to_square_square}
        return jsonify(computer_move)
    except:
        return jsonify("c5")


if __name__ == "__main__":

    app.run(debug=True)
