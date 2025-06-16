import React, { useState, useEffect } from 'react';
import Board from './Board';

const Game = ({ settings }) => {
  const [board, setBoard] = useState([]);
  const [selectedPiece, setSelectedPiece] = useState(null);
  const [validMoves, setValidMoves] = useState([]);
  const [currentPlayer, setCurrentPlayer] = useState('player1');
  const [message, setMessage] = useState('Chargement du jeu...');
  
  // Définir les couleurs des joueurs en fonction de la paire de couleurs sélectionnée
  const getPlayerColors = () => {
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

  // Charger l'état initial du plateau
  useEffect(() => {
    fetchBoard();
  }, []);

  const fetchBoard = async () => {
    try {
      // Ajouter les couleurs sélectionnées comme paramètres
      const params = new URLSearchParams({
        colorPair: settings?.colorPair || 'black-white'
      });
      
      const response = await fetch(`http://localhost:8000/board?${params}`);
      if (!response.ok) {
        throw new Error('Erreur réseau');
      }
      const data = await response.json();
      setBoard(data);
      setMessage(`C'est au tour des ${playerColors.player1}`);
    } catch (error) {
      console.error('Erreur lors du chargement du plateau:', error);
      setMessage('Erreur de connexion au serveur. Le backend est-il démarré?');
      
      // Créer un plateau de test si le backend n'est pas disponible
      const testBoard = Array(8).fill().map(() => Array(8).fill([{type: 'square', color: null, height: 1}]));
      setBoard(testBoard);
    }
  };

  // Utiliser les paramètres de difficulté et couleurs lors des appels à l'API
  const fetchValidMoves = async (row, col) => {
    try {
      // Transmettre le mode, la difficulté et les couleurs au backend
      const params = new URLSearchParams({
        mode: settings?.mode || 'local',
        difficulty: settings?.difficulty || 'medium',
        colorPair: settings?.colorPair || 'black-white'
      });
      
      const response = await fetch(`http://localhost:8000/valid_moves/${row}/${col}?${params}`);
      if (!response.ok) {
        throw new Error('Erreur réseau');
      }
      const data = await response.json();
      setValidMoves(Array.isArray(data) ? data : data.validMoves || []);
    } catch (error) {
      console.error('Erreur lors de la récupération des mouvements valides:', error);
    }
  };

  const handleSelectPiece = async (row, col) => {
    // Logique de sélection de pièce
    if (board[row][col][board[row][col].length - 1].type !== 'Pawn' || board[row][col][board[row][col].length - 1].color !== getPlayerColors()[currentPlayer]) {
      setSelectedPiece(null);
      setValidMoves([]);
      console.log('selectedPiece', selectedPiece);
      console.log('stack', board[row][col]);
      console.log('type', board[row][col][board[row][col].length - 1].type);
      console.log('player', getPlayerColors()[currentPlayer]);
      setMessage('Sélection invalide, veuillez choisir une pièce de votre couleur');
      return;
    }
    setSelectedPiece({ row, col });
    setMessage('Pièce sélectionnée');
    
    // Récupérer les mouvements valides depuis le backend
    fetchValidMoves(row, col);
  };

  const handleMove = async (row, col) => {
    // Logique de déplacement simplifiée pour le moment
    if (!selectedPiece || !validMoves.some(move => move[0] === row && move[1] === col)) {
      return;
    }

    try {
      const response = await fetch('http://localhost:8000/move_pawn', {
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
        setMessage('Déplacement effectué');
        setSelectedPiece(null);
        setValidMoves([]);
    
        // Simuler un changement de joueur
        setCurrentPlayer(currentPlayer === 'player1' ? 'player2' : 'player1');
        fetchBoard(); // Rafraîchir le plateau
      }
    } catch (error) {
      console.error('Error making move:', error);
    }
    
  };

  const resetGame = async () => {
    try {
      // Inclure les couleurs dans la réinitialisation
      const params = new URLSearchParams({
        colorPair: settings?.colorPair || 'black-white'
      });
      
      await fetch(`http://localhost:8000/reset?${params}`, { method: 'POST' });
      fetchBoard();
      setSelectedPiece(null);
      setValidMoves([]);
      setCurrentPlayer('player1');
      setMessage('Nouvelle partie commencée');
    } catch (error) {
      console.error('Erreur lors de la réinitialisation:', error);
      setMessage('Erreur de connexion au serveur');
    }
  };

  // Fonction pour afficher le nom de la couleur en français
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

  // Nouvelle fonction de gestion du clic sur une case
  const handleCellClick = async (row, col) => {
    if (selectedPiece && validMoves.some(move => move[0] === row && move[1] === col)) {
      // Si une pièce est sélectionnée et la case cliquée est un coup valide, on effectue le move
      await handleMove(row, col);
    } else {
      // Sinon, on sélectionne la pièce
      await handleSelectPiece(row, col);
    }
  };

  return (
    <div className="game">
      <div className="game-info">
        {settings?.mode === 'ai' && (
          <div className="ai-indicator">
            IA: {settings.difficulty === 'easy' ? 'Facile 😊' : 
                settings.difficulty === 'medium' ? 'Moyen 😐' : 'Difficile 😈'}
          </div>
        )}
        <div className="color-indicator">
          Couleurs: {getColorName(playerColors.player1)} vs {getColorName(playerColors.player2)}
        </div>
        <div>{message}</div>
        <div>Joueur actuel: {getColorName(playerColors[currentPlayer])}</div>
        <button onClick={resetGame}>Nouvelle partie</button>
      </div>
      
      {board.length > 0 ? (
        <Board 
          board={board} 
          selectedPiece={selectedPiece}
          validMoves={validMoves}
          onSelectPiece={() => {}} // plus utilisé directement
          onMove={() => {}} // plus utilisé directement
          onCellClick={handleCellClick}
          playerColors={playerColors}
        />
      ) : (
        <p>Chargement du plateau...</p>
      )}
    </div>
  );
};

export default Game;