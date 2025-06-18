import React, { useState } from 'react';
import Rules from './Rules';
//import './Menu.css'; // Assurez-vous d'avoir le fichier CSS pour les styles

const COLOR_CHOICES = [
  { name: 'Red', value: 'red' },
  { name: 'Green', value: 'green' },
  { name: 'Blue', value: 'blue' },
  { name: 'Yellow', value: 'yellow' },
  { name: 'Orange', value: 'orange' },
  { name: 'Purple', value: 'purple' },
  { name: 'Pink', value: 'pink' },
  { name: 'Brown', value: 'brown' },
  { name: 'Black', value: 'black' },
  { name: 'White', value: 'white' },
  { name: 'Gray', value: 'gray' },
  { name: 'Cyan', value: 'cyan' },
  { name: 'Magenta', value: 'magenta' },
  { name: 'Lime', value: 'lime' },
  { name: 'Navy', value: 'navy' }
];

function Stars({ count = 80 }) {
  const stars = Array.from({ length: count }).map((_, i) => {
    const style = {
      left: `${Math.random() * 100}vw`,
      top: `${Math.random() * 100}vh`,
      width: `${Math.random() * 2 + 1}px`,
      height: `${Math.random() * 2 + 1}px`,
      animationDelay: `${Math.random() * 2}s`
    };
    return <div className="star" style={style} key={i} />;
  });
  return <div className="stars">{stars}</div>;
}

