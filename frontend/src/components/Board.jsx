import React from 'react';
import Cell from './Cell';

const Board = ({ 
  board, 
  selectedPiece, 
  selectedEPC,
  validMoves, 
  onCellClick, 
  playerColors,
  gamePhase,
  lastPawnPosition,
  lastMoveDest,
  lastEPCPosition,
  lastEPCDestination
}) => {
  return (
    <div className="board">
      {board.map((row, rowIndex) => (
        <div key={rowIndex} className="row">
          {row.map((stack, colIndex) => {
            // Déterminer si la cellule est sélectionnée
            let isSelected = false;
            if (gamePhase === 'move_pawn' && selectedPiece) {
              isSelected = selectedPiece.row === rowIndex && selectedPiece.col === colIndex;
            } else if (gamePhase === 'move_epc' && selectedEPC) {
              isSelected = selectedEPC.row === rowIndex && selectedEPC.col === colIndex;
            }
            
            // Déterminer si c'est un mouvement valide
            const isValidMove = validMoves.some(move => move[0] === rowIndex && move[1] === colIndex);
            
            // Déterminer si c'est la position d'origine du pion
            const isLastPawnPosition = lastPawnPosition && 
                                       lastPawnPosition.row === rowIndex && 
                                       lastPawnPosition.col === colIndex;
            
            const isLastPawnDestination = lastMoveDest &&
              lastMoveDest.row === rowIndex &&
              lastMoveDest.col === colIndex;

            // Déterminer si cette cellule doit animer la pièce
            const animateMove = lastMoveDest &&
              lastMoveDest.row === rowIndex &&
              lastMoveDest.col === colIndex;

            // Déterminer si c'est la position d'origine de l'EPC
            const isLastEPCPosition = lastEPCPosition &&  
              lastEPCPosition.row === rowIndex && 
              lastEPCPosition.col === colIndex;
            const isLastEPCDestination = lastEPCDestination &&
              lastEPCDestination.row === rowIndex &&
              lastEPCDestination.col === colIndex;
            return (
              <Cell
                key={colIndex}
                stack={stack}
                onClick={() => onCellClick(rowIndex, colIndex)}
                isSelected={isSelected}
                isValidMove={isValidMove}
                playerColors={playerColors}
                gamePhase={gamePhase}
                isLastPawnPosition={isLastPawnPosition}
                isLastPawnDestination={isLastPawnDestination}
                isLastEPCPosition={isLastEPCPosition}
                isLastEPCDestination={isLastEPCDestination}
                animateMove={animateMove}
              />
            );
          })}
        </div>
      ))}
    </div>
  );
};

export default Board;