import React, { useState, useEffect } from 'react';

interface TimerProps {
  initialMinutes: number;
  onTimerComplete: () => void;
  isActive: boolean;
}

const Timer: React.FC<TimerProps> = ({ initialMinutes, onTimerComplete, isActive }) => {
  const [seconds, setSeconds] = useState(initialMinutes * 60);
  
  useEffect(() => {
    setSeconds(initialMinutes * 60);
  }, [initialMinutes]);

  useEffect(() => {
    let interval: NodeJS.Timeout | null = null;
    
    if (isActive && seconds > 0) {
      interval = setInterval(() => {
        setSeconds(seconds => seconds - 1);
      }, 1000);
    } else if (seconds === 0) {
      onTimerComplete();
    }
    
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [isActive, seconds, onTimerComplete]);
  
  const formatTime = (timeInSeconds: number): string => {
    const minutes = Math.floor(timeInSeconds / 60);
    const seconds = timeInSeconds % 60;
    return `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
  };
  
  return (
    <div className="timer">
      <h2 className="timer-display">{formatTime(seconds)}</h2>
    </div>
  );
};

export default Timer; 