const Menu = ({ onStartGame }) => {
  const [showRules, setShowRules] = useState(false);
  const [showModeSelection, setShowModeSelection] = useState(false);
  const [showDifficultySelection, setShowDifficultySelection] = useState(false);
  const [showColorSelection, setShowColorSelection] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const [selectedMode, setSelectedMode] = useState('local'); // Mode par défaut
  const [selectedDifficulty, setSelectedDifficulty] = useState('medium'); // Difficulté par défaut
  const [selectedColorPair, setSelectedColorPair] = useState('black-white'); // Couleurs par défaut
  const [customColorPairs, setCustomColorPairs] = useState([]);
  const [color1, setColor1] = useState('red');
  const [color2, setColor2] = useState('green');

  const handlePlayClick = () => {
    // Lancer le jeu avec les paramètres actuellement sélectionnés
    onStartGame({
      mode: selectedMode,
      difficulty: selectedMode === 'ai' ? selectedDifficulty : null,
      colorPair: selectedColorPair,
      customColorPairs: customColorPairs
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
      onStartGame({
        mode: 'local',
        difficulty: null,
        colorPair: selectedColorPair,
        customColorPairs: customColorPairs
      });
    }
  };

  const handleDifficultySelect = (difficulty) => {
    setSelectedDifficulty(difficulty);
    setShowDifficultySelection(false);
    // Lance la partie contre l'IA avec la difficulté choisie
    onStartGame({
      mode: 'ai',
      difficulty: difficulty,
      colorPair: selectedColorPair,
      customColorPairs: customColorPairs
    });
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
      default:
        if (selectedColorPair.startsWith('custom-')) {
          const idx = parseInt(selectedColorPair.split('-')[1], 10);
          const pair = customColorPairs[idx];
          if (pair) {
            const n1 = COLOR_CHOICES.find(c=>c.value===pair.color1)?.name || pair.color1;
            const n2 = COLOR_CHOICES.find(c=>c.value===pair.color2)?.name || pair.color2;
            return `${n1} vs ${n2}`;
          }
        }
        return 'Couleurs inconnues';
    }
  };

  return (
    <>
      <div className="animated-bg">
        <Stars count={80} />
      </div>
      <div className="game-menu">
        <div className="menu-glass">
          <h1>Wall Street</h1>
          {!showModeSelection && !showDifficultySelection && !showColorSelection && !showSettings ? (
            <div className="menu-buttons">
              <button className="menu-button play-button" onClick={handlePlayClick}>
                <i className="fas fa-play-circle"></i> JOUER
              </button>
              <button className="menu-button rules-button" onClick={() => setShowRules(true)}>
                <i className="fas fa-book"></i> RÈGLES
              </button>
              <button className="menu-button settings-button" onClick={() => setShowSettings(true)}>
                <i className="fas fa-cog"></i> PARAMÈTRES
              </button>
              <button className="menu-button mode-button main-menu" onClick={handleModeClick}>
                <i className="fas fa-gamepad"></i> MODE DE JEU: {getModeName()}
              </button>
              <button className="menu-button color-select-button" onClick={handleColorClick}>
                <i className="fas fa-palette"></i> COULEURS: {getColorName()}
              </button>
            </div>
          ) : showModeSelection ? (
            <div className="menu-buttons">
              <h2>Mode de jeu</h2>
              <button className="menu-button mode-button" onClick={() => handleModeSelect('local')}>
                <i className="fas fa-users"></i> JOUEUR VS JOUEUR
              </button>
              <button className="menu-button mode-button" onClick={() => handleModeSelect('ai')}>
                <i className="fas fa-robot"></i> JOUEUR VS IA
              </button>
              <button className="menu-button back-button" onClick={() => setShowModeSelection(false)}>
                <i className="fas fa-arrow-left"></i> RETOUR
              </button>
            </div>
          ) : showDifficultySelection ? (
            <div className="menu-buttons">
              <h2>Difficulté</h2>
              <button className="menu-button difficulty-button easy" onClick={() => handleDifficultySelect('easy')}>
                <i className="fas fa-leaf"></i> FACILE
              </button>
              <button className="menu-button difficulty-button medium" onClick={() => handleDifficultySelect('medium')}>
                <i className="fas fa-bolt"></i> MOYEN
              </button>
              <button className="menu-button difficulty-button hard" onClick={() => handleDifficultySelect('hard')}>
                <i className="fas fa-fire"></i> DIFFICILE
              </button>
              <button className="menu-button back-button" onClick={() => {
                setShowDifficultySelection(false);
                setShowModeSelection(true);
              }}>
                <i className="fas fa-arrow-left"></i> RETOUR
              </button>
            </div>
          ) : showSettings ? (
            <div className="rules-modal">
              <div className="rules-content">
                <h2>Créer une paire de couleurs</h2>
                <div style={{ display: 'flex', flexDirection: 'column', gap: '18px', alignItems: 'center' }}>
                  <div style={{ display: 'flex', gap: '18px', alignItems: 'center' }}>
                    <label>Joueur 1:
                      <select value={color1} onChange={e => setColor1(e.target.value)} style={{ marginLeft: 8 }}>
                        {COLOR_CHOICES.map(opt => (
                          <option key={opt.value} value={opt.value}>{opt.name}</option>
                        ))}
                      </select>
                    </label>
                    <label>Joueur 2:
                      <select value={color2} onChange={e => setColor2(e.target.value)} style={{ marginLeft: 8 }}>
                        {COLOR_CHOICES.map(opt => (
                          <option key={opt.value} value={opt.value}>{opt.name}</option>
                        ))}
                      </select>
                    </label>
                  </div>
                  <button className="menu-button play-button" style={{ width: 'auto', padding: '8px 24px' }}
                    onClick={() => {
                      if (color1 !== color2) {
                        setCustomColorPairs([...customColorPairs, { color1, color2 }]);
                        setShowSettings(false);
                      }
                    }}>
                    Ajouter la paire
                  </button>
                  <button className="close-rules-button" onClick={() => setShowSettings(false)}>Fermer</button>
                </div>
              </div>
            </div>
          ) : showColorSelection ? (
            <div className="menu-buttons">
              <h2>Couleurs des pions</h2>
              <button className="menu-button color-button black-white" onClick={() => handleColorSelect('black-white')}>
                <i className="fas fa-chess"></i> NOIR vs BLANC
              </button>
              <button className="menu-button color-button red-green" onClick={() => handleColorSelect('red-green')}>
                <i className="fas fa-chess"></i> ROUGE vs VERT
              </button>
              <button className="menu-button color-button orange-blue" onClick={() => handleColorSelect('orange-blue')}>
                <i className="fas fa-chess"></i> ORANGE vs BLEU
              </button>
              {customColorPairs.map((pair, idx) => (
                <button
                  key={idx}
                  className="menu-button color-button"
                  style={{
                    background: `linear-gradient(to right, ${pair.color1} 50%, ${pair.color2} 50%)`,
                    color: '#fff',
                    border: '2px solid #999',
                    textShadow: '1px 1px 2px rgba(0,0,0,0.8)'
                  }}
                  onClick={() => handleColorSelect(`custom-${idx}`)}
                >
                  <i className="fas fa-chess"></i> {COLOR_CHOICES.find(c=>c.value===pair.color1)?.name || pair.color1} vs {COLOR_CHOICES.find(c=>c.value===pair.color2)?.name || pair.color2}
                </button>
              ))}
              <button className="menu-button back-button" onClick={() => setShowColorSelection(false)}>
                <i className="fas fa-arrow-left"></i> RETOUR
              </button>
            </div>
          ) : null}
          {showRules && <Rules onClose={() => setShowRules(false)} />}
        </div>
      </div>
    </>
  );
};

export default Menu;