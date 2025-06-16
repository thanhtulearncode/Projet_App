import React from 'react';
import Cell from './Cell';

const Board = ({ board, selectedPiece, validMoves, onCellClick, playerColors }) => {
    return (
        <div className="board">
            {board.map((row, rowIndex) => (
                <div key={rowIndex} className="row">
                    {row.map((stack, colIndex) => {
                        const isSelected = selectedPiece?.row === rowIndex && selectedPiece?.col === colIndex;
                        const isValidMove = Array.isArray(validMoves) && validMoves.some(move => move[0] === rowIndex && move[1] === colIndex);
                        
                        return (
                            <Cell
                                key={colIndex}
                                stack={stack}
                                onClick={() => onCellClick(rowIndex, colIndex)}
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