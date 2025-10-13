import React, { useState, useEffect } from 'react';
import Timer from './Timer';
import Controls from './Controls';
import ModeSelector, { TimerMode } from './ModeSelector';
import './PomodoroApp.css';

const PomodoroApp: React.FC = () => {
  const [isActive, setIsActive] = useState(false);
  const [mode, setMode] = useState<TimerMode>('work');
  const [completedPomodoros, setCompletedPomodoros] = useState(0);
  
  // Default timer durations
  const durations = {
    work: 25,
    shortBreak: 5,
    longBreak: 15
  };
  
  // Reset timer when changing modes
  useEffect(() => {
    setIsActive(false);
  }, [mode]);
  
  const handleStart = () => {
    setIsActive(true);
  };
  
  const handlePause = () => {
    setIsActive(false);
  };
  
  const handleReset = () => {
    setIsActive(false);
  };
  
  const handleModeChange = (newMode: TimerMode) => {
    setMode(newMode);
  };
  
  const handleTimerComplete = () => {
    // Play a sound notification
    const audio = new Audio('/notification.mp3');
    audio.play().catch(error => console.error('Error playing notification:', error));
    
    setIsActive(false);
    
    // Auto-switch to the next appropriate mode
    if (mode === 'work') {
      setCompletedPomodoros(prev => prev + 1);
      // After 4 pomodoros, take a long break
      if ((completedPomodoros + 1) % 4 === 0) {
        setMode('longBreak');
      } else {
        setMode('shortBreak');
      }
    } else {
      setMode('work');
    }
  };
  
  return (
    <div className="pomodoro-app">
      <h1>Pomodoro Timer</h1>
      
      <div className="pomodoro-counter">
        Completed Pomodoros: {completedPomodoros}
      </div>
      
      <ModeSelector currentMode={mode} onModeChange={handleModeChange} />
      
      <Timer 
        initialMinutes={durations[mode]} 
        onTimerComplete={handleTimerComplete} 
        isActive={isActive} 
      />
      
      <Controls 
        isActive={isActive}
        onStart={handleStart}
        onPause={handlePause}
        onReset={handleReset}
      />
    </div>
  );
};

export default PomodoroApp; 