import React from 'react';
import './Rules.css';

const Rules = ({ onClose }) => {
  return (
    <div className="rules-modal" onClick={onClose}>
      <div className="rules-content" onClick={(e) => e.stopPropagation()}>
        <button className="close-rules-button" onClick={onClose}>
          ×
        </button>
        
        <h2>Règles du jeu Wall Street</h2>
        
        <h3>Présentation</h3>
        <p>Wall Street est un jeu abstrait de stratégie dont le but est de posséder plus de buildings que la société adverse.</p>
        
        <h3>Préparation</h3>
        <p>On place d'abord les « pièces carrées » sur le plateau (une par case, sur toutes les cases du plateau), puis on place les pions comme présenté sur la photo de l'exemple 1.</p>
        <p>On tire au sort qui possède la White Company (les blancs) ; l'autre joueur possède la Black Industry (les noirs). White Company commence.</p>
        
        <h3>Déroulement d'un tour de jeu</h3>
        <p>Un tour est composé de deux phases :</p>
        
        <h4>Phase 1</h4>
        <p>Le joueur déplace un pion de sa couleur. Ce déplacement est orthogonal. Il peut avancer d'au maximum le nombre de pièces carrées que contient l'empilement de pièces carrées sur lequel il est placé.</p>
        <p>S'il est placé sur un empilement d'une seule pièce carrée, il ne peut avancer que d'une case. (Pour des raisons de lisibilité, l'expression « empilement de pièces carrées » sera abrégée en EPC.)</p>
        <p>Les cases ne contenant pas de pièce carrée ne comptent pas dans le décompte des cases.</p>
        <p>Le pion ne peut pas, pendant son déplacement, passer par une case occupée par un autre pion, et ne peut pas changer de direction au cours du déplacement (comme la tour aux échecs).</p>
        <p>Le pion déplacé peut atterrir sur une case occupée par un pion adverse uniquement s'il a parcouru, pour arriver sur cette case, la distance maximale autorisée par l'EPC d'origine. Dans ce cas, le joueur prend le pion adverse et le pose sur la case inoccupée de son choix.</p>
        
        <h4>Phase 2</h4>
        <p>Cette phase ne peut être exécutée qu'après le déplacement.</p>
        <p>Il s'agit de prendre un EPC situé sur une case non occupée par un pion, et de le déplacer vers un autre EPC également non occupé.</p>
        <p>L'EPC se déplace comme un pion, mais d'une seule case seulement.</p>
        <p>Le nouvel EPC ainsi formé ne peut contenir plus de 5 pièces carrées.</p>
        <p>Un empilement de 5 pièces carrées s'appelle un building.</p>
        
        <h3>Fin de partie</h3>
        <p>La partie s'arrête à l'instant où un joueur, qui devrait déplacer un EPC, ne peut plus le faire.</p>
        <p>Le gagnant est celui qui a le plus de pions situés sur des buildings.</p>
        <p>En cas d'égalité, le vainqueur est celui qui possède le plus de pions situés sur des EPC de 5 pièces, puis de 4, etc.</p>
      </div>
    </div>
  );
};

export default Rules;