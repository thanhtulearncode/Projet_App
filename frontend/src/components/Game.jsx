import React, { useState, useEffect } from 'react';
import Board from './Board';

const Game = () => {
  const [board, setBoard] = useState([]);
  const [selectedPiece, setSelectedPiece] = useState(null);
  const [validMoves, setValidMoves] = useState([]);
  const [currentPlayer, setCurrentPlayer] = useState('white');
  const [message, setMessage] = useState('');

  // Charger l'état initial du plateau
  useEffect(() => {
    fetchBoard();
  }, []);

  const fetchBoard = async () => {
    try {
      console.log("Fetching board data...");
      const response = await fetch('/board');
      const data = await response.json();
      console.log("Board data received:", data);
      setBoard(data);
    } catch (error) {
      console.error('Error fetching board:', error);
      setMessage('Impossible de charger le plateau de jeu');
    }
  };

  const handleSelectPiece = async (row, col) => {
    // Vérifier si c'est bien un pion et du bon joueur
    if (board[row][col].type !== 'round' || board[row][col].color !== currentPlayer) {
      setSelectedPiece(null);
      setValidMoves([]);
      return;
    }

    setSelectedPiece({ row, col });
    
    try {
      const response = await fetch(`http://localhost:8000/valid_moves/${row}/${col}`);
      const moves = await response.json();
      setValidMoves(moves);
    } catch (error) {
      console.error('Error fetching valid moves:', error);
    }
  };

  const handleMove = async (row, col) => {
    if (!selectedPiece || !validMoves.some(move => move[0] === row && move[1] === col)) {
      return;
    }

    try {
      const response = await fetch('http://localhost:8000/move', {
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
        setCurrentPlayer(result.current_player);
        setMessage(result.captured ? 'Capture réussie!' : 'Déplacement effectué');
        fetchBoard(); // Rafraîchir le plateau
      }
    } catch (error) {
      console.error('Error making move:', error);
    }

    setSelectedPiece(null);
    setValidMoves([]);
  };

  const resetGame = async () => {
    try {
      await fetch('http://localhost:8000/reset', { method: 'POST' });
      fetchBoard();
      setCurrentPlayer('white');
      setMessage('');
    } catch (error) {
      console.error('Error resetting game:', error);
    }
  };

  return (
    <div className="game">
      <h1>NoNameGame</h1>
      {board.length === 0 ? (
        <div>
          <p>Chargement du plateau de jeu...</p>
          <button onClick={fetchBoard}>Réessayer</button>
        </div>
      ) : (
        <>
          <div className="game-info">
            <h2>Tour du joueur: {currentPlayer === 'black' ? 'Noir' : 'Blanc'}</h2>
            <button onClick={resetGame}>Recommencer</button>
            {message && <p className="message">{message}</p>}
          </div>
          <Board 
            board={board} 
            selectedPiece={selectedPiece}
            validMoves={validMoves}
            onSelectPiece={handleSelectPiece}
            onMove={handleMove}
          />
        </>
      )}
    </div>
  );
};

export default Game;