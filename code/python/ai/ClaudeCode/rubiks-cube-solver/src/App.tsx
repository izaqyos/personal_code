import React, { useState } from 'react';
import './App.css';
import CubeVisualization from './components/CubeVisualization';
import Cube3D from './components/Cube3D';
import SolutionPlayer from './components/SolutionPlayer';
import { CubeState, Solution, Move } from './types/cube';
import { createSolvedCube, scrambleCube, isSolved } from './utils/cubeUtils';
import { ImprovedSolver } from './algorithms/improvedSolver';
import { applyMove } from './utils/cubeRotations';
import './components/SolutionPlayer.css';

function App() {
  const [cube, setCube] = useState<CubeState>(createSolvedCube());
  const [solution, setSolution] = useState<Solution | null>(null);
  const [isScrambled, setIsScrambled] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  const [use3D, setUse3D] = useState(true);

  const handleScramble = () => {
    const scrambled = scrambleCube(cube);
    setCube(scrambled);
    setSolution(null);
    setIsScrambled(true);
    setIsPlaying(false);
  };

  const handleSolve = () => {
    const solver = new ImprovedSolver(cube);
    const solutionResult = solver.solve();
    setSolution(solutionResult);
  };

  const handleReset = () => {
    setCube(createSolvedCube());
    setSolution(null);
    setIsScrambled(false);
    setIsPlaying(false);
  };

  const handleMoveApplied = (move: Move) => {
    setCube(prevCube => applyMove(prevCube, move));
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Rubik's Cube Solver</h1>
        <div className="status">
          {isSolved(cube) ? (
            <span className="solved">✓ Solved</span>
          ) : (
            <span className="unsolved">⚠ Unsolved</span>
          )}
        </div>
      </header>
      
      <main className="App-main">
        <div className="view-toggle">
          <button 
            onClick={() => setUse3D(false)} 
            className={!use3D ? 'active' : ''}
          >
            2D View
          </button>
          <button 
            onClick={() => setUse3D(true)} 
            className={use3D ? 'active' : ''}
          >
            3D View
          </button>
        </div>

        {use3D ? (
          <Cube3D cube={cube} isAnimating={isPlaying} />
        ) : (
          <CubeVisualization cube={cube} />
        )}
        
        <div className="controls">
          <button onClick={handleScramble} disabled={isPlaying}>
            Scramble
          </button>
          <button onClick={handleSolve} disabled={!isScrambled || isPlaying}>
            Solve
          </button>
          <button onClick={handleReset} disabled={isPlaying}>
            Reset
          </button>
        </div>
        
        {solution && (
          <SolutionPlayer
            moves={solution.moves}
            onMoveApplied={handleMoveApplied}
            isPlaying={isPlaying}
            onPlayingChange={setIsPlaying}
          />
        )}
      </main>
    </div>
  );
}

export default App;
