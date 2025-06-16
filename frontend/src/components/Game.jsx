import React, { useState, useEffect } from 'react';
import Board from './Board';

const Game = ({ settings }) => {
  const [board, setBoard] = useState([]);
  const [selectedPiece, setSelectedPiece] = useState(null);
  const [validMoves, setValidMoves] = useState([]);
  const [currentPlayer, setCurrentPlayer] = useState('player1');
  const [message, setMessage] = useState('Chargement du jeu...');
  const [pendingCaptured, setPendingCaptured] = useState(null);
  
  // Nouvelles variables d'état pour gérer les EPC
  const [gamePhase, setGamePhase] = useState('move_pawn'); // 'move_pawn' ou 'move_epc'
  const [selectedEPC, setSelectedEPC] = useState(null);
  const [validEPCMoves, setValidEPCMoves] = useState([]);
  const [lastPawnPosition, setLastPawnPosition] = useState(null);
  
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
      
      if (gamePhase === 'move_pawn') {
        setMessage(`C'est au tour des ${getColorName(playerColors[currentPlayer])} de déplacer un pion`);
      } else {
        setMessage(`${getColorName(playerColors[currentPlayer])} doit maintenant déplacer un EPC`);
      }
    } catch (error) {
      console.error('Erreur lors du chargement du plateau:', error);
      setMessage('Erreur de connexion au serveur. Le backend est-il démarré?');
      
      // Créer un plateau de test si le backend n'est pas disponible
      const testBoard = Array(8).fill().map(() => Array(8).fill([{type: 'square', color: null, height: 1}]));
      setBoard(testBoard);
    }
  };

  // Fonction pour récupérer les mouvements valides des pions
  const fetchValidMoves = async (row, col) => {
    try {
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

  // Nouvelle fonction pour récupérer les mouvements valides des EPC
  const fetchValidEPCMoves = async (row, col) => {
    try {
      const params = new URLSearchParams({
        colorPair: settings?.colorPair || 'black-white'
      });
      
      console.log(`Fetching valid EPC moves for (${row},${col})`);
      const response = await fetch(`http://localhost:8000/valid_epc_moves/${row}/${col}?${params}`);
      
      if (!response.ok) {
        throw new Error(`Erreur réseau: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('Valid EPC moves received:', data);
      
      // Assigner les données à validEPCMoves
      setValidEPCMoves(Array.isArray(data) ? data : data.validMoves || []);
    } catch (error) {
      console.error('Erreur lors de la récupération des mouvements valides pour EPC:', error);
      setMessage(`Erreur: ${error.message}`);
    }
  };

  const handleSelectPiece = async (row, col) => {
    // Ne permettre la sélection de pièce que pendant la phase 'move_pawn'
    if (gamePhase !== 'move_pawn') {
      setMessage('Vous devez d\'abord déplacer un EPC');
      return;
    }
    
    // Vérifier que la pièce sélectionnée est un pion et de la bonne couleur
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
    
    // Récupérer les mouvements valides depuis le backend
    fetchValidMoves(row, col);
  };

<<<<<<< HEAD
  // Nouvelle version de handleMove qui choisit le bon endpoint
  const handleMove = async (row, col) => {
    if (!selectedPiece || !validMoves.some(move => move[0] === row && move[1] === col)) {
      return;
    }
    // Vérifie si la case d'arrivée contient un pion adverse
    const stack = board[row][col];
    const hasOpponentPawn = stack.some(p => p.type === 'Pawn' && p.color !== getPlayerColors()[currentPlayer]);
    if (hasOpponentPawn) {
      // Capture : utilise /attack_pion
      try {
        const attackBody = {
=======
  // Fonction handleSelectEPC mise à jour

  const handleSelectEPC = async (row, col) => {
    // Ne permettre la sélection d'EPC que pendant la phase 'move_epc'
    if (gamePhase !== 'move_epc') {
      setMessage('Vous devez d\'abord déplacer un pion');
      return;
    }
    
    // Supprimer complètement cette vérification qui force la sélection de l'EPC d'origine
    // if (lastPawnPosition && (row !== lastPawnPosition.row || col !== lastPawnPosition.col)) {
    //   setMessage(`Vous devez déplacer l'EPC à la position (${lastPawnPosition.row + 1},${lastPawnPosition.col + 1})`);
    //   return;
    // }
    
    // Vérifier que la case contient au moins une pièce carrée
    const hasSquare = board[row][col].some(piece => 
      piece.type === 'Square' || piece.type === 'square');
    
    if (!hasSquare) {
      setSelectedEPC(null);
      setValidEPCMoves([]);
      setMessage('Cette case ne contient pas d\'EPC');
      return;
    }
    
    // Vérifier que la case ne contient pas de pion
    const hasPawn = board[row][col].some(piece => 
      piece.type === 'Pawn' || piece.type === 'round');
    
    if (hasPawn) {
      setSelectedEPC(null);
      setValidEPCMoves([]);
      setMessage('Cette case contient un pion, vous ne pouvez pas déplacer cet EPC');
      return;
    }
    
    setSelectedEPC({ row, col });
    setMessage('EPC sélectionné. Choisissez une destination adjacente.');
    
    // Récupérer les mouvements valides pour l'EPC
    fetchValidEPCMoves(row, col);
  };

  // Modification de la fonction handleMove

  const handleMove = async (row, col) => {
    // Vérifier que nous sommes en phase de déplacement de pion
    if (gamePhase !== 'move_pawn') return;
    
    // Vérifier que le mouvement est valide
    if (!selectedPiece || !validMoves.some(move => move[0] === row && move[1] === col)) {
      return;
    }

    try {
      // Sauvegarder la position d'origine du pion
      const originPosition = { row: selectedPiece.row, col: selectedPiece.col };
      
      const response = await fetch('http://localhost:8000/move_pawn', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
>>>>>>> 61e071e0 (epc)
          start_row: selectedPiece.row,
          start_col: selectedPiece.col,
          end_row: row,
          end_col: col
<<<<<<< HEAD
        };
        console.log('POST /attack_pion', attackBody);
        const response = await fetch('http://localhost:8000/attack_pion', {
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
            setMessage('Sélectionnez une case pour déplacer le pion capturé');
            setSelectedPiece(null);
            return;
          }
          setMessage('Déplacement effectué');
          setSelectedPiece(null);
          setValidMoves([]);
          setCurrentPlayer(currentPlayer === 'player1' ? 'player2' : 'player1');
          fetchBoard();
        }
      } catch (error) {
        setMessage('Erreur lors de la capture');
      }
    } else {
      // Déplacement simple : utilise /move_pion
      try {
        const response = await fetch('http://localhost:8000/move_pion', {
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
          setCurrentPlayer(currentPlayer === 'player1' ? 'player2' : 'player1');
          fetchBoard();
        }
      } catch (error) {
        setMessage('Erreur lors du déplacement');
=======
        })
      });

      const result = await response.json();
      if (result.success) {
        // Mettre à jour l'état pour le changement de phase
        setSelectedPiece(null);
        setValidMoves([]);
        // On garde lastPawnPosition pour la mise en évidence visuelle uniquement
        setLastPawnPosition(originPosition);
        
        // Passer à la phase de déplacement d'EPC
        setGamePhase('move_epc');
        // Message plus générique
        setMessage(`${getColorName(playerColors[currentPlayer])}: Déplacez maintenant un EPC de votre choix`);
        
        fetchBoard(); // Rafraîchir le plateau
>>>>>>> 61e071e0 (epc)
      }
    }
  };

<<<<<<< HEAD
  // Gestion du choix de la destination du pion capturé
  const handleCapturedMove = async (row, col) => {
    if (!pendingCaptured || !pendingCaptured.validDest.some(move => move[0] === row && move[1] === col)) return;
    try {
      const body = {
        start_row: pendingCaptured.from.row,
        start_col: pendingCaptured.from.col,
        end_row: pendingCaptured.to.row,
        end_col: pendingCaptured.to.col,
        captured_dest: [row, col]
      };
      console.log('POST /attack_pion (choix position pion adverse)', body);
      const response = await fetch('http://localhost:8000/attack_pion', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      });
      const result = await response.json();
      setPendingCaptured(null);
      setValidMoves([]);
      setMessage('Pion capturé déplacé !');
      setCurrentPlayer(currentPlayer === 'player1' ? 'player2' : 'player1');
      fetchBoard();
    } catch (error) {
      setMessage('Erreur lors du déplacement du pion capturé');
=======
  // Nouvelle fonction pour déplacer un EPC
  const handleMoveEPC = async (row, col) => {
    if (!selectedEPC) return;
    
    console.log('Attempting to move EPC from', selectedEPC, 'to', {row, col});
    console.log('Valid EPC moves:', validEPCMoves);
    
    // Vérifier que le mouvement est valide
    if (!validEPCMoves.some(move => move[0] === row && move[1] === col)) {
      console.log('Move not in valid moves list');
      return;
    }

    try {
      console.log('Sending move_epc request with data:', {
        start_row: selectedEPC.row,
        start_col: selectedEPC.col,
        end_row: row,
        end_col: col
      });
      
      const response = await fetch('http://localhost:8000/move_epc', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          start_row: selectedEPC.row,
          start_col: selectedEPC.col,
          end_row: row,
          end_col: col
        })
      });

      const result = await response.json();
      console.log('Move EPC response:', result);
      
      if (result.success) {
        setMessage('EPC déplacé avec succès');
        setSelectedEPC(null);
        setValidEPCMoves([]);
        setLastPawnPosition(null);
        
        // Passer au joueur suivant et revenir à la phase de déplacement de pion
        setCurrentPlayer(currentPlayer === 'player1' ? 'player2' : 'player1');
        setGamePhase('move_pawn');
        
        fetchBoard(); // Rafraîchir le plateau
      } else {
        setMessage('Mouvement d\'EPC invalide');
      }
    } catch (error) {
      console.error('Error moving EPC:', error);
    }
  };

  // Fonction pour passer le tour de déplacement d'EPC
  const skipEPCMove = () => {
    if (gamePhase === 'move_epc') {
      setSelectedEPC(null);
      setValidEPCMoves([]);
      setLastPawnPosition(null);
      
      // Passer au joueur suivant et revenir à la phase de déplacement de pion
      setCurrentPlayer(currentPlayer === 'player1' ? 'player2' : 'player1');
      setGamePhase('move_pawn');
      
      setMessage(`C'est maintenant au tour des ${getColorName(playerColors[currentPlayer === 'player1' ? 'player1' : 'player2'])}`);
>>>>>>> 61e071e0 (epc)
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
      setSelectedEPC(null);
      setValidEPCMoves([]);
      setLastPawnPosition(null);
      setCurrentPlayer('player1');
      setGamePhase('move_pawn');
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

  // Fonction de gestion du clic sur une case
  const handleCellClick = async (row, col) => {
<<<<<<< HEAD
    if (selectedPiece && validMoves.some(move => move[0] === row && move[1] === col)) {
      // Si une pièce est sélectionnée et la case cliquée est un coup valide, on effectue le move
      await handleMove(row, col);
    } else if (pendingCaptured && pendingCaptured.validDest.some(dest => dest[0] === row && dest[1] === col)) {
      // Si un pion est en attente d'être capturé et la case cliquée est une destination valide, on effectue le déplacement du pion capturé
      await handleCapturedMove(row, col);
    } else {
      // Sinon, on sélectionne la pièce
      await handleSelectPiece(row, col);
=======
    console.log(`Cell clicked: ${row},${col} in phase: ${gamePhase}`);
    
    if (gamePhase === 'move_pawn') {
      // Phase 1: Déplacement de pion
      if (selectedPiece && validMoves.some(move => move[0] === row && move[1] === col)) {
        // Si un pion est sélectionné et le mouvement est valide
        await handleMove(row, col);
      } else {
        // Sinon, tenter de sélectionner un pion
        await handleSelectPiece(row, col);
      }
    } else if (gamePhase === 'move_epc') {
      // Phase 2: Déplacement d'EPC
      if (selectedEPC && validEPCMoves.some(move => move[0] === row && move[1] === col)) {
        // Si un EPC est sélectionné et le mouvement est valide
        console.log('Valid EPC move detected, calling handleMoveEPC');
        await handleMoveEPC(row, col);
      } else {
        // Sinon, tenter de sélectionner un EPC
        console.log('Attempting to select EPC');
        await handleSelectEPC(row, col);
      }
>>>>>>> 61e071e0 (epc)
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
        <div className="message">{message}</div>
        <div className="current-player">
          Joueur actuel: {getColorName(playerColors[currentPlayer])}
        </div>
        <div className="game-phase">
          Phase: {gamePhase === 'move_pawn' 
            ? 'Déplacement de pion' 
            : 'Déplacement d\'un EPC au choix'}
        </div>
        
        {gamePhase === 'move_epc' && (
          <div className="phase-help">
            Sélectionnez n'importe quel EPC sans pion pour le déplacer
          </div>
        )}
        
        {gamePhase === 'move_epc' && (
          <button className="skip-button" onClick={skipEPCMove}>
            Passer le déplacement d'EPC
          </button>
        )}
        
        <button onClick={resetGame} className="reset-button">Nouvelle partie</button>
      </div>
      
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
        />
      ) : (
        <p>Chargement du plateau...</p>
      )}
    </div>
  );
};

export default Game;