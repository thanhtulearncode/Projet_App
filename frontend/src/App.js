import React, { useState, useEffect } from 'react';
import Game from './components/Game';
import Menu from './components/Menu';
import './App.css';

function App() {
  const [showMenu, setShowMenu] = useState(true);
  const [gameSettings, setGameSettings] = useState({ mode: null, difficulty: null });
  const [isLoading, setIsLoading] = useState(false);
  const [transition, setTransition] = useState(false);

  // Effet de transition entre les écrans
  useEffect(() => {
    if (transition) {
      const timer = setTimeout(() => {
        setShowMenu(!showMenu);
        setTransition(false);
      }, 500);
      return () => clearTimeout(timer);
    }
  }, [transition, showMenu]);

  const handleStartGame = (settings) => {
    setIsLoading(true);
    setGameSettings(settings);
    setTransition(true);
    
    setTimeout(() => {
      setIsLoading(false);
    }, 1000);
  };

  const handleBackToMenu = () => {
    setTransition(true);
  };

  const getGameModeText = () => {
    if (gameSettings.mode === 'local') {
      return 'Joueur vs Joueur';
    } else if (gameSettings.mode === 'ai') {
      const difficultyText = {
        easy: 'Facile',
        medium: 'Moyen',
        hard: 'Difficile'
      }[gameSettings.difficulty];

      return `Joueur vs IA (${difficultyText})`;
    }
    return '';
  };

  return (
    <div className={`app-container ${transition ? 'transitioning' : ''}`}>
      {isLoading && (
        <div className="loading-screen">
          <div className="spinner"></div>
          <div className="loading-text">Chargement...</div>
        </div>
      )}
      
      {showMenu ? (
        <div className={`menu-view ${transition ? 'fade-out' : 'fade-in'}`}>
          <Menu onStartGame={handleStartGame} />
        </div>
      ) : (
        <div className={`game-view ${transition ? 'fade-out' : 'fade-in'}`}>
          <button className="back-to-menu" onClick={handleBackToMenu}>
            <i className="fas fa-arrow-left"></i> Menu
          </button>
          <div className="game-mode-indicator" style={{ marginBottom: '10px', fontWeight: 'bold', color: '#fff' }}>
            Mode: {getGameModeText()}
          </div>
          <Game settings={gameSettings} />
        </div>
      )}
      
      <div className="app-background"></div>
    </div>
  );
}

export default App;
