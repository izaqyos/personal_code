import { CubeState, Move } from '../types/cube';

export const applyMove = (cube: CubeState, move: Move): CubeState => {
  const newCube = JSON.parse(JSON.stringify(cube));
  
  switch (move) {
    case 'R':
      return rotateRight(newCube);
    case 'R\'':
      return rotateRight(rotateRight(rotateRight(newCube)));
    case 'R2':
      return rotateRight(rotateRight(newCube));
    case 'L':
      return rotateLeft(newCube);
    case 'L\'':
      return rotateLeft(rotateLeft(rotateLeft(newCube)));
    case 'L2':
      return rotateLeft(rotateLeft(newCube));
    case 'U':
      return rotateUp(newCube);
    case 'U\'':
      return rotateUp(rotateUp(rotateUp(newCube)));
    case 'U2':
      return rotateUp(rotateUp(newCube));
    case 'D':
      return rotateDown(newCube);
    case 'D\'':
      return rotateDown(rotateDown(rotateDown(newCube)));
    case 'D2':
      return rotateDown(rotateDown(newCube));
    case 'F':
      return rotateFront(newCube);
    case 'F\'':
      return rotateFront(rotateFront(rotateFront(newCube)));
    case 'F2':
      return rotateFront(rotateFront(newCube));
    case 'B':
      return rotateBack(newCube);
    case 'B\'':
      return rotateBack(rotateBack(rotateBack(newCube)));
    case 'B2':
      return rotateBack(rotateBack(newCube));
    default:
      return newCube;
  }
};

const rotateFaceClockwise = (face: any) => {
  const temp = face.squares[0][0];
  face.squares[0][0] = face.squares[2][0];
  face.squares[2][0] = face.squares[2][2];
  face.squares[2][2] = face.squares[0][2];
  face.squares[0][2] = temp;
  
  const temp2 = face.squares[0][1];
  face.squares[0][1] = face.squares[1][0];
  face.squares[1][0] = face.squares[2][1];
  face.squares[2][1] = face.squares[1][2];
  face.squares[1][2] = temp2;
};

const rotateRight = (cube: CubeState): CubeState => {
  rotateFaceClockwise(cube.right);
  
  // Rotate adjacent faces
  const temp = [cube.front.squares[0][2], cube.front.squares[1][2], cube.front.squares[2][2]];
  cube.front.squares[0][2] = cube.bottom.squares[0][2];
  cube.front.squares[1][2] = cube.bottom.squares[1][2];
  cube.front.squares[2][2] = cube.bottom.squares[2][2];
  
  cube.bottom.squares[0][2] = cube.back.squares[2][0];
  cube.bottom.squares[1][2] = cube.back.squares[1][0];
  cube.bottom.squares[2][2] = cube.back.squares[0][0];
  
  cube.back.squares[0][0] = cube.top.squares[2][2];
  cube.back.squares[1][0] = cube.top.squares[1][2];
  cube.back.squares[2][0] = cube.top.squares[0][2];
  
  cube.top.squares[0][2] = temp[0];
  cube.top.squares[1][2] = temp[1];
  cube.top.squares[2][2] = temp[2];
  
  return cube;
};

const rotateLeft = (cube: CubeState): CubeState => {
  rotateFaceClockwise(cube.left);
  
  const temp = [cube.front.squares[0][0], cube.front.squares[1][0], cube.front.squares[2][0]];
  cube.front.squares[0][0] = cube.top.squares[0][0];
  cube.front.squares[1][0] = cube.top.squares[1][0];
  cube.front.squares[2][0] = cube.top.squares[2][0];
  
  cube.top.squares[0][0] = cube.back.squares[2][2];
  cube.top.squares[1][0] = cube.back.squares[1][2];
  cube.top.squares[2][0] = cube.back.squares[0][2];
  
  cube.back.squares[0][2] = cube.bottom.squares[2][0];
  cube.back.squares[1][2] = cube.bottom.squares[1][0];
  cube.back.squares[2][2] = cube.bottom.squares[0][0];
  
  cube.bottom.squares[0][0] = temp[0];
  cube.bottom.squares[1][0] = temp[1];
  cube.bottom.squares[2][0] = temp[2];
  
  return cube;
};

const rotateUp = (cube: CubeState): CubeState => {
  rotateFaceClockwise(cube.top);
  
  const temp = [cube.front.squares[0][0], cube.front.squares[0][1], cube.front.squares[0][2]];
  cube.front.squares[0] = [...cube.right.squares[0]];
  cube.right.squares[0] = [...cube.back.squares[0]];
  cube.back.squares[0] = [...cube.left.squares[0]];
  cube.left.squares[0] = [...temp];
  
  return cube;
};

const rotateDown = (cube: CubeState): CubeState => {
  rotateFaceClockwise(cube.bottom);
  
  const temp = [cube.front.squares[2][0], cube.front.squares[2][1], cube.front.squares[2][2]];
  cube.front.squares[2] = [...cube.left.squares[2]];
  cube.left.squares[2] = [...cube.back.squares[2]];
  cube.back.squares[2] = [...cube.right.squares[2]];
  cube.right.squares[2] = [...temp];
  
  return cube;
};

const rotateFront = (cube: CubeState): CubeState => {
  rotateFaceClockwise(cube.front);
  
  const temp = [cube.top.squares[2][0], cube.top.squares[2][1], cube.top.squares[2][2]];
  cube.top.squares[2][0] = cube.left.squares[2][2];
  cube.top.squares[2][1] = cube.left.squares[1][2];
  cube.top.squares[2][2] = cube.left.squares[0][2];
  
  cube.left.squares[0][2] = cube.bottom.squares[0][0];
  cube.left.squares[1][2] = cube.bottom.squares[0][1];
  cube.left.squares[2][2] = cube.bottom.squares[0][2];
  
  cube.bottom.squares[0][0] = cube.right.squares[2][0];
  cube.bottom.squares[0][1] = cube.right.squares[1][0];
  cube.bottom.squares[0][2] = cube.right.squares[0][0];
  
  cube.right.squares[0][0] = temp[0];
  cube.right.squares[1][0] = temp[1];
  cube.right.squares[2][0] = temp[2];
  
  return cube;
};

const rotateBack = (cube: CubeState): CubeState => {
  rotateFaceClockwise(cube.back);
  
  const temp = [cube.top.squares[0][0], cube.top.squares[0][1], cube.top.squares[0][2]];
  cube.top.squares[0][0] = cube.right.squares[0][2];
  cube.top.squares[0][1] = cube.right.squares[1][2];
  cube.top.squares[0][2] = cube.right.squares[2][2];
  
  cube.right.squares[0][2] = cube.bottom.squares[2][2];
  cube.right.squares[1][2] = cube.bottom.squares[2][1];
  cube.right.squares[2][2] = cube.bottom.squares[2][0];
  
  cube.bottom.squares[2][0] = cube.left.squares[2][0];
  cube.bottom.squares[2][1] = cube.left.squares[1][0];
  cube.bottom.squares[2][2] = cube.left.squares[0][0];
  
  cube.left.squares[0][0] = temp[2];
  cube.left.squares[1][0] = temp[1];
  cube.left.squares[2][0] = temp[0];
  
  return cube;
};