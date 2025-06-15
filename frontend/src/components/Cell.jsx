import React from 'react';
import Piece from './Piece';

const Cell = ({ stack, onClick, isSelected, isValidMove }) => {
    return (
        <div 
            className={`cell ${isSelected ? 'selected' : ''} ${isValidMove ? 'valid-move' : ''}`}
            onClick={onClick}
            style={{
                position: 'relative',
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                width: '50px',
                height: '50px',
            }}
        >
            {/* Affiche toutes les pièces de la pile avec positionnement relatif */}
            {stack.map((piece, index) => (
                <div 
                    key={index} 
                    style={{
                        position: 'absolute',
                        zIndex: index, // Pièces du dessous ont zIndex plus bas
                        transform: `translate(0, ${-index * 2}px)`, // Décalage vertical pour l'effet d'empilement
                    }}
                >
                    <Piece 
                        type={piece.type} 
                        color={piece.color} 
                        height={piece.height}
                        stackIndex={index}
                        stackHeight={stack.length}
                    />
                </div>
            ))}
            
            {stack.filter(piece => piece.type === 'square').length > 0 && (
                <span className="stack-badge">
                    {stack.filter(piece => piece.type === 'square').length}
                </span>
            )}
        </div>
    );
};

export default Cell;