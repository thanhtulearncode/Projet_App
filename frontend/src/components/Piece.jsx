import React from 'react';

const Piece = ({ type, color, stackIndex, stackHeight }) => {
    // Style différent pour les pièces carrées et rondes
    const getStyle = () => {
        const baseStyle = {
            width: '38px',
            height: '38px',
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
                case 'yellow':
                    background = 'radial-gradient(circle at 30% 30%, #fff700 60%, #bbaa00 100%)';
                    borderColor = '#bbaa00';
                    shadow = '0 2px 8px #bbaa00aa';
                    break;
                case 'purple':
                    background = 'radial-gradient(circle at 30% 30%, #c299fc 60%, #6c3483 100%)';
                    borderColor = '#6c3483';
                    shadow = '0 2px 8px #6c3483aa';
                    break;
                case 'pink':
                    background = 'radial-gradient(circle at 30% 30%, #ffb6c1 60%, #e75480 100%)';
                    borderColor = '#e75480';
                    shadow = '0 2px 8px #e75480aa';
                    break;
                case 'brown':
                    background = 'radial-gradient(circle at 30% 30%, #bc8f8f 60%, #6e2c00 100%)';
                    borderColor = '#6e2c00';
                    shadow = '0 2px 8px #6e2c00aa';
                    break;
                case 'gray':
                    background = 'radial-gradient(circle at 30% 30%, #e0e0e0 60%, #888 100%)';
                    borderColor = '#888';
                    shadow = '0 2px 8px #8888';
                    break;
                case 'cyan':
                    background = 'radial-gradient(circle at 30% 30%, #a7fffa 60%, #00bcd4 100%)';
                    borderColor = '#00bcd4';
                    shadow = '0 2px 8px #00bcd4aa';
                    break;
                case 'magenta':
                    background = 'radial-gradient(circle at 30% 30%, #ffb3ff 60%, #c71585 100%)';
                    borderColor = '#c71585';
                    shadow = '0 2px 8px #c71585aa';
                    break;
                case 'lime':
                    background = 'radial-gradient(circle at 30% 30%, #eaffd0 60%, #32cd32 100%)';
                    borderColor = '#32cd32';
                    shadow = '0 2px 8px #32cd32aa';
                    break;
                case 'navy':
                    background = 'radial-gradient(circle at 30% 30%, #b0c4de 60%, #001f3f 100%)';
                    borderColor = '#001f3f';
                    shadow = '0 2px 8px #001f3faa';
                    break;
                default:
                    background = color;
                    borderColor = color;
                    shadow = '0 2px 8px #8888';
            }
            return {
                ...baseStyle,
                borderRadius: '50%',
                background,
                border: `2.5px solid ${borderColor}`,
                boxShadow: shadow,
                transform: 'scale(0.85)',
            };
        }
        return baseStyle;
    };

    return (
        <div style={getStyle()} />
    );
};

export default Piece;