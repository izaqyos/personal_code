import React from 'react';

interface ControlsProps {
  isActive: boolean;
  onStart: () => void;
  onPause: () => void;
  onReset: () => void;
}

const Controls: React.FC<ControlsProps> = ({ isActive, onStart, onPause, onReset }) => {
  return (
    <div className="controls">
      {!isActive ? (
        <button className="control-button start" onClick={onStart}>
          Start
        </button>
      ) : (
        <button className="control-button pause" onClick={onPause}>
          Pause
        </button>
      )}
      <button className="control-button reset" onClick={onReset}>
        Reset
      </button>
    </div>
  );
};

export default Controls; 