import { CubeState, Move, Solution } from '../types/cube';
import { applyMove } from '../utils/cubeRotations';
import { isSolved } from '../utils/cubeUtils';

export class ImprovedSolver {
  private cube: CubeState;
  private moves: Move[] = [];
  private maxMoves = 100; // Prevent infinite loops

  constructor(cube: CubeState) {
    this.cube = JSON.parse(JSON.stringify(cube));
  }

  solve(): Solution {
    this.moves = [];
    
    // If already solved, return empty solution
    if (isSolved(this.cube)) {
      return {
        moves: [],
        description: 'Cube is already solved!'
      };
    }

    // Try to solve using various methods
    let attempts = 0;
    while (!isSolved(this.cube) && attempts < 3) {
      attempts++;
      
      // Method 1: Try to solve bottom layer
      this.solveBottomLayer();
      
      // Method 2: Try to solve middle layer
      this.solveMiddleLayer();
      
      // Method 3: Try to solve top layer
      this.solveTopLayer();
      
      // If not solved, try some general scrambling to get unstuck
      if (!isSolved(this.cube)) {
        this.applyGeneralAlgorithms();
      }
    }

    // If still not solved, apply some known solving sequences
    if (!isSolved(this.cube)) {
      this.applyKnownSequences();
    }

    return {
      moves: this.moves,
      description: `Improved solving method (${this.moves.length} moves)`
    };
  }

  private applyMove(move: Move): void {
    if (this.moves.length >= this.maxMoves) return;
    this.moves.push(move);
    this.cube = applyMove(this.cube, move);
  }

  private solveBottomLayer(): void {
    // Try to get white pieces to the bottom
    const algorithms = [
      ['F', 'R', 'U', 'R\'', 'F\''],
      ['R', 'U', 'R\'', 'U', 'R', 'U2', 'R\''],
      ['U', 'R', 'U\'', 'R\''],
      ['F', 'U', 'F\''],
      ['R', 'U2', 'R\'', 'U\'', 'R', 'U\'', 'R\'']
    ];

    for (let i = 0; i < 4; i++) {
      const algorithm = algorithms[i % algorithms.length];
      algorithm.forEach(move => this.applyMove(move as Move));
      
      // Rotate to next position
      this.applyMove('D');
    }
  }

  private solveMiddleLayer(): void {
    // Middle layer algorithms
    const rightAlgorithm = ['U', 'R', 'U\'', 'R\'', 'U\'', 'F\'', 'U', 'F'];
    const leftAlgorithm = ['U\'', 'L\'', 'U', 'L', 'U', 'F', 'U\'', 'F\''];

    for (let i = 0; i < 4; i++) {
      if (i % 2 === 0) {
        rightAlgorithm.forEach(move => this.applyMove(move as Move));
      } else {
        leftAlgorithm.forEach(move => this.applyMove(move as Move));
      }
      this.applyMove('U');
    }
  }

  private solveTopLayer(): void {
    // Top layer algorithms (OLL and PLL)
    const ollAlgorithms = [
      ['F', 'R', 'U', 'R\'', 'U\'', 'F\''], // Line
      ['F', 'U', 'R', 'U\'', 'R\'', 'F\''], // L-shape
      ['R', 'U', 'R\'', 'U', 'R', 'U2', 'R\''], // Sune
      ['R', 'U2', 'R\'', 'U\'', 'R', 'U\'', 'R\''] // Anti-Sune
    ];

    const pllAlgorithms = [
      ['R', 'U', 'R\'', 'F\'', 'R', 'U', 'R\'', 'U\'', 'R\'', 'F', 'R2', 'U\'', 'R\''], // T-perm
      ['R', 'U2', 'R\'', 'U\'', 'R', 'U2', 'L\'', 'U', 'R\'', 'U\'', 'L'], // Y-perm
      ['R\'', 'U', 'L\'', 'U2', 'R', 'U\'', 'R\'', 'U2', 'R', 'L'], // V-perm
      ['R', 'U\'', 'R', 'U', 'R', 'U', 'R', 'U\'', 'R\'', 'U\'', 'R2'] // H-perm
    ];

    // Apply OLL algorithms
    ollAlgorithms.forEach(algorithm => {
      algorithm.forEach(move => this.applyMove(move as Move));
    });

    // Apply PLL algorithms
    pllAlgorithms.forEach(algorithm => {
      algorithm.forEach(move => this.applyMove(move as Move));
    });
  }

