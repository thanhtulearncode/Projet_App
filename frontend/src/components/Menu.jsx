import React, { useState, useEffect } from 'react';
import Rules from './Rules';
import ColorSelector from './ColorSelector';
import './Menu.css';

function Menu({ onStartGame }) {
  const [showRules, setShowRules] = useState(false);
  const [showModeSelection, setShowModeSelection] = useState(false);
  const [showDifficultySelection, setShowDifficultySelection] = useState(false);
  const [showColorSelection, setShowColorSelection] = useState(false);
  const [showSettings, setShowSettings] = useState(false);
  const [selectedMode, setSelectedMode] = useState('local');
  const [selectedDifficulty, setSelectedDifficulty] = useState('medium');
  const [selectedColorPair, setSelectedColorPair] = useState('black-white');
  const [customColorPairs, setCustomColorPairs] = useState([]);
  const [animateTitle, setAnimateTitle] = useState(false);
  const [showBoard, setShowBoard] = useState(false);

  // Animation d'entrée
  useEffect(() => {
    setTimeout(() => setAnimateTitle(true), 300);
    setTimeout(() => setShowBoard(true), 800);
  }, []);

  const handlePlayClick = () => {
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

  const getModeName = () => {
    if (selectedMode === 'local') return 'Joueur vs Joueur';
    if (selectedMode === 'ai') {
      const difficultyText = selectedDifficulty === 'easy' ? 'Facile' : 
                           selectedDifficulty === 'medium' ? 'Moyen' : 'Difficile';
      return `Joueur vs IA (${difficultyText})`;
    }
    return 'Mode inconnu';
  };

  const getColorName = () => {
    switch (selectedColorPair) {
      case 'black-white': return 'Noir vs Blanc';
      case 'red-green': return 'Rouge vs Vert';
      case 'orange-blue': return 'Orange vs Bleu';
      default: return 'Couleurs personnalisées';
    }
  };

  // Plateau animé en arrière-plan
  const renderBoardBackground = () => {
    return (
      <div className={`board-background ${showBoard ? 'visible' : ''}`}>
        <div className="board-grid">
          {Array(64).fill().map((_, index) => {
            const row = Math.floor(index / 8);
            const col = index % 8;
            const isDark = (row + col) % 2 === 1;
            const hasPiece = (row < 3 || row > 4) && isDark;
            const pieceColor = row < 3 ? 'piece-dark' : row > 4 ? 'piece-light' : '';
            const delay = Math.random() * 0.5;
            
            return (
              <div 
                key={index} 
                className={`board-cell ${isDark ? 'dark' : 'light'}`}
                style={{animationDelay: `${delay}s`}}
              >
                {hasPiece && <div className={`board-piece ${pieceColor}`}></div>}
                {(row === 3 || row === 4) && Math.random() > 0.7 && (
                  <div className="board-stack" style={{height: `${Math.floor(Math.random() * 4 + 1) * 20}%`}}></div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    );
  };

  return (
    <div className="menu-container">
      {renderBoardBackground()}
      
      <div className="logo-section">
        <div className={`game-logo ${animateTitle ? 'visible' : ''}`}>
          <div className="logo-icon">
            <div className="logo-building"></div>
            <div className="logo-building"></div>
            <div className="logo-building"></div>
          </div>
          <h1 className="game-title">WALL STREET</h1>
          <div className="logo-tagline">Le jeu de stratégie financière</div>
        </div>
      </div>
      
      <div className={`menu-content ${animateTitle ? 'visible' : ''}`}>
        {!showModeSelection && !showDifficultySelection && !showColorSelection && !showSettings ? (
          <div className="main-menu">
            <button className="menu-button play-button" onClick={handlePlayClick}>
              <i className="fas fa-play-circle"></i>
              <span>JOUER</span>
            </button>
            
            <div className="menu-group">
              <button className="menu-button mode-button" onClick={handleModeClick}>
                <i className="fas fa-gamepad"></i>
                <span>MODE</span>
                <div className="button-value">{getModeName()}</div>
              </button>
              
              <button className="menu-button color-button" onClick={handleColorClick}>
                <i className="fas fa-palette"></i>
                <span>COULEURS</span>
                <div className="button-value">{getColorName()}</div>
              </button>
            </div>
            
            <div className="menu-group">
              <button className="menu-button rules-button" onClick={() => setShowRules(true)}>
                <i className="fas fa-book"></i>
                <span>RÈGLES</span>
              </button>
              
              <button className="menu-button settings-button" onClick={() => setShowSettings(true)}>
                <i className="fas fa-cog"></i>
                <span>OPTIONS</span>
              </button>
            </div>
          </div>
        ) : showModeSelection ? (
          <div className="submenu mode-selection">
            <h2>Mode de jeu</h2>
            <div className="selection-options">
              <div 
                className={`selection-card ${selectedMode === 'local' ? 'selected' : ''}`}
                onClick={() => handleModeSelect('local')}
              >
                <div className="card-icon">
                  <i className="fas fa-users"></i>
                </div>
                <div className="card-content">
                  <h3>Joueur vs Joueur</h3>
                  <p>Affrontez un ami en local sur le même appareil</p>
                </div>
              </div>
              
              <div 
                className={`selection-card ${selectedMode === 'ai' ? 'selected' : ''}`}
                onClick={() => handleModeSelect('ai')}
              >
                <div className="card-icon">
                  <i className="fas fa-robot"></i>
                </div>
                <div className="card-content">
                  <h3>Joueur vs IA</h3>
                  <p>Défiez l'intelligence artificielle</p>
                </div>
              </div>
            </div>
            
            <button className="back-button" onClick={() => setShowModeSelection(false)}>
              <i className="fas fa-arrow-left"></i> Retour
            </button>
          </div>
        ) : showDifficultySelection ? (
          <div className="submenu difficulty-selection">
            <h2>Niveau de difficulté</h2>
            <div className="selection-options">
              <div 
                className={`selection-card ${selectedDifficulty === 'easy' ? 'selected' : ''}`}
                onClick={() => handleDifficultySelect('easy')}
              >
                <div className="card-icon easy">
                  <i className="fas fa-child"></i>
                </div>
                <div className="card-content">
                  <h3>Facile</h3>
                  <p>Pour les débutants ou parties détendues</p>
                </div>
              </div>
              
              <div 
                className={`selection-card ${selectedDifficulty === 'medium' ? 'selected' : ''}`}
                onClick={() => handleDifficultySelect('medium')}
              >
                <div className="card-icon medium">
                  <i className="fas fa-user"></i>
                </div>
                <div className="card-content">
                  <h3>Moyen</h3>
                  <p>Pour les joueurs réguliers</p>
                </div>
              </div>
              
              <div 
                className={`selection-card ${selectedDifficulty === 'hard' ? 'selected' : ''}`}
                onClick={() => handleDifficultySelect('hard')}
              >
                <div className="card-icon hard">
                  <i className="fas fa-chess-king"></i>
                </div>
                <div className="card-content">
                  <h3>Difficile</h3>
                  <p>Pour les joueurs expérimentés</p>
                </div>
              </div>
            </div>
            
            <button className="back-button" onClick={() => {
              setShowDifficultySelection(false);
              setShowModeSelection(true);
            }}>
              <i className="fas fa-arrow-left"></i> Retour
            </button>
          </div>
        ) : showColorSelection ? (
          <ColorSelector 
            onSelect={(colorPair, customData) => {
              if (customData) {
                setCustomColorPairs([...customColorPairs, customData]);
              }
              handleColorSelect(colorPair);
            }}
            onBack={() => setShowColorSelection(false)}
            defaultPair={selectedColorPair}
            customPairs={customColorPairs}
          />
        ) : showSettings ? (
          <div className="submenu settings-menu">
            <h2>Options</h2>
            <div className="settings-options">
              <div className="settings-group">
                <h3>Son</h3>
                <div className="settings-controls">
                  <label>
                    <span>Musique</span>
                    <input type="range" min="0" max="100" defaultValue="70" />
                  </label>
                  <label>
                    <span>Effets sonores</span>
                    <input type="range" min="0" max="100" defaultValue="80" />
                  </label>
                </div>
              </div>
              
              <div className="settings-group">
                <h3>Interface</h3>
                <div className="settings-controls">
                  <label>
                    <input type="checkbox" defaultChecked />
                    <span>Animations</span>
                  </label>
                  <label>
                    <input type="checkbox" defaultChecked />
                    <span>Indices de jeu</span>
                  </label>
                </div>
              </div>
            </div>
            
            <button className="back-button" onClick={() => setShowSettings(false)}>
              <i className="fas fa-arrow-left"></i> Retour
            </button>
          </div>
        ) : null}
      </div>
      
      {showRules && <Rules onClose={() => setShowRules(false)} />}
      
      <div className="menu-footer">
        <div className="copyright">© 2025 Wall Street Game</div>
        <div className="version">v1.0.0</div>
      </div>
    </div>
  );
}

export default Menu;