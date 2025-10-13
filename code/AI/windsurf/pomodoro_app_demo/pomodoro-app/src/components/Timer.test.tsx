import React from 'react';
import { render, screen } from '@testing-library/react';
import Timer from './Timer';

describe('Timer Component', () => {
  test('renders timer with correct initial time', () => {
    const mockOnComplete = jest.fn();
    render(
      <Timer 
        initialMinutes={25} 
        onTimerComplete={mockOnComplete} 
        isActive={false} 
      />
    );
    
    const timerDisplay = screen.getByText('25:00');
    expect(timerDisplay).toBeInTheDocument();
  });
  
  test('renders timer with different initial time', () => {
    const mockOnComplete = jest.fn();
    render(
      <Timer 
        initialMinutes={5} 
        onTimerComplete={mockOnComplete} 
        isActive={false} 
      />
    );
    
    const timerDisplay = screen.getByText('05:00');
    expect(timerDisplay).toBeInTheDocument();
  });
  
  test('updates timer when initialMinutes changes', () => {
    const mockOnComplete = jest.fn();
    const { rerender } = render(
      <Timer 
        initialMinutes={25} 
        onTimerComplete={mockOnComplete} 
        isActive={false} 
      />
    );
    
    // Verify initial time
    expect(screen.getByText('25:00')).toBeInTheDocument();
    
    // Change initialMinutes
    rerender(
      <Timer 
        initialMinutes={10} 
        onTimerComplete={mockOnComplete} 
        isActive={false} 
      />
    );
    
    // Verify updated time
    expect(screen.getByText('10:00')).toBeInTheDocument();
  });
}); 