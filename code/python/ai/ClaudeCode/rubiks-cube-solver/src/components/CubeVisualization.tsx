import React from 'react';
import { CubeState, CubeFace } from '../types/cube';
import './CubeVisualization.css';

interface CubeVisualizationProps {
  cube: CubeState;
}

const Face: React.FC<{ face: CubeFace; className: string }> = ({ face, className }) => (
  <div className={`cube-face ${className}`}>
    {face.squares.map((row, i) => (
      <div key={i} className="cube-row">
        {row.map((color, j) => (
          <div key={j} className={`cube-square ${color}`} />
        ))}
      </div>
    ))}
  </div>
);

const CubeVisualization: React.FC<CubeVisualizationProps> = ({ cube }) => {
  return (
    <div className="cube-container">
      <div className="cube-net">
        <div className="cube-net-row">
          <div className="cube-net-space"></div>
          <Face face={cube.top} className="top" />
          <div className="cube-net-space"></div>
          <div className="cube-net-space"></div>
        </div>
        <div className="cube-net-row">
          <Face face={cube.left} className="left" />
          <Face face={cube.front} className="front" />
          <Face face={cube.right} className="right" />
          <Face face={cube.back} className="back" />
        </div>
        <div className="cube-net-row">
          <div className="cube-net-space"></div>
          <Face face={cube.bottom} className="bottom" />
          <div className="cube-net-space"></div>
          <div className="cube-net-space"></div>
        </div>
      </div>
    </div>
  );
};

export default CubeVisualization;