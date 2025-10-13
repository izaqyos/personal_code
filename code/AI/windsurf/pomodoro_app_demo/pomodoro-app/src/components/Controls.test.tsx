import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import Controls from './Controls';

describe('Controls Component', () => {
  test('renders Start button when not active', () => {
    const mockOnStart = jest.fn();
    const mockOnPause = jest.fn();
    const mockOnReset = jest.fn();
    
    render(
      <Controls 
        isActive={false}
        onStart={mockOnStart}
        onPause={mockOnPause}
        onReset={mockOnReset}
      />
    );
    
    const startButton = screen.getByText('Start');
    expect(startButton).toBeInTheDocument();
    expect(screen.queryByText('Pause')).not.toBeInTheDocument();
  });
  
  test('renders Pause button when active', () => {
    const mockOnStart = jest.fn();
    const mockOnPause = jest.fn();
    const mockOnReset = jest.fn();
    
    render(
      <Controls 
        isActive={true}
        onStart={mockOnStart}
        onPause={mockOnPause}
        onReset={mockOnReset}
      />
    );
    
    const pauseButton = screen.getByText('Pause');
    expect(pauseButton).toBeInTheDocument();
    expect(screen.queryByText('Start')).not.toBeInTheDocument();
  });
  
  test('clicking Start button calls onStart', () => {
    const mockOnStart = jest.fn();
    const mockOnPause = jest.fn();
    const mockOnReset = jest.fn();
    
    render(
      <Controls 
        isActive={false}
        onStart={mockOnStart}
        onPause={mockOnPause}
        onReset={mockOnReset}
      />
    );
    
    const startButton = screen.getByText('Start');
    fireEvent.click(startButton);
    expect(mockOnStart).toHaveBeenCalledTimes(1);
  });
  
  test('clicking Pause button calls onPause', () => {
    const mockOnStart = jest.fn();
    const mockOnPause = jest.fn();
    const mockOnReset = jest.fn();
    
    render(
      <Controls 
        isActive={true}
        onStart={mockOnStart}
        onPause={mockOnPause}
        onReset={mockOnReset}
      />
    );
    
    const pauseButton = screen.getByText('Pause');
    fireEvent.click(pauseButton);
    expect(mockOnPause).toHaveBeenCalledTimes(1);
  });
  
  test('clicking Reset button calls onReset', () => {
    const mockOnStart = jest.fn();
    const mockOnPause = jest.fn();
    const mockOnReset = jest.fn();
    
    render(
      <Controls 
        isActive={false}
        onStart={mockOnStart}
        onPause={mockOnPause}
        onReset={mockOnReset}
      />
    );
    
    const resetButton = screen.getByText('Reset');
    fireEvent.click(resetButton);
    expect(mockOnReset).toHaveBeenCalledTimes(1);
  });
}); 