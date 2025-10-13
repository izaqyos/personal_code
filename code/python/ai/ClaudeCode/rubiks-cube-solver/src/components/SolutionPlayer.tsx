import React, { useState, useEffect } from 'react';
import { Move } from '../types/cube';

interface SolutionPlayerProps {
  moves: Move[];
  onMoveApplied: (move: Move) => void;
  isPlaying: boolean;
  onPlayingChange: (playing: boolean) => void;
}

const SolutionPlayer: React.FC<SolutionPlayerProps> = ({ 
  moves, 
  onMoveApplied, 
  isPlaying, 
  onPlayingChange 
}) => {
  const [currentMoveIndex, setCurrentMoveIndex] = useState(0);
  const [speed, setSpeed] = useState(1000); // ms between moves

  useEffect(() => {
    if (isPlaying && currentMoveIndex < moves.length) {
      const timer = setTimeout(() => {
        onMoveApplied(moves[currentMoveIndex]);
        setCurrentMoveIndex(prev => prev + 1);
      }, speed);

      return () => clearTimeout(timer);
    } else if (currentMoveIndex >= moves.length) {
      onPlayingChange(false);
      setCurrentMoveIndex(0);
    }
  }, [isPlaying, currentMoveIndex, moves, onMoveApplied, onPlayingChange, speed]);

  const handlePlay = () => {
    if (currentMoveIndex >= moves.length) {
      setCurrentMoveIndex(0);
    }
    onPlayingChange(true);
  };

  const handlePause = () => {
    onPlayingChange(false);
  };

  const handleReset = () => {
    onPlayingChange(false);
    setCurrentMoveIndex(0);
  };

  const handleStepForward = () => {
    if (currentMoveIndex < moves.length) {
      onMoveApplied(moves[currentMoveIndex]);
      setCurrentMoveIndex(prev => prev + 1);
    }
  };

  const handleStepBackward = () => {
    if (currentMoveIndex > 0) {
      setCurrentMoveIndex(prev => prev - 1);
      // Note: This would need reverse move implementation
    }
  };

  if (moves.length === 0) {
    return null;
  }

  return (
    <div className="solution-player">
      <div className="solution-progress">
        <div className="progress-bar">
          <div 
            className="progress-fill" 
            style={{ width: `${(currentMoveIndex / moves.length) * 100}%` }}
          />
        </div>
        <div className="progress-text">
          {currentMoveIndex} / {moves.length} moves
        </div>
      </div>

      <div className="solution-controls">
        <button 
          onClick={handleStepBackward}
          disabled={currentMoveIndex === 0}
          className="control-btn"
        >
          ⏮
        </button>
        
        {isPlaying ? (
          <button onClick={handlePause} className="control-btn play-pause">
            ⏸
          </button>
        ) : (
          <button onClick={handlePlay} className="control-btn play-pause">
            ▶️
          </button>
        )}
        
        <button 
          onClick={handleStepForward}
          disabled={currentMoveIndex >= moves.length}
          className="control-btn"
        >
          ⏭
        </button>
        
        <button onClick={handleReset} className="control-btn">
          🔄
        </button>
      </div>

      <div className="speed-control">
        <label>Speed: </label>
        <input
          type="range"
          min="200"
          max="2000"
          value={speed}
          onChange={(e) => setSpeed(Number(e.target.value))}
          className="speed-slider"
        />
        <span>{(2000 - speed) / 200 + 1}x</span>
      </div>

      <div className="current-move">
        Current move: {currentMoveIndex < moves.length ? moves[currentMoveIndex] : 'Complete'}
      </div>

      <div className="moves-sequence">
        {moves.map((move, index) => (
          <span 
            key={index}
            className={`move ${index === currentMoveIndex ? 'current' : ''} ${index < currentMoveIndex ? 'completed' : ''}`}
          >
            {move}
          </span>
        ))}
      </div>
    </div>
  );
};

export default SolutionPlayer;