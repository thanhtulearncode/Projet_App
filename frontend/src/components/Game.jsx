import React, { useEffect, useRef, useState } from 'react';
import Board from './Board';
import Rules from './Rules';
import API_BASE_URL from '../config/api';
import './Game.css';

const Game = ({ settings }) => {
  const [board, setBoard] = useState([]);
  const [selectedPiece, setSelectedPiece] = useState(null);
  const [validMoves, setValidMoves] = useState([]);
  const [currentPlayer, setCurrentPlayer] = useState('player1');
  const [message, setMessage] = useState('Chargement du jeu...');
  const [pendingCaptured, setPendingCaptured] = useState(null);
  // Gestion EPC
  const [gamePhase, setGamePhase] = useState('move_pawn'); // 'move_pawn' ou 'move_epc'
  const [selectedEPC, setSelectedEPC] = useState(null);
  const [validEPCMoves, setValidEPCMoves] = useState([]);
  const [lastPawnPosition, setLastPawnPosition] = useState(null);
  const [lastPawnDestination, setLastPawnDestination] = useState(null);
  const [lastEPCPosition, setLastEPCPosition] = useState(null);
  const [lastEPCDestination, setLastEPCDestination] = useState(null);
  const [capturedDestination, setCapturedDestination] = useState(null);

  // Gestion de la fin de partie
  const [gameOver, setGameOver] = useState(false);
  const [winner, setWinner] = useState(null);
  const [showRules, setShowRules] = useState(false);
  // Gestion AI state
  const [aiState, setAIState] = useState(false);
  // New AI difficulty management
  const [currentAIDifficulty, setCurrentAIDifficulty] = useState(settings?.difficulty || 'medium');
  const [showDifficultySelector, setShowDifficultySelector] = useState(false);
  const [aiMoveTime, setAiMoveTime] = useState(null);

  // Définir les couleurs des joueurs
  const getPlayerColors = () => {
    if (settings?.colorPair?.startsWith('custom-')) {
      const idx = parseInt(settings.colorPair.split('-')[1], 10);
      const pair = settings.customColorPairs?.[idx];
      if (pair) {
        return { player1: pair.color1, player2: pair.color2 };
      }
    }
    switch (settings?.colorPair) {
      case 'red-green':
        return { player1: 'red', player2: 'green' };
      case 'orange-blue':
        return { player1: 'orange', player2: 'blue' };
      
      default:
        return { player1: 'white', player2: 'black' };
    }
  };
  const playerColors = getPlayerColors();

  const handleAnimation = (lastPawnPosition, lastPawnDestination, lastEPCPosition, lastEPCDestination) => {
    if (lastPawnPosition !== null) {
      setLastPawnPosition({row : lastPawnPosition[0],col: lastPawnPosition[1]});
    } else {
      setLastPawnPosition(null);
    }
    if (lastPawnDestination !== null) {
      setLastPawnDestination({row : lastPawnDestination[0], col : lastPawnDestination[1]});
    } else {
      setLastPawnDestination(null);
    }  
    if (lastEPCPosition !== null) {
      setLastEPCPosition({row : lastEPCPosition[0], col : lastEPCPosition[1]});
    } else {
      setLastEPCPosition(null);
    }
    if (lastEPCDestination !== null) {
      setLastEPCDestination({row : lastEPCDestination[0], col : lastEPCDestination[1]});
    } else {
      setLastEPCDestination(null);
    }
   if (capturedDestination !== null) {
      setCapturedDestination({row : capturedDestination[0], col : capturedDestination[1]});
    } else {
      setCapturedDestination(null);
    }
  };

  const getCustomColors = () => {
    if (settings?.colorPair?.startsWith('custom-')) {
      const idx = parseInt(settings.colorPair.split('-')[1], 10);
      const pair = settings.customColorPairs?.[idx];
      if (pair) return { color1: pair.color1, color2: pair.color2 };
    }
    return {};
  };

  useEffect(() => {
    fetchBoard();
    if (settings?.mode === 'ai') {
      fetchAIDifficulty();
    }
  }, []);

  // Fetch current AI difficulty from backend
  const fetchAIDifficulty = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/ai_difficulty`);
      if (response.ok) {
        const data = await response.json();
        setCurrentAIDifficulty(data.difficulty);
      }
    } catch (error) {
      console.log('Could not fetch AI difficulty, using default');
    }
  };

  // Set AI difficulty
  const setAIDifficulty = async (difficulty) => {
    try {
      const response = await fetch(`${API_BASE_URL}/set_ai_difficulty`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ difficulty })
      });
      if (response.ok) {
        const data = await response.json();
        setCurrentAIDifficulty(difficulty);
        setMessage(`Niveau IA changé à ${getDifficultyName(difficulty)}`);
        setShowDifficultySelector(false);
      }
    } catch (error) {
      setMessage('Erreur lors du changement de niveau IA');
    }
  };

  const getDifficultyName = (difficulty) => {
    switch (difficulty) {
      case 'easy': return 'Facile';
      case 'medium': return 'Moyen';
      case 'hard': return 'Difficile';
      default: return difficulty;
    }
  };

  const getDifficultyEmoji = (difficulty) => {
    switch (difficulty) {
      case 'easy': return '😊';
      case 'medium': return '😐';
      case 'hard': return '😈';
      default: return '🤖';
    }
  };

  const fetchBoard = async () => {
    try {
      const params = new URLSearchParams({
        colorPair: settings.colorPair,
        ...(settings.colorPair.startsWith('custom-') && settings.customColorPairs
          ? {
              color1: settings.customColorPairs[parseInt(settings.colorPair.split('-')[1], 10)].color1,
              color2: settings.customColorPairs[parseInt(settings.colorPair.split('-')[1], 10)].color2,
            }
          : {})
      });
      const response = await fetch(`${API_BASE_URL}/board?${params}`);
      if (!response.ok) throw new Error('Erreur réseau');
      const data = await response.json();
      setBoard(data);
      if (gamePhase === 'move_pawn') {
        setMessage(`C'est au tour des ${getColorName(playerColors[currentPlayer])} de déplacer un pion`);
      } else {
        setMessage(`${getColorName(playerColors[currentPlayer])} doit maintenant déplacer un EPC`);
      }
      console.log('mode',settings?.mode || 'local');
    } catch (error) {
      setMessage('Erreur de connexion au serveur. Le backend est-il démarré?');
      const testBoard = Array(8).fill().map(() => Array(8).fill([{type: 'square', color: null, height: 1}]));
      setBoard(testBoard);
      
    }
  };

  // Mouvements valides pion
  const fetchValidMoves = async (row, col) => {
    try {
      const params = new URLSearchParams({
        mode: settings?.mode || 'local',
        difficulty: settings?.difficulty || 'medium',
        colorPair: settings?.colorPair || 'black-white',
        ...getCustomColors()
      });
      const response = await fetch(`${API_BASE_URL}/valid_moves/${row}/${col}?${params}`);
      if (!response.ok) throw new Error('Erreur réseau');
      const data = await response.json();
      setValidMoves(Array.isArray(data) ? data : data.validMoves || []);
    } catch (error) {
      setMessage('Erreur lors de la récupération des mouvements valides');
    }
  };

  // Mouvements valides EPC
  const fetchValidEPCMoves = async (row, col) => {
    try {
      const params = new URLSearchParams({
        colorPair: settings?.colorPair || 'black-white',
        ...getCustomColors()
      });
      const response = await fetch(`${API_BASE_URL}/valid_moves/${row}/${col}?${params}`);
      if (!response.ok) throw new Error(`Erreur réseau: ${response.status}`);
      const data = await response.json();
      setValidEPCMoves(Array.isArray(data) ? data : data.validMoves || []);
    } catch (error) {
      setMessage(`Erreur: ${error.message}`);
    }
  };

  // Sélection pion
  const handleSelectPiece = async (row, col) => {
    if (gamePhase !== 'move_pawn') {
      setMessage('Vous devez d\'abord déplacer un EPC');
      return;
    }
    if (aiState) {
      setMessage('L\'IA est en train de jouer, veuillez patienter');
      return;
    }
    if (board[row][col].length === 0 || 
        board[row][col][board[row][col].length - 1].type !== 'Pawn' || 
        board[row][col][board[row][col].length - 1].color !== playerColors[currentPlayer]) {
      setSelectedPiece(null);
      setValidMoves([]);
      setMessage('Sélection invalide, veuillez choisir une pièce de votre couleur');
      return;
    }
    setSelectedPiece({ row, col });
    setMessage('Pion sélectionné. Choisissez une destination.');
    fetchValidMoves(row, col);
  };

  // Sélection EPC
  const handleSelectEPC = async (row, col) => {
    if (gamePhase !== 'move_epc') {
      setMessage('Vous devez d\'abord déplacer un pion');
      return;
    }
    // Vérifier qu'il y a au moins une pièce carrée
    const hasSquare = board[row][col].some(piece => piece.type === 'Square' || piece.type === 'square');
    if (!hasSquare) {
      setSelectedEPC(null);
      setValidEPCMoves([]);
      setMessage('Cette case ne contient pas d\'EPC');
      return;
    }
    // Vérifier qu'il n'y a pas de pion
    const hasPawn = board[row][col].some(piece => piece.type === 'Pawn' || piece.type === 'round');
    if (hasPawn) {
      setSelectedEPC(null);
      setValidEPCMoves([]);
      setMessage('Cette case contient un pion, vous ne pouvez pas déplacer cet EPC');
      return;
    }
    setSelectedEPC({ row, col });
    setMessage('EPC sélectionné. Choisissez une destination adjacente.');
    fetchValidEPCMoves(row, col);
  };

  const playMoveSound = () => {
    const audio = new window.Audio('/sounds/move.mp3');
    audio.volume = 0.5;
    audio.play();
  };

  // Fonction pour jouer un son d'alerte
  const playClockSound = () => {
    const audio = new window.Audio('/sounds/clock.mp3');
    audio.play();
  };

  // Déplacement pion (inclut capture)
  const handleMove = async (row, col) => {
    if (gamePhase !== 'move_pawn') return;
    if (!selectedPiece || !validMoves.some(move => move[0] === row && move[1] === col)) return;
    // Vérifie si la case d'arrivée contient un pion adverse
    const stack = board[row][col];
    const hasOpponentPawn = stack.some(p => p.type === 'Pawn' && p.color !== playerColors[currentPlayer]);
    if (hasOpponentPawn) {
      // Capture
      try {
        const attackBody = {
          start_row: selectedPiece.row,
          start_col: selectedPiece.col,
          end_row: row,
          end_col: col
        };
        const response = await fetch(`${API_BASE_URL}/attack_pion`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(attackBody)
        });
        const result = await response.json();
        if (result.success) {
          if (result.captured && result.captured_valid_dest && result.captured_valid_dest.length > 0) {
            setPendingCaptured({
              from: { row: selectedPiece.row, col: selectedPiece.col },
              to: { row, col },
              validDest: result.captured_valid_dest
            });
            setValidMoves(result.captured_valid_dest);
            setSelectedPiece(null);
            setMessage('Sélectionnez une case pour déplacer le pion capturé');
            return;
          }
          setMessage('Déplacement effectué');
          setSelectedPiece(null);
          setValidMoves([]);
          setGamePhase('move_epc');
          fetchBoard();
          handleAnimation(selectedPiece, { row, col }, null, null);
        }
      } catch (error) {
        setMessage('Erreur lors de la capture');
      }
    } else {
      // Déplacement simple
      try {
        const response = await fetch(`${API_BASE_URL}/move_pawn`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            start_row: selectedPiece.row,
            start_col: selectedPiece.col,
            end_row: row,
            end_col: col
          })
        });
        const result = await response.json();
        if (result.success) {
          playMoveSound(); // <-- Joue le son ici
          setMessage('Déplacement effectué');
          setSelectedPiece(null);
          setValidMoves([]);
          setGamePhase('move_epc');
          fetchBoard();
          handleAnimation(selectedPiece, { row, col }, null, null);
        } else {
          setMessage('Mouvement invalide');
        }
      } catch (error) {
        setMessage('Erreur lors du déplacement');
      }
    }
  };

  const handleCapturedMove = async (row, col) => {
    if (!pendingCaptured) return;
    try {
      const response = await fetch(`${API_BASE_URL}/attack_pion`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          start_row: pendingCaptured.from.row,
          start_col: pendingCaptured.from.col,
          end_row: pendingCaptured.to.row,
          end_col: pendingCaptured.to.col,
          captured_dest: [row, col]
        })
      });
      const result = await response.json();
      if (result.success) {
        setMessage('Capture et déplacement effectués');
        setPendingCaptured(null);
        setValidMoves([]);
        setGamePhase('move_epc');
        fetchBoard();
        handleAnimation(pendingCaptured.from, pendingCaptured.to, null, null);
      } else {
        setMessage('Erreur lors de la capture');
      }
    } catch (error) {
      setMessage('Erreur lors de la capture');
    }
  };

  const handleMoveEPC = async (row, col) => {
    if (gamePhase !== 'move_epc') return;
    if (!selectedEPC || !validEPCMoves.some(move => move[0] === row && move[1] === col)) return;
    try {
      const response = await fetch(`${API_BASE_URL}/move_square`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          src_row: selectedEPC.row,
          src_col: selectedEPC.col,
          dst_row: row,
          dst_col: col
        })
      });
      const result = await response.json();
      if (result.success) {
        setMessage('Déplacement d\'EPC effectué');
        setSelectedEPC(null);
        setValidEPCMoves([]);
        setCurrentPlayer(currentPlayer === 'player1' ? 'player2' : 'player1');
        setGamePhase('move_pawn');
        fetchBoard();
        handleAnimation(null, null, selectedEPC, { row, col });
        if (settings?.mode === 'ai') {
          handleAIPlay();
        }
      } else {
        setMessage('Mouvement d\'EPC invalide');
      }
    } catch (error) {
      setMessage('Erreur lors du déplacement EPC');
    }
  };

  const handleAIPlay = async () => {
    try {
      setAIState(true);
      setMessage(`L'IA ${getDifficultyName(currentAIDifficulty)} réfléchit...`);
      const startTime = Date.now();
      
      const params = new URLSearchParams({
        colorPair: settings?.colorPair || 'black-white',
        ...getCustomColors()
      });
      const response = await fetch(`${API_BASE_URL}/ai_move?${params}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({})
      });
      
      const endTime = Date.now();
      const moveTime = (endTime - startTime) / 1000; // Convert to seconds
      setAiMoveTime(moveTime);
      
      if (!response.ok) throw new Error('Erreur réseau');
      const data = await response.json();
      if (data.success) { 
        setMessage(`L'IA ${getDifficultyName(data.ai_difficulty || currentAIDifficulty)} a joué en ${moveTime.toFixed(2)}s`);
        fetchBoard();
        setAIState(false);
        setCurrentPlayer('player1');
        setGamePhase('move_pawn');
        setSelectedPiece(null);
        setValidMoves([]);
        handleAnimation(data.pawnPosition, data.pawnDestination, data.EPCPosition, data.EPCDestination, data.capturedDestination);
      } else {
        setMessage('L\'IA n\'a pas pu jouer');
        setAIState(false);
      }
    } catch (error) { 
      setMessage('Erreur lors du coup de l\'IA');
      setAIState(false);
    }
  };

  // Passer le déplacement EPC
  const skipEPCMove = () => {
    if (gamePhase === 'move_epc') {
      setSelectedEPC(null);
      setValidEPCMoves([]);
      setLastPawnPosition(null);
      setCurrentPlayer(currentPlayer === 'player1' ? 'player2' : 'player1');
      setGamePhase('move_pawn');
      setMessage(`C'est maintenant au tour des ${getColorName(playerColors[currentPlayer === 'player1' ? 'player1' : 'player2'])}`);
    }
  };

  // Reset
  const resetGame = async () => {
    try {
      const params = new URLSearchParams({
        colorPair: settings?.colorPair || 'black-white',
        ai_difficulty: currentAIDifficulty,
        ...getCustomColors()
      });
      await fetch(`${API_BASE_URL}/reset?${params}`, { method: 'POST' });
      fetchBoard();
      setSelectedPiece(null);
      setValidMoves([]);
      setSelectedEPC(null);
      setValidEPCMoves([]);
      handleAnimation(null, null, null, null);
      setCurrentPlayer('player1');
      setGamePhase('move_pawn');
      setAIState(false);
      setGameOver(false);
      setWinner(null);
      setAiMoveTime(null);
      setMessage('Nouvelle partie commencée');
    } catch (error) {
      setMessage('Erreur de connexion au serveur');
    }
  };

  // Nom couleur
  const getColorName = (color) => {
    switch (color) {
      case 'white': return 'Blanc';
      case 'black': return 'Noir';
      case 'red': return 'Rouge';
      case 'green': return 'Vert';
      case 'orange': return 'Orange';
      case 'blue': return 'Bleu';
      default: return color;
    }
  };

  // Vérifie la fin du jeu
  const checkGameOver = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/is_game_over`);
      if (!response.ok) throw new Error('Erreur réseau');
      const data = await response.json();
      if (data.game_over) {
        setGameOver(true);
        setWinner(data.winner);
        setMessage(
          data.winner === 'draw'
            ? 'Match nul !'
            : `Victoire des ${getColorName(data.winner)} !`
        );
      } else {
        setGameOver(false);
        setWinner(null);
      }
    } catch (error) {
      // Ne rien faire, on garde l'état précédent
    }
  };

  // Appeler checkGameOver après chaque action importante
  useEffect(() => {
    checkGameOver();
  }, [board]);

  // Clic sur case
  const handleCellClick = async (row, col) => {
    if (gameOver) return;
    if (gamePhase === 'move_pawn') {
      if (selectedPiece && validMoves.some(move => move[0] === row && move[1] === col)) {
        await handleMove(row, col);
      } else if (pendingCaptured && pendingCaptured.validDest.some(dest => dest[0] === row && dest[1] === col)) {
        await handleCapturedMove(row, col);
      } else {
        await handleSelectPiece(row, col);
      }
    } else if (gamePhase === 'move_epc') {
      if (selectedEPC && validEPCMoves.some(move => move[0] === row && move[1] === col)) {
        await handleMoveEPC(row, col);
      } else {
        await handleSelectEPC(row, col);
      }
    }
  };

  // AI Difficulty Selector Component
  const AIDifficultySelector = () => {
    if (!showDifficultySelector) return null;
    
    return (
      <div className="ai-difficulty-selector">
        <div className="difficulty-selector-content">
          <h3>Changer le niveau de l'IA</h3>
          <div className="difficulty-options">
            <button 
              className={`difficulty-option ${currentAIDifficulty === 'easy' ? 'selected' : ''}`}
              onClick={() => setAIDifficulty('easy')}
            >
              <span className="difficulty-emoji">😊</span>
              <span className="difficulty-name">Facile</span>
              <span className="difficulty-desc">Mouvements aléatoires</span>
            </button>
            <button 
              className={`difficulty-option ${currentAIDifficulty === 'medium' ? 'selected' : ''}`}
              onClick={() => setAIDifficulty('medium')}
            >
              <span className="difficulty-emoji">😐</span>
              <span className="difficulty-name">Moyen</span>
              <span className="difficulty-desc">Stratégie basique</span>
            </button>
            <button 
              className={`difficulty-option ${currentAIDifficulty === 'hard' ? 'selected' : ''}`}
              onClick={() => setAIDifficulty('hard')}
            >
              <span className="difficulty-emoji">😈</span>
              <span className="difficulty-name">Difficile</span>
              <span className="difficulty-desc">Stratégie avancée</span>
            </button>
          </div>
          <button 
            className="close-difficulty-selector"
            onClick={() => setShowDifficultySelector(false)}
          >
            Fermer
          </button>
        </div>
      </div>
    );
  };

  useEffect(() => {
    // Créer la signature programmatiquement
    const signature = document.createElement('div');
    signature.textContent = 'Wall Street';
    signature.style.position = 'fixed';
    signature.style.bottom = '20px';
    signature.style.left = '50%';
    signature.style.transform = 'translateX(-50%)';
    signature.style.fontFamily = 'Playfair Display, serif';
    signature.style.fontStyle = 'italic';
    signature.style.fontSize = '1.2rem';
    signature.style.color = 'rgba(255, 215, 0, 0.4)';
    signature.style.textShadow = '0 2px 10px rgba(0, 0, 0, 0.3)';
    signature.style.letterSpacing = '2px';
    signature.style.pointerEvents = 'none';
    signature.style.zIndex = '1000';
    signature.style.whiteSpace = 'nowrap';
    
    // Ajouter au document
    document.body.appendChild(signature);
    
    // Nettoyage lors du démontage du composant
    return () => {
      document.body.removeChild(signature);
    };
  }, []);

  return (
    <div className="game">
      {/* Fond avec effet radial */}
      <div className="game-background">
        <div className="game-logo-background"></div>
        <div className="animated-logo">
          <div className="logo-building"></div>
          <div className="logo-building"></div>
          <div className="logo-building"></div>
        </div>
      </div>

      <div className="game-content">

        <div className="game-sidebar mobile-order-1">
          <div className="game-proverb">
            "Focus To Win, Strategy To Conquer"
          </div>

          <div className="game-top-controls">
            <div className="current-player-indicator">
              <div 
                className="player-color-marker" 
                style={{ backgroundColor: playerColors[currentPlayer] }}
              ></div>
            </div>

            <div className="game-actions">
              {gamePhase === 'move_epc' && (
                <button className="action-button skip-button" onClick={skipEPCMove}>
                  Passer
                </button>
              )}
              <button className="action-button reset-button" onClick={resetGame}>
                Nouvelle partie
              </button>
              <button className="action-button rules-button" onClick={() => setShowRules(true)}>
                Règles
              </button>
            </div>

            {message && <div className="message-toast">{message}</div>}

            {settings?.mode === 'ai' && (
              <div className="ai-badge">
                <div className="ai-level">
                  {getDifficultyEmoji(currentAIDifficulty)}
                  <button 
                    className="ai-level-button"
                    onClick={() => setShowDifficultySelector(true)}
                    disabled={aiState}
                  >
                    {getDifficultyName(currentAIDifficulty)}
                  </button>
                </div>
              </div>
            )}
          </div>


        </div>
        <div className="game-board-center mobile-order-2">
          <div className="board-logo-background"></div>
          {board.length > 0 ? (
            <Board 
              board={board} 
              selectedPiece={gamePhase === 'move_pawn' ? selectedPiece : null}
              selectedEPC={gamePhase === 'move_epc' ? selectedEPC : null}
              validMoves={gamePhase === 'move_pawn' ? validMoves : validEPCMoves}
              onCellClick={handleCellClick}
              playerColors={playerColors}
              gamePhase={gamePhase}
              lastPawnPosition={lastPawnPosition}
              lastMoveDest={lastPawnDestination}
              lastEPCPosition={lastEPCPosition}
              lastEPCDestination={lastEPCDestination}
              capturedDestination={capturedDestination}
              currentPlayer={currentPlayer}
            />
          ) : (
            <div className="loading-board">
              <div className="spinner"></div>
              <p>Chargement du plateau...</p>
            </div>
          )}
        </div>

      </div>

      {/* Règles */}
      {showRules && <Rules onClose={() => setShowRules(false)} />}

      {/* Fin de partie */}
      {gameOver && (
        <div className="game-over">
          <h2>Fin de la partie</h2>
          <p>{winner === 'draw' ? 'Match nul !' : `Victoire des ${getColorName(winner)} !`}</p>
          <button onClick={resetGame}>Rejouer</button>
        </div>
      )}

      {/* Sélecteur de difficulté IA */}
      <AIDifficultySelector />

      {/* Signature Wall Street élégante */}
      <div className="wall-street-signature">Wall Street</div>
    </div>
  );

};

export default Game;