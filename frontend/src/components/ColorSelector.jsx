import React, { useState, useEffect } from 'react';
import './ColorSelector.css';

const ColorSelector = ({ onSelect, onBack, defaultPair, customPairs = [] }) => {
  const [selectedOption, setSelectedOption] = useState(defaultPair || 'black-white');
  const [animateColors, setAnimateColors] = useState(false);
  const [previewActive, setPreviewActive] = useState(false);
  const [previewColors, setPreviewColors] = useState({first: 'black', second: 'white'});
  
  useEffect(() => {
    // Animation d'entrée
    setTimeout(() => setAnimateColors(true), 200);
  }, []);

  // Présets de couleurs avec descriptions et images de preview
  const colorPresets = [
    {
      id: 'black-white',
      name: 'Classique',
      description: 'Le jeu traditionnel',
      colors: ['black', 'white'],
      icon: 'chess-pawn'
    },
    {
      id: 'red-green',
      name: 'Contrasté',
      description: 'Rouge vs Vert',
      colors: ['#C0392B', '#27AE60'],
      icon: 'fire'
    },
    {
      id: 'gold-blue',
      name: 'Luxueux',
      description: 'Or vs Bleu',
      colors: ['#F39C12', '#2980B9'],
      icon: 'crown'
    },
    {
      id: 'purple-cyan',
      name: 'Moderne',
      description: 'Violet vs Cyan',
      colors: ['#8E44AD', '#00BCD4'],
      icon: 'bolt'
    },
    {
      id: 'brown-cream',
      name: 'Vintage',
      description: 'Brun vs Crème',
      colors: ['#795548', '#F5EED6'],
      icon: 'scroll'
    },
    {
      id: 'navy-coral',
      name: 'Océanique',
      description: 'Marine vs Corail',
      colors: ['#34495E', '#FF7F50'],
      icon: 'water'
    }
  ];

  const handlePresetClick = (preset) => {
    setSelectedOption(preset.id);
    setPreviewActive(true);
    setPreviewColors({first: preset.colors[0], second: preset.colors[1]});
  };

  const handleConfirm = () => {
    onSelect(selectedOption);
  };

  // Rendu de l'échiquier de prévisualisation
  const renderBoardPreview = () => {
    const rows = 8;
    const cols = 8;
    const cells = [];

    for (let i = 0; i < rows; i++) {
      for (let j = 0; j < cols; j++) {
        const isDark = (i + j) % 2 === 1;
        const hasPiece = i < 3 || i > 4;
        const pieceColor = i < 3 ? previewColors.first : i > 4 ? previewColors.second : null;
        
        if (hasPiece && isDark) {
          cells.push(
            <div 
              key={`${i}-${j}`} 
              className={`preview-cell ${isDark ? 'dark' : 'light'}`}
              style={{
                gridRow: i + 1,
                gridColumn: j + 1,
              }}
            >
              {pieceColor && (
                <div 
                  className="preview-piece" 
                  style={{backgroundColor: pieceColor}}
                ></div>
              )}
            </div>
          );
        } else {
          cells.push(
            <div 
              key={`${i}-${j}`} 
              className={`preview-cell ${isDark ? 'dark' : 'light'}`}
              style={{
                gridRow: i + 1,
                gridColumn: j + 1,
              }}
            ></div>
          );
        }
      }
    }

    return cells;
  };

  const selectedPreset = colorPresets.find(p => p.id === selectedOption) || colorPresets[0];

  return (
    <div className="color-selector">
      <h2>Sélection des Couleurs</h2>
      
      <div className={`color-preview-container ${previewActive ? 'active' : ''}`}>
        <div className="board-preview">
          {renderBoardPreview()}
        </div>
        
        <div className="selected-colors">
          <div className="color-badge" style={{backgroundColor: previewColors.first}}>
            Joueur 1
          </div>
          <div className="versus">VS</div>
          <div className="color-badge" style={{backgroundColor: previewColors.second}}>
            Joueur 2
          </div>
        </div>
      </div>
      
      <div className={`color-presets ${animateColors ? 'animate' : ''}`}>
        {colorPresets.map((preset, index) => (
          <div 
            key={preset.id}
            className={`color-preset ${selectedOption === preset.id ? 'selected' : ''}`}
            onClick={() => handlePresetClick(preset)}
            style={{animationDelay: `${index * 0.1}s`}}
          >
            <div className="preset-icon">
              <i className={`fas fa-${preset.icon}`}></i>
            </div>
            <div className="preset-colors">
              <div className="preset-color" style={{backgroundColor: preset.colors[0]}}></div>
              <div className="preset-color" style={{backgroundColor: preset.colors[1]}}></div>
            </div>
            <div className="preset-info">
              <h3>{preset.name}</h3>
              <p>{preset.description}</p>
            </div>
          </div>
        ))}
        
        {customPairs.map((pair, index) => (
          <div 
            key={`custom-${index}`}
            className={`color-preset ${selectedOption === `custom-${index}` ? 'selected' : ''}`}
            onClick={() => {
              setSelectedOption(`custom-${index}`);
              setPreviewActive(true);
              setPreviewColors({first: pair.color1, second: pair.color2});
            }}
            style={{animationDelay: `${(colorPresets.length + index) * 0.1}s`}}
          >
            <div className="preset-icon">
              <i className="fas fa-palette"></i>
            </div>
            <div className="preset-colors">
              <div className="preset-color" style={{backgroundColor: pair.color1}}></div>
              <div className="preset-color" style={{backgroundColor: pair.color2}}></div>
            </div>
            <div className="preset-info">
              <h3>Personnalisé {index + 1}</h3>
              <p>Vos couleurs</p>
            </div>
          </div>
        ))}
      </div>
      
      <div className="color-selector-actions">
        <button className="back-button" onClick={onBack}>
          <i className="fas fa-arrow-left"></i> Retour
        </button>
        <button className="confirm-button" onClick={handleConfirm}>
          Confirmer <i className="fas fa-check"></i>
        </button>
      </div>
    </div>
  );
};

export default ColorSelector;