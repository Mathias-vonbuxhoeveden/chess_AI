from flask import Flask, send_from_directory, request
from flask import jsonify
from flask_cors import CORS, cross_origin
import json
import chess
import random


app=Flask(__name__,static_folder='client/build',static_url_path='')
cors = CORS(app)

@app.route("/members", methods = ['POST'])
@cross_origin()
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

@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == "__main__":

    app.run(debug=True)
