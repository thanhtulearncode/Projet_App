import React, { useState } from 'react';
import Rules from './Rules';

const Menu = ({ onStartGame }) => {
  const [showRules, setShowRules] = useState(false);
  const [showModeSelection, setShowModeSelection] = useState(false);
  const [showDifficultySelection, setShowDifficultySelection] = useState(false);
  const [showColorSelection, setShowColorSelection] = useState(false);
  const [selectedMode, setSelectedMode] = useState('local'); // Mode par défaut
  const [selectedDifficulty, setSelectedDifficulty] = useState('medium'); // Difficulté par défaut
  const [selectedColorPair, setSelectedColorPair] = useState('black-white'); // Couleurs par défaut

  const handlePlayClick = () => {
    // Lancer le jeu avec les paramètres actuellement sélectionnés
    onStartGame({
      mode: selectedMode,
      difficulty: selectedMode === 'ai' ? selectedDifficulty : null,
      colorPair: selectedColorPair
    });
  };

  const handleModeClick = () => {
    setShowModeSelection(true);
  };

  const handleColorClick = () => {
    setShowColorSelection(true);
  };

  const handleModeSelect = (mode) => {
    setSelectedMode(mode);
    if (mode === 'ai') {
      setShowModeSelection(false);
      setShowDifficultySelection(true);
    } else {
      setShowModeSelection(false);
    }
  };

  const handleDifficultySelect = (difficulty) => {
    setSelectedDifficulty(difficulty);
    setShowDifficultySelection(false);
  };

  const handleColorSelect = (colorPair) => {
    setSelectedColorPair(colorPair);
    setShowColorSelection(false);
  };

  // Fonction pour obtenir le nom convivial du mode
  const getModeName = () => {
    if (selectedMode === 'local') return 'Joueur vs Joueur';
    if (selectedMode === 'ai') {
      const difficultyText = selectedDifficulty === 'easy' ? 'Facile' : 
                            selectedDifficulty === 'medium' ? 'Moyen' : 'Difficile';
      return `Joueur vs IA (${difficultyText})`;
    }
    return 'Mode inconnu';
  };

  // Fonction pour obtenir le nom convivial des couleurs
  const getColorName = () => {
    switch (selectedColorPair) {
      case 'black-white': return 'Noir vs Blanc';
      case 'red-green': return 'Rouge vs Vert';
      case 'orange-blue': return 'Orange vs Bleu';
      default: return 'Couleurs inconnues';
    }
  };

  return (
    <div className="game-menu">
      <h1>Wall Street</h1>
      
      {!showModeSelection && !showDifficultySelection && !showColorSelection ? (
        // Menu principal avec 5 boutons
        <div className="menu-buttons">
          <button className="menu-button play-button" onClick={handlePlayClick}>
            JOUER
          </button>
          <button className="menu-button rules-button" onClick={() => setShowRules(true)}>
            RÈGLES
          </button>
          <button className="menu-button settings-button" onClick={() => alert('Paramètres à venir dans une future version')}>
            PARAMÈTRES
          </button>
          <button className="menu-button mode-button main-menu" onClick={handleModeClick}>
            MODE DE JEU: {getModeName()}
          </button>
          <button className="menu-button color-select-button" onClick={handleColorClick}>
            COULEURS: {getColorName()}
          </button>
        </div>
      ) : showModeSelection ? (
        // Menu de sélection du mode
        <div className="menu-buttons">
          <h2>Mode de jeu</h2>
          <button className="menu-button mode-button" onClick={() => handleModeSelect('local')}>
            JOUEUR VS JOUEUR
          </button>
          <button className="menu-button mode-button" onClick={() => handleModeSelect('ai')}>
            JOUEUR VS IA
          </button>
          <button className="menu-button back-button" onClick={() => setShowModeSelection(false)}>
            RETOUR
          </button>
        </div>
      ) : showDifficultySelection ? (
        // Menu de sélection de la difficulté
        <div className="menu-buttons">
          <h2>Difficulté</h2>
          <button className="menu-button difficulty-button easy" onClick={() => handleDifficultySelect('easy')}>
            FACILE
          </button>
          <button className="menu-button difficulty-button medium" onClick={() => handleDifficultySelect('medium')}>
            MOYEN
          </button>
          <button className="menu-button difficulty-button hard" onClick={() => handleDifficultySelect('hard')}>
            DIFFICILE
          </button>
          <button className="menu-button back-button" onClick={() => {
            setShowDifficultySelection(false);
            setShowModeSelection(true);
          }}>
            RETOUR
          </button>
        </div>
      ) : (
        // Menu de sélection des couleurs
        <div className="menu-buttons">
          <h2>Couleurs des pions</h2>
          <button className="menu-button color-button black-white" onClick={() => handleColorSelect('black-white')}>
            NOIR vs BLANC
          </button>
          <button className="menu-button color-button red-green" onClick={() => handleColorSelect('red-green')}>
            ROUGE vs VERT
          </button>
          <button className="menu-button color-button orange-blue" onClick={() => handleColorSelect('orange-blue')}>
            ORANGE vs BLEU
          </button>
          <button className="menu-button back-button" onClick={() => setShowColorSelection(false)}>
            RETOUR
          </button>
        </div>
      )}

      {showRules && <Rules onClose={() => setShowRules(false)} />}
    </div>
  );
};

export default Menu;