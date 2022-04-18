from flask import Flask, request
from flask import jsonify

app=Flask(__name__)

@app.route("/members", methods = ['GET', 'POST'])
def members():
    if request.method == 'POST':
        data = request.json
        pawn_moves = []
        for move in data:
            if len(move) < 3:
                pawn_moves.append(move)

    else:
        pass
    return jsonify("c5")


if __name__ == "__main__":

    app.run(debug=True)