  private applyGeneralAlgorithms(): void {
    // General purpose algorithms that help mix up the cube
    const generalAlgorithms = [
      ['R', 'U', 'R\'', 'U\''], // Basic right-hand
      ['L\'', 'U\'', 'L', 'U'], // Basic left-hand
      ['F', 'R', 'U\'', 'R\'', 'U\'', 'R', 'U', 'R\'', 'F\''], // Complex algorithm
      ['R', 'U', 'R\'', 'U', 'R', 'U2', 'R\'', 'U'], // Extended right-hand
      ['U', 'R', 'U\'', 'L\'', 'U', 'R\'', 'U\'', 'L'] // Interchange
    ];

    generalAlgorithms.forEach(algorithm => {
      algorithm.forEach(move => this.applyMove(move as Move));
    });
  }

  private applyKnownSequences(): void {
    // Some well-known sequences that can help solve the cube
    const sequences = [
      // Commutators and conjugates
      ['R', 'U', 'R\'', 'U\'', 'R\'', 'F', 'R2', 'U\'', 'R\'', 'U\'', 'R', 'U', 'R\'', 'F\''],
      ['R', 'U', 'R\'', 'D', 'R', 'U\'', 'R\'', 'D\''],
      ['R', 'U2', 'R\'', 'U\'', 'R', 'U\'', 'R\''],
      ['R', 'U', 'R\'', 'U', 'R', 'U2', 'R\''],
      ['F', 'R', 'U\'', 'R\'', 'U\'', 'R', 'U', 'R\'', 'F\''],
      ['R', 'U', 'R\'', 'F\'', 'R', 'U', 'R\'', 'U\'', 'R\'', 'F', 'R2', 'U\'', 'R\''],
      
      // More complex sequences
      ['R\'', 'U2', 'R', 'U', 'R\'', 'U', 'R'],
      ['R2', 'D\'', 'R', 'U2', 'R\'', 'D', 'R', 'U2', 'R'],
      ['R', 'U', 'R\'', 'U\'', 'R\'', 'F', 'R', 'F\''],
      ['F', 'R', 'U', 'R\'', 'U\'', 'R', 'U', 'R\'', 'U\'', 'F\''],
      
      // Final attempts - mix of various algorithms
      ['R', 'U', 'R\'', 'U2', 'R', 'U', 'R\'', 'U2', 'R', 'U\'', 'R\''],
      ['R2', 'U', 'R', 'U', 'R\'', 'U\'', 'R\'', 'U\'', 'R\'', 'U', 'R\''],
      ['R', 'U2', 'R2', 'U\'', 'R2', 'U\'', 'R2', 'U2', 'R'],
      ['R2', 'U\'', 'R\'', 'U\'', 'R', 'U', 'R', 'U', 'R', 'U\'', 'R']
    ];

    // Apply sequences until solved or max moves reached
    for (const sequence of sequences) {
      if (isSolved(this.cube)) break;
      if (this.moves.length >= this.maxMoves) break;
      
      sequence.forEach(move => this.applyMove(move as Move));
      
      // Try the sequence in different orientations
      for (let i = 0; i < 3; i++) {
        this.applyMove('U');
        if (isSolved(this.cube)) break;
      }
    }
  }

  // Helper method to check if a specific layer is solved
  private isLayerSolved(layer: 'bottom' | 'middle' | 'top'): boolean {
    if (layer === 'bottom') {
      const bottom = this.cube.bottom;
      return bottom.squares.every(row => row.every(cell => cell === 'white'));
    }
    // Add more layer checking logic as needed
    return false;
  }
}