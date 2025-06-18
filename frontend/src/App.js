import React, { useState } from 'react';
import Game from './components/Game';
import Menu from './components/Menu';
import backgroundImage from './images/wallstreet_background.jpg';

function App() {
  const [showMenu, setShowMenu] = useState(true);
  const [gameSettings, setGameSettings] = useState({ mode: null, difficulty: null });

  const appStyle = {
    backgroundImage: `url(${backgroundImage})`,
    backgroundSize: 'cover',
    backgroundPosition: 'center',
    backgroundRepeat: 'no-repeat',
    minHeight: '100vh',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    flexDirection: 'column' 
  };

  const handleStartGame = (settings) => {
    setGameSettings(settings);
    setShowMenu(false);
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
    <div className="App" style={appStyle}>
      {showMenu ? (
        <Menu onStartGame={handleStartGame} />
      ) : (
        <div className="game-container" style={{ textAlign: 'center' }}>
          <div className="game-mode-indicator" style={{ marginBottom: '10px', fontWeight: 'bold', color: '#fff' }}>
            Mode: {getGameModeText()}
          </div>
          <button 
            className="back-to-menu-button"
            onClick={() => setShowMenu(true)}
            style={{ marginBottom: '20px', padding: '10px 20px' }}
          >
            Retour au menu
          </button>
          <Game settings={gameSettings} />
        </div>
      )}
    </div>
  );
}

export default App;
