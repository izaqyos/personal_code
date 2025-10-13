import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import ModeSelector, { TimerMode } from './ModeSelector';

describe('ModeSelector Component', () => {
  test('renders all mode buttons', () => {
    const mockOnModeChange = jest.fn();
    render(
      <ModeSelector 
        currentMode="work"
        onModeChange={mockOnModeChange}
      />
    );
    
    expect(screen.getByText('Work')).toBeInTheDocument();
    expect(screen.getByText('Short Break')).toBeInTheDocument();
    expect(screen.getByText('Long Break')).toBeInTheDocument();
  });
  
  test('applies active class to current mode button', () => {
    const mockOnModeChange = jest.fn();
    render(
      <ModeSelector 
        currentMode="work"
        onModeChange={mockOnModeChange}
      />
    );
    
    const workButton = screen.getByText('Work');
    const shortBreakButton = screen.getByText('Short Break');
    const longBreakButton = screen.getByText('Long Break');
    
    expect(workButton.className).toContain('active');
    expect(shortBreakButton.className).not.toContain('active');
    expect(longBreakButton.className).not.toContain('active');
  });
  
  test('clicking a mode button calls onModeChange with correct mode', () => {
    const mockOnModeChange = jest.fn();
    render(
      <ModeSelector 
        currentMode="work"
        onModeChange={mockOnModeChange}
      />
    );
    
    const shortBreakButton = screen.getByText('Short Break');
    fireEvent.click(shortBreakButton);
    
    expect(mockOnModeChange).toHaveBeenCalledWith('shortBreak');
  });
  
  test('changes active button when currentMode changes', () => {
    const mockOnModeChange = jest.fn();
    const { rerender } = render(
      <ModeSelector 
        currentMode="work"
        onModeChange={mockOnModeChange}
      />
    );
    
    // Initially work is active
    expect(screen.getByText('Work').className).toContain('active');
    
    // Change to short break
    rerender(
      <ModeSelector 
        currentMode="shortBreak"
        onModeChange={mockOnModeChange}
      />
    );
    
    // Now short break should be active
    expect(screen.getByText('Work').className).not.toContain('active');
    expect(screen.getByText('Short Break').className).toContain('active');
    expect(screen.getByText('Long Break').className).not.toContain('active');
  });
}); 