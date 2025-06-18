import React, { useState, useEffect, useRef } from 'react';
import Cell from './Cell';

const Board = ({ 
  board, 
  selectedPiece, 
  selectedEPC,
  validMoves, 
  onCellClick, 
  playerColors,
  gamePhase,
  lastPawnPosition,
  lastMoveDest,
  lastEPCPosition,
  lastEPCDestination,
  currentPlayer
}) => {
  const [isFullscreen, setIsFullscreen] = useState(false);
  const boardRef = useRef(null);

  // Fonction pour gérer le basculement du mode plein écran
  const toggleFullscreen = () => {
    if (!isFullscreen) {
      // Passer en plein écran
      if (boardRef.current.requestFullscreen) {
        boardRef.current.requestFullscreen();
      } else if (boardRef.current.webkitRequestFullscreen) { /* Safari */
        boardRef.current.webkitRequestFullscreen();
      } else if (boardRef.current.msRequestFullscreen) { /* IE11 */
        boardRef.current.msRequestFullscreen();
      }
    } else {
      // Quitter le plein écran
      if (document.exitFullscreen) {
        document.exitFullscreen();
      } else if (document.webkitExitFullscreen) { /* Safari */
        document.webkitExitFullscreen();
      } else if (document.msExitFullscreen) { /* IE11 */
        document.msExitFullscreen();
      }
    }
  };

  // Événement pour détecter quand le plein écran est fermé par l'utilisateur (via Escape par exemple)
  useEffect(() => {
    const handleFullscreenChange = () => {
      const isFullscreenNow = !!(
        document.fullscreenElement || 
        document.webkitFullscreenElement || 
        document.msFullscreenElement
      );
      setIsFullscreen(isFullscreenNow);
    };

    document.addEventListener('fullscreenchange', handleFullscreenChange);
    document.addEventListener('webkitfullscreenchange', handleFullscreenChange);
    document.addEventListener('msfullscreenchange', handleFullscreenChange);

    return () => {
      document.removeEventListener('fullscreenchange', handleFullscreenChange);
      document.removeEventListener('webkitfullscreenchange', handleFullscreenChange);
      document.removeEventListener('msfullscreenchange', handleFullscreenChange);
    };
  }, []);

  // Rendre les cellules du plateau
  const renderBoard = () => {
    return board.map((row, rowIndex) => (
      <div key={rowIndex} className="row">
        {row.map((stack, colIndex) => {
          // Déterminer si la cellule est sélectionnée
          let isSelected = false;
          if (gamePhase === 'move_pawn' && selectedPiece) {
            isSelected = selectedPiece.row === rowIndex && selectedPiece.col === colIndex;
          } else if (gamePhase === 'move_epc' && selectedEPC) {
            isSelected = selectedEPC.row === rowIndex && selectedEPC.col === colIndex;
          }
          
          // Déterminer si c'est un mouvement valide
          const isValidMove = validMoves.some(move => move[0] === rowIndex && move[1] === colIndex);
          
          // Déterminer si c'est la position d'origine du pion
          const isLastPawnPosition = lastPawnPosition && 
                                    lastPawnPosition.row === rowIndex && 
                                    lastPawnPosition.col === colIndex;
          const isLastPawnDestination = lastMoveDest &&
              lastMoveDest.row === rowIndex &&
              lastMoveDest.col === colIndex;
          
          // Déterminer si cette cellule doit animer la pièce
          const animateMove = lastMoveDest &&
            lastMoveDest.row === rowIndex &&
            lastMoveDest.col === colIndex;
          
          // Déterminer si c'est la position d'origine de l'EPC
          const isLastEPCPosition = lastEPCPosition &&  
            lastEPCPosition.row === rowIndex && 
            lastEPCPosition.col === colIndex;
          const isLastEPCDestination = lastEPCDestination &&
            lastEPCDestination.row === rowIndex &&
            lastEPCDestination.col === colIndex;
          return (
            <Cell
              key={colIndex}
              stack={stack}
              onClick={() => onCellClick(rowIndex, colIndex)}
              isSelected={isSelected}
              isValidMove={isValidMove}
              playerColors={playerColors}
              gamePhase={gamePhase}
              isLastPawnPosition={isLastPawnPosition}
              isLastPawnDestination={isLastPawnDestination}
              isLastEPCPosition={isLastEPCPosition}
              isLastEPCDestination={isLastEPCDestination}
              animateMove={animateMove}
              isFullscreen={isFullscreen}
            />
          );
        })}
      </div>
    ));
  };

  return (
    <div 
      className="board-container" 
      ref={boardRef}
      data-turn={currentPlayer ? `Tour: Joueur ${currentPlayer}` : ''}
    >
      {isFullscreen ? (
        <div className={`board fullscreen`}>
          <div className="board-fullscreen-wrapper">
            {renderBoard()}
          </div>
          
          <div className="fullscreen-info">
            <div className="game-phase">
              {gamePhase === 'move_pawn' ? 'Phase: Déplacement de Pion' : 'Phase: Déplacement d\'EPC'}
            </div>
            {currentPlayer && (
              <div className="player-turn" style={{color: playerColors[currentPlayer]}}>
                Tour: Joueur {currentPlayer}
              </div>
            )}
          </div>
        </div>
      ) : (
        <div className="board">
          {renderBoard()}
        </div>
      )}
      
      <button 
        className="fullscreen-toggle" 
        onClick={toggleFullscreen}
        title={isFullscreen ? "Quitter le plein écran" : "Afficher en plein écran"}
      >
        <i className={`fas fa-${isFullscreen ? 'compress' : 'expand'}`}></i>
      </button>
    </div>
  );
};

export default Board;