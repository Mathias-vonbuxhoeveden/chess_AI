from flask import Flask, send_from_directory, request
from flask import jsonify
from flask_cors import CORS, cross_origin
import json
import chess
import keras
import random
import numpy as np
from model import predict_pro_move




app=Flask(__name__,static_folder='client/build',static_url_path='')
cors = CORS(app)

@app.route("/members", methods = ['POST'])
@cross_origin()



def members():
    try:
        data = request.json
        chess_board = chess.Board(data)
        from_square, to_square = predict_pro_move().predict(chess_board)
        move = chess.Move(from_square=from_square, to_square=to_square)
        computer_move = {"from": move.uci()[0:2], "to": move.uci()[2:]}
        return jsonify(computer_move)
    except:
        return jsonify("c5")


@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == "__main__":
    app.run(debug=True)
