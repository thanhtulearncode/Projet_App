import React from 'react';

const Piece = ({ type, color, stackIndex, stackHeight }) => {
    // Style différent pour les pièces carrées et rondes
    const getStyle = () => {
        const baseStyle = {
            width: '40px',
            height: '40px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: '0 2px 4px rgba(0,0,0,0.2)',
        };

        // Style pour les pièces carrées (fond)
        if (type === 'square') {
            return {
                ...baseStyle,
                borderRadius: '4px',
                backgroundColor: color || '#b58863',
                border: '1px solid #8b4513',
            };
        }
        
        // Style pour les pions ronds
        if (type === 'round') {
            return {
                ...baseStyle,
                borderRadius: '50%',
                backgroundColor: color === 'black' ? '#000' : '#fff',
                border: `2px solid ${color === 'black' ? '#444' : '#999'}`,
                transform: 'scale(0.8)', // Réduire légèrement la taille du pion
            };
        }
        
        return baseStyle;
    };

    return (
        <div style={getStyle()}>
        </div>
    );
};

export default Piece;