import React from 'react';

export type TimerMode = 'work' | 'shortBreak' | 'longBreak';

interface ModeSelectorProps {
  currentMode: TimerMode;
  onModeChange: (mode: TimerMode) => void;
}

const ModeSelector: React.FC<ModeSelectorProps> = ({ currentMode, onModeChange }) => {
  return (
    <div className="mode-selector">
      <button 
        className={`mode-button ${currentMode === 'work' ? 'active' : ''}`}
        onClick={() => onModeChange('work')}
      >
        Work
      </button>
      <button 
        className={`mode-button ${currentMode === 'shortBreak' ? 'active' : ''}`}
        onClick={() => onModeChange('shortBreak')}
      >
        Short Break
      </button>
      <button 
        className={`mode-button ${currentMode === 'longBreak' ? 'active' : ''}`}
        onClick={() => onModeChange('longBreak')}
      >
        Long Break
      </button>
    </div>
  );
};

export default ModeSelector; 