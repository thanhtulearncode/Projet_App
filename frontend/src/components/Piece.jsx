import React from 'react';

const Piece = ({ type, color, stackIndex, stackHeight, isFullscreen }) => {
    // Style différent pour les pièces carrées et rondes
    const getStyle = () => {
        // Calculer la taille en fonction du mode d'affichage
        const baseSize = isFullscreen ? '60px' : '38px';
        
        const baseStyle = {
            width: baseSize,
            height: baseSize,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: '0 2px 8px rgba(0,0,0,0.25)',
            margin: 'auto',
            transition: 'box-shadow 0.2s, transform 0.2s',
        };

        if (type === 'square') {
            return {
                ...baseStyle,
                borderRadius: '8px',
                background: 'linear-gradient(145deg, #e0c097 60%, #b58863 100%)',
                border: '2px solid #8b4513',
                boxShadow: '0 2px 8px #8b4513aa, 0 1px 0 #fff8 inset',
            };
        }
        
        if (type === 'round') {
            let background, borderColor, shadow;
            switch (color) {
                case 'black':
                    background = 'radial-gradient(circle at 30% 30%, #444 60%, #000 100%)';
                    borderColor = '#222';
                    shadow = '0 2px 8px #000a';
                    break;
                case 'white':
                    background = 'radial-gradient(circle at 30% 30%, #fff 70%, #ccc 100%)';
                    borderColor = '#bbb';
                    shadow = '0 2px 8px #8888';
                    break;
                case 'red':
                    background = 'radial-gradient(circle at 30% 30%, #ff6b6b 60%, #b22222 100%)';
                    borderColor = '#922B21';
                    shadow = '0 2px 8px #b22222aa';
                    break;
                case 'green':
                    background = 'radial-gradient(circle at 30% 30%, #7fff7f 60%, #228B22 100%)';
                    borderColor = '#1E8449';
                    shadow = '0 2px 8px #228B22aa';
                    break;
                case 'orange':
                    background = 'radial-gradient(circle at 30% 30%, #ffd580 60%, #e67e22 100%)';
                    borderColor = '#BA4A00';
                    shadow = '0 2px 8px #e67e22aa';
                    break;
                case 'blue':
                    background = 'radial-gradient(circle at 30% 30%, #85caff 60%, #2980b9 100%)';
                    borderColor = '#1F618D';
                    shadow = '0 2px 8px #2980b9aa';
                    break;
                default:
                    background = '#fff';
                    borderColor = '#999';
                    shadow = '0 2px 8px #8888';
            }
            return {
                ...baseStyle,
                borderRadius: '50%',
                background,
                border: `2.5px solid ${borderColor}`,
                boxShadow: shadow,
                transform: isFullscreen ? 'scale(0.9)' : 'scale(0.85)',
            };
        }
        return baseStyle;
    };

    return (
        <div style={getStyle()} />
    );
};

export default Piece;