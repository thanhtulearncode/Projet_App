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
        
        // Style pour les pions ronds - Support de toutes les couleurs
        if (type === 'round') {
            let backgroundColor;
            let borderColor;
            
            // Déterminer la couleur de fond selon la couleur du pion
            switch (color) {
                case 'black':
                    backgroundColor = '#000000';
                    borderColor = '#444444';
                    break;
                case 'white':
                    backgroundColor = '#FFFFFF';
                    borderColor = '#999999';
                    break;
                case 'red':
                    backgroundColor = '#C0392B';
                    borderColor = '#922B21';
                    break;
                case 'green':
                    backgroundColor = '#27AE60';
                    borderColor = '#1E8449';
                    break;
                case 'orange':
                    backgroundColor = '#E67E22';
                    borderColor = '#BA4A00';
                    break;
                case 'blue':
                    backgroundColor = '#2980B9';
                    borderColor = '#1F618D';
                    break;
                default:
                    backgroundColor = '#FFFFFF';
                    borderColor = '#999999';
            }
            
            return {
                ...baseStyle,
                borderRadius: '50%',
                backgroundColor: backgroundColor,
                border: `2px solid ${borderColor}`,
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