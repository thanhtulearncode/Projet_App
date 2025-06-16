import React, { useState } from 'react';
import Game from './components/Game';
import Menu from './components/Menu';
import backgroundImage from './images/wallstreet_background.jpg';  // Importez l'image

function App() {
  const [showMenu, setShowMenu] = useState(true);
  const [gameSettings, setGameSettings] = useState({ mode: null, difficulty: null });

  // Ajouter un style pour l'arrière-plan
  const appStyle = {
    backgroundImage: `url(${backgroundImage})`,
    backgroundSize: 'cover',
    backgroundPosition: 'center',
    backgroundRepeat: 'no-repeat',
    minHeight: '100vh',
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
  };

  const handleStartGame = (settings) => {
    setGameSettings(settings);
    setShowMenu(false);
  };

  // Fonction pour afficher le mode et la difficulté
  const getGameModeText = () => {
    if (gameSettings.mode === 'local') {
      return 'Joueur vs Joueur';
    } else if (gameSettings.mode === 'ai') {
      const difficultyText = {
        'easy': 'Facile',
        'medium': 'Moyen',
        'hard': 'Difficile'
      }[gameSettings.difficulty];
      
      return `Joueur vs IA (${difficultyText})`;
    }
    return '';
  };

  return (
    <div className="App" style={appStyle}>  {/* Appliquez le style ici */}
      {showMenu ? (
        <Menu onStartGame={handleStartGame} />
      ) : (
        <div className="game-container">
          <button 
            className="back-to-menu-button"
            onClick={() => setShowMenu(true)}
          >
            Retour au menu
          </button>
          <div className="game-mode-indicator">
            Mode: {getGameModeText()}
          </div>
          <Game settings={gameSettings} />
        </div>
      )}
    </div>
  );
}

export default App;