
import { useState, useEffect } from 'react';
import { Chessboard } from 'react-chessboard';
import { Chess } from 'chess.js';
function App() {
  const [game, setGame] = useState(new Chess());


// perform modify function on game state
  function safeGameMutate(modify) {
    setGame((g) => {
      const update = { ...g };
      modify(update);
      return update;
    });
  }


function makeRandomMove() {

   fetch('/members')
  .then((response) => response.json())
  .then((actualData) => {
    safeGameMutate((game) => {
         game.move(actualData);
       });


  })


 }

// perform action when piece dropped by user
  function onDrop(sourceSquare, targetSquare) {
    // attempt move
    let move = null;
    safeGameMutate((game) => {
      move = game.move({
        from: sourceSquare,
        to: targetSquare,
        promotion: 'q'
      });
    });

    // illegal move made
    if (move === null) return false;
    // valid move made, make computer move
    setTimeout(makeRandomMove, 200);
    return true;
    console.log(game)
  }
  return <Chessboard position={game.fen()} onPieceDrop={onDrop} />;
}
export default App;
