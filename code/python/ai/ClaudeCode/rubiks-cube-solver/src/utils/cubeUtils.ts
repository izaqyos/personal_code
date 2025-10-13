import { CubeState, CubeFace, CubeColor, Move } from '../types/cube';
import { applyMove } from './cubeRotations';

export const createSolvedCube = (): CubeState => {
  const createFace = (color: CubeColor): CubeFace => ({
    squares: Array(3).fill(null).map(() => Array(3).fill(color))
  });

  return {
    front: createFace('red'),
    back: createFace('orange'),
    left: createFace('blue'),
    right: createFace('green'),
    top: createFace('white'),
    bottom: createFace('yellow')
  };
};

export const scrambleCube = (cube: CubeState): CubeState => {
  let newCube = JSON.parse(JSON.stringify(cube));
  
  // Create a proper scramble by applying random moves
  const moves: Move[] = ['R', 'L', 'U', 'D', 'F', 'B', 'R\'', 'L\'', 'U\'', 'D\'', 'F\'', 'B\'', 'R2', 'L2', 'U2', 'D2', 'F2', 'B2'];
  const numMoves = 20 + Math.floor(Math.random() * 10); // 20-30 moves
  
  for (let i = 0; i < numMoves; i++) {
    const randomMove = moves[Math.floor(Math.random() * moves.length)];
    newCube = applyMove(newCube, randomMove);
  }
  
  return newCube;
};

export const isSolved = (cube: CubeState): boolean => {
  const faces = ['front', 'back', 'left', 'right', 'top', 'bottom'] as const;
  
  return faces.every(faceKey => {
    const face = cube[faceKey];
    const firstColor = face.squares[0][0];
    return face.squares.every(row => 
      row.every(square => square === firstColor)
    );
  });
};