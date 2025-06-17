import React, { useState, useEffect } from 'react';
import Board from './Board';
import Rules from './Rules';

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
  const [gameOver, setGameOver] = useState(false);
  const [winner, setWinner] = useState(null);
  const [showRules, setShowRules] = useState(false);
  // Gestion AI state
  const [aiState, setAIState] = useState(false);

  // Définir les couleurs des joueurs
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

  useEffect(() => {
    fetchBoard();
  }, []);

  const updateBoard = (newBoard) => {
    setBoard(newBoard);
    if (gamePhase === 'move_pawn') {
        setMessage(`C'est au tour des ${getColorName(playerColors[currentPlayer])} de déplacer un pion`);
      } else {
        setMessage(`${getColorName(playerColors[currentPlayer])} doit maintenant déplacer un EPC`);
      }
  };

  const fetchBoard = async () => {
    try {
      const params = new URLSearchParams({
        colorPair: settings?.colorPair || 'black-white'
      });
      const response = await fetch(`http://localhost:8000/board?${params}`);
      if (!response.ok) throw new Error('Erreur réseau');
      const data = await response.json();
      setBoard(data);
      if (gamePhase === 'move_pawn') {
        setMessage(`C'est au tour des ${getColorName(playerColors[currentPlayer])} de déplacer un pion`);
      } else {
        setMessage(`${getColorName(playerColors[currentPlayer])} doit maintenant déplacer un EPC`);
      }
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
        colorPair: settings?.colorPair || 'black-white'
      });
      const response = await fetch(`http://localhost:8000/valid_moves/${row}/${col}?${params}`);
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
        colorPair: settings?.colorPair || 'black-white'
      });
      const response = await fetch(`http://localhost:8000/valid_moves/${row}/${col}?${params}`);
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
            setSelectedPiece(null);
            setMessage('Sélectionnez une case pour déplacer le pion capturé');
            return;
          }
          setMessage('Déplacement effectué');
          setSelectedPiece(null);
          setValidMoves([]);
          setLastPawnPosition({ row: selectedPiece.row, col: selectedPiece.col });
          setGamePhase('move_epc');
          updateBoard(result.board);
        }
      } catch (error) {
        setMessage('Erreur lors de la capture');
      }
    } else {
      // Déplacement simple
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
          setLastPawnPosition({ row: selectedPiece.row, col: selectedPiece.col });
          setGamePhase('move_epc');
          updateBoard(result.board);
        }
      } catch (error) {
        setMessage('Erreur lors du déplacement');
      }
    }
  };

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
      const response = await fetch('http://localhost:8000/attack_pion', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body)
      });
      const result = await response.json();
      setPendingCaptured(null);
      setValidMoves([]);
      setMessage('Pion capturé déplacé !');
      setLastPawnPosition({ row: pendingCaptured.from.row, col: pendingCaptured.from.col });
      setGamePhase('move_epc');
      updateBoard(result.board);
    } catch (error) {
      setMessage('Erreur lors du déplacement du pion capturé');
    }
  };

  // Déplacement EPC
  const handleMoveEPC = async (row, col) => {
    if (!selectedEPC) return;
    if (!validEPCMoves.some(move => move[0] === row && move[1] === col)) return;
    try {
      const response = await fetch('http://localhost:8000/move_square', {
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
        setMessage('EPC déplacé avec succès');
        setSelectedEPC(null);
        setValidEPCMoves([]);
        setLastPawnPosition(null);
        setCurrentPlayer(currentPlayer === 'player1' ? 'player2' : 'player1');
        setGamePhase('move_pawn');
        updateBoard(result.board);
        console.log('mode:', settings?.mode);
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
    //if (gamePhase !== 'move_pawn' || currentPlayer !== 'player2') return;
    try {
      setAIState(true);
      setMessage('L\'IA réfléchit...');
      const response = await fetch('http://localhost:8000/ai_move', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          board,
          playerColor: playerColors.player2,
          difficulty: settings?.difficulty || 'medium',
          colorPair: settings?.colorPair || 'black-white'
        })
      });
      if (!response.ok) throw new Error('Erreur réseau');
      const data = await response.json();
      if (data.success) { 
        setMessage('L\'IA a joué son coup');
        updateBoard(data.board);
        setAIState(false);
        setCurrentPlayer('player1');
        setGamePhase('move_pawn');
        setSelectedPiece(null);
        setValidMoves([]);
        setLastPawnPosition(null);
      } else {
        setMessage('L\'IA n\'a pas pu jouer');
      }
    } catch (error) { 
      setMessage('Erreur lors du coup de l\'IA');
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
        colorPair: settings?.colorPair || 'black-white'
      });
      const response = await fetch(`http://localhost:8000/reset?${params}`, { method: 'POST' });
      const data = await response.json();
      updateBoard(data.board);
      setSelectedPiece(null);
      setValidMoves([]);
      setSelectedEPC(null);
      setValidEPCMoves([]);
      setLastPawnPosition(null);
      setCurrentPlayer('player1');
      setGamePhase('move_pawn');
      setAIState(false);
      setGameOver(false);
      setWinner(null);
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
      const response = await fetch('http://localhost:8000/is_game_over');
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

  return (
    <div className="game">
      <div className="game-info">
      </div>
      <div className="game-info-panel">
        <button className="rules-side-button" onClick={() => setShowRules(true)}>
          Règles
        </button>




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
      {gameOver && (
        <div className="game-over">
          <h2>Fin de la partie</h2>
          <p>{winner === 'draw' ? 'Match nul !' : `Victoire des ${getColorName(winner)} !`}</p>
          <button onClick={resetGame}>Rejouer</button>
        </div>
      )}
    </div>
  );
};

export default Game;