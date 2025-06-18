import React from 'react';
import Piece from './Piece';

const mapType = (type) => {
    if (type === 'Square') return 'square';
    if (type === 'Pawn') return 'round';
    return type;
};

const Cell = ({ 
    stack, 
    onClick, 
    isSelected, 
    isValidMove, 
    playerColors, 
    gamePhase, 
    isLastPawnPosition,
    isLastPawnDestination, 
    isLastEPCPosition,
    isLastEPCDestination,
    animateMove 
}) => {
    // Construire la classe CSS avec toutes les conditions
    let cellClassName = 'cell';
    
    if (isSelected) {
        cellClassName += ' selected';
    } 
    
    if (isValidMove) {
        cellClassName += ' valid-move';
    }
    
    // Ajouter la classe pour la phase EPC
    if (gamePhase === 'move_epc') {
        cellClassName += ' epc-phase';
    }
    
    // Ajouter la classe pour la position d'origine du pion
    if (isLastPawnPosition) {
        cellClassName += ' last-pawn-position';
    }

    if (isLastPawnDestination) {
        cellClassName += ' last-pawn-destination';
    }

    if (isLastEPCPosition) {
        cellClassName += ' last-pawn-postition';
    }

    if (isLastEPCDestination) {
        cellClassName += ' last-pawn-destination';   
    }

    return (
        <div 
            className={cellClassName}
            onClick={onClick}
            style={{
                position: 'relative',
                display: 'flex',
                justifyContent: 'center',
                alignItems: 'center',
                width: '64px',
                height: '64px',
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
                    <div className={animateMove && index === stack.length - 1 ? "piece-animate-move" : ""}>
                        <Piece 
                            type={mapType(piece.type)} 
                            color={piece.color} 
                            height={piece.height}
                            stackIndex={index}
                            stackHeight={stack.length}
                        />
                    </div>
                </div>
            ))}
            
            {/* Badge de hauteur de pile carrée */}
            {stack.filter(piece => mapType(piece.type) === 'square').length > 0 && (
                <span className="stack-badge">
                    {stack.filter(piece => mapType(piece.type) === 'square').length}
                </span>
            )}
            
            {/* Indicateur visuel pour la position d'origine du pion */}
            {isLastPawnPosition && gamePhase === 'move_epc' && (
                <div className="last-pawn-indicator">
                    Position précédente
                </div>
            )}
        </div>
    );
};

export default Cell;