import React from 'react';
import Cell from './Cell'; 

const Board = ({ board, selectedPiece, validMoves, onSelectPiece, onMove }) => {
    return (
        <div className="board">
            {board.map((row, rowIndex) => (
                <div key={rowIndex} className="row">
                    {row.map((stack, colIndex) => {
                        const isSelected = selectedPiece?.row === rowIndex && selectedPiece?.col === colIndex;
                        const isValidMove = validMoves.some(move => move[0] === rowIndex && move[1] === colIndex);
                        
                        return (
                            <Cell
                                key={`${rowIndex}-${colIndex}`}
                                stack={stack}
                                isSelected={isSelected}
                                isValidMove={isValidMove}
                                onClick={() => {
                                    if (isValidMove) {
                                        onMove(rowIndex, colIndex);
                                    } else {
                                        onSelectPiece(rowIndex, colIndex);
                                    }
                                }}
                            />
                        );
                    })}
                </div>
            ))}
        </div>
    );
};

export default Board;