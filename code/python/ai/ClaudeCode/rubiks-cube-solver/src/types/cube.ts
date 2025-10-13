export type CubeColor = 'white' | 'yellow' | 'red' | 'orange' | 'blue' | 'green';

export interface CubeFace {
  squares: CubeColor[][];
}

export interface CubeState {
  front: CubeFace;
  back: CubeFace;
  left: CubeFace;
  right: CubeFace;
  top: CubeFace;
  bottom: CubeFace;
}

export type Move = 'R' | 'L' | 'U' | 'D' | 'F' | 'B' | 'R\'' | 'L\'' | 'U\'' | 'D\'' | 'F\'' | 'B\'' | 'R2' | 'L2' | 'U2' | 'D2' | 'F2' | 'B2';

export interface Solution {
  moves: Move[];
  description: string;
}