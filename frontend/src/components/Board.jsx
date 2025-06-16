import React from 'react';
import Cell from './Cell';

const Board = ({ board, selectedPiece, validMoves, onSelectPiece, onMove, playerColors }) => {
    const handleCellClick = (row, col) => {
        // Si une pièce est déjà sélectionnée et que la case cliquée est un mouvement valide
        if (selectedPiece && validMoves.some(move => move[0] === row && move[1] === col)) {
            onMove(row, col);
        } else {
            // Sinon, on essaie de sélectionner une pièce
            onSelectPiece(row, col);
        }
    };

    return (
        <div className="board">
            {board.map((row, rowIndex) => (
                <div key={rowIndex} className="row">
                    {row.map((stack, colIndex) => {
                        const isSelected = selectedPiece?.row === rowIndex && selectedPiece?.col === colIndex;
                        const isValidMove = validMoves.some(move => move[0] === rowIndex && move[1] === colIndex);
                        
                        return (
                            <Cell
                                key={colIndex}
                                stack={stack}
                                onClick={() => handleCellClick(rowIndex, colIndex)}
                                isSelected={isSelected}
                                isValidMove={isValidMove}
                                playerColors={playerColors}
                            />
                        );
                    })}
                </div>
            ))}
        </div>
    );
};

export default Board;