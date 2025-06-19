import React from 'react';

const Piece = ({ type, color, stackIndex, stackHeight, isFullscreen, playerColors }) => {
    // Map color to custom color if needed
    let trueColor = color;
    if (playerColors) {
        if (color === 'white' || color === 'player1') {
            trueColor = playerColors.player1;
        } else if (color === 'black' || color === 'player2') {
            trueColor = playerColors.player2;
        }
    }
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
            switch (trueColor) {
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
                case 'gold':
                    background = 'radial-gradient(circle at 30% 30%, #ffe066 60%, #bfa100 100%)';
                    borderColor = '#bfa100';
                    shadow = '0 2px 8px #bfa100aa';
                    break;
                case 'blue':
                    background = 'radial-gradient(circle at 30% 30%, #85caff 60%, #2980b9 100%)';
                    borderColor = '#1F618D';
                    shadow = '0 2px 8px #2980b9aa';
                    break;
                case 'brown':
                    background = 'radial-gradient(circle at 30% 30%, #bc8f6f 60%, #795548 100%)';
                    borderColor = '#795548';
                    shadow = '0 2px 8px #795548aa';
                    break;
                case 'cream':
                    background = 'radial-gradient(circle at 30% 30%, #fffdd0 60%, #f5eed6 100%)';
                    borderColor = '#f5eed6';
                    shadow = '0 2px 8px #f5eed6aa';
                    break;
                case 'navy':
                    background = 'radial-gradient(circle at 30% 30%, #5a7bb7 60%, #001f3f 100%)';
                    borderColor = '#001f3f';
                    shadow = '0 2px 8px #001f3faa';
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
                case 'purple':
                    background = 'radial-gradient(circle at 30% 30%, #d1aaff 60%, #8e44ad 100%)';
                    borderColor = '#8e44ad';
                    shadow = '0 2px 8px #8e44adaa';
                    break;
                case 'cyan':
                    background = 'radial-gradient(circle at 30% 30%, #a7ffff 60%, #00bcd4 100%)';
                    borderColor = '#00bcd4';
                    shadow = '0 2px 8px #00bcd4aa';
                    break;
                case 'coral':
                    background = 'radial-gradient(circle at 30% 30%, #ffbfa3 60%, #ff7f50 100%)';
                    borderColor = '#ff7f50';
                    shadow = '0 2px 8px #ff7f50aa';
                    break;
                default:
                    background = trueColor;
                    borderColor = trueColor;
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