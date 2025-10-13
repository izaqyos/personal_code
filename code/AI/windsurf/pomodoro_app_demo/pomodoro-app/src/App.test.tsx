import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

test('renders Pomodoro app', () => {
  render(<App />);
  const headingElement = screen.getByText(/Pomodoro Timer/i);
  expect(headingElement).toBeInTheDocument();
});
