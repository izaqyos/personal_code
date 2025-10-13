import React, { useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls } from '@react-three/drei';
import { Group, Mesh } from 'three';
import { CubeState, CubeColor } from '../types/cube';

interface CubieProps {
  position: [number, number, number];
  colors: { [key: string]: CubeColor };
}

const colorMap = {
  white: '#ffffff',
  yellow: '#ffff00',
  red: '#ff0000',
  orange: '#ff8800',
  blue: '#0066ff',
  green: '#00ff00',
  black: '#000000'
};

const Cubie: React.FC<CubieProps> = ({ position, colors }) => {
  const meshRef = useRef<Mesh>(null);
  
  return (
    <group position={position}>
      <mesh ref={meshRef}>
        <boxGeometry args={[0.95, 0.95, 0.95]} />
        <meshStandardMaterial color="#222" />
      </mesh>
      
      {/* Face stickers */}
      {colors.front && (
        <mesh position={[0, 0, 0.48]}>
          <planeGeometry args={[0.8, 0.8]} />
          <meshStandardMaterial color={colorMap[colors.front]} />
        </mesh>
      )}
      
      {colors.back && (
        <mesh position={[0, 0, -0.48]} rotation={[0, Math.PI, 0]}>
          <planeGeometry args={[0.8, 0.8]} />
          <meshStandardMaterial color={colorMap[colors.back]} />
        </mesh>
      )}
      
      {colors.right && (
        <mesh position={[0.48, 0, 0]} rotation={[0, Math.PI/2, 0]}>
          <planeGeometry args={[0.8, 0.8]} />
          <meshStandardMaterial color={colorMap[colors.right]} />
        </mesh>
      )}
      
      {colors.left && (
        <mesh position={[-0.48, 0, 0]} rotation={[0, -Math.PI/2, 0]}>
          <planeGeometry args={[0.8, 0.8]} />
          <meshStandardMaterial color={colorMap[colors.left]} />
        </mesh>
      )}
      
      {colors.top && (
        <mesh position={[0, 0.48, 0]} rotation={[-Math.PI/2, 0, 0]}>
          <planeGeometry args={[0.8, 0.8]} />
          <meshStandardMaterial color={colorMap[colors.top]} />
        </mesh>
      )}
      
      {colors.bottom && (
        <mesh position={[0, -0.48, 0]} rotation={[Math.PI/2, 0, 0]}>
          <planeGeometry args={[0.8, 0.8]} />
          <meshStandardMaterial color={colorMap[colors.bottom]} />
        </mesh>
      )}
    </group>
  );
};

interface RubiksCube3DProps {
  cube: CubeState;
  isAnimating: boolean;
  rotationAnimation?: {
    axis: string;
    angle: number;
    layer: number;
  };
}

const RubiksCube3D: React.FC<RubiksCube3DProps> = ({ cube, isAnimating, rotationAnimation }) => {
  const cubeRef = useRef<Group>(null);
  
  useFrame(() => {
    if (cubeRef.current && !isAnimating) {
      cubeRef.current.rotation.y += 0.005;
    }
  });

  const getCubieColors = (x: number, y: number, z: number) => {
    const colors: { [key: string]: CubeColor } = {};
    
    // Map 3D position to 2D face coordinates
    if (z === 1) colors.front = cube.front.squares[1-y][x+1];
    if (z === -1) colors.back = cube.back.squares[1-y][1-x];
    if (x === 1) colors.right = cube.right.squares[1-y][1-z];
    if (x === -1) colors.left = cube.left.squares[1-y][z+1];
    if (y === 1) colors.top = cube.top.squares[1-z][x+1];
    if (y === -1) colors.bottom = cube.bottom.squares[z+1][x+1];
    
    return colors;
  };

  const cubies = [];
  for (let x = -1; x <= 1; x++) {
    for (let y = -1; y <= 1; y++) {
      for (let z = -1; z <= 1; z++) {
        const colors = getCubieColors(x, y, z);
        cubies.push(
          <Cubie
            key={`${x}-${y}-${z}`}
            position={[x, y, z]}
            colors={colors}
          />
        );
      }
    }
  }

  return (
    <group ref={cubeRef}>
      {cubies}
    </group>
  );
};

interface Cube3DProps {
  cube: CubeState;
  isAnimating?: boolean;
}

const Cube3D: React.FC<Cube3DProps> = ({ cube, isAnimating = false }) => {
  return (
    <div style={{ width: '100%', height: '500px' }}>
      <Canvas camera={{ position: [5, 5, 5], fov: 75 }}>
        <ambientLight intensity={0.4} />
        <directionalLight position={[10, 10, 5]} intensity={1} />
        <directionalLight position={[-10, -10, -5]} intensity={0.5} />
        
        <RubiksCube3D cube={cube} isAnimating={isAnimating} />
        
        <OrbitControls
          enablePan={false}
          enableZoom={true}
          enableRotate={true}
          autoRotate={false}
          maxDistance={10}
          minDistance={3}
        />
      </Canvas>
    </div>
  );
};

export default Cube3D;