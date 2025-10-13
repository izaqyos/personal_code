import React, { useRef, useEffect } from 'react';
import * as THREE from 'three';
import Cube from './Cube';
import Solver from './solver';
import './App.css';

function App() {
  const mountRef = useRef(null);
  const cubeRef = useRef(null);

  useEffect(() => {
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer({ antialias: true });

    renderer.setSize(window.innerWidth, window.innerHeight);
    mountRef.current.appendChild(renderer.domElement);

    const cube = new Cube(scene);
    cubeRef.current = cube;
    cube.scramble();

    camera.position.z = 5;

    const mouse = new THREE.Vector2();
    const previousMouse = new THREE.Vector2();
    let isDragging = false;
    let shiftPressed = false;

    const onKeyDown = (event) => {
      if (event.key === 'Shift') {
        shiftPressed = true;
      }
    };

    const onKeyUp = (event) => {
      if (event.key === 'Shift') {
        shiftPressed = false;
      }
    };

    const onMouseDown = (event) => {
      isDragging = true;
      mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
      mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
      previousMouse.copy(mouse);
    };

    const onMouseMove = (event) => {
      if (isDragging) {
        mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
        mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

        const deltaX = mouse.x - previousMouse.x;
        const deltaY = mouse.y - previousMouse.y;

        if (shiftPressed) {
          scene.rotation.z += (deltaX + deltaY) * 2;
        } else {
          scene.rotation.y += deltaX * 2;
          scene.rotation.x += deltaY * 2;
        }

        previousMouse.copy(mouse);
      }
    };

    const onMouseUp = () => {
      isDragging = false;
    };

    renderer.domElement.addEventListener('mousedown', onMouseDown);
    renderer.domElement.addEventListener('mousemove', onMouseMove);
    window.addEventListener('mouseup', onMouseUp);
    window.addEventListener('keydown', onKeyDown);
    window.addEventListener('keyup', onKeyUp);

    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.6);
    directionalLight.position.set(10, 20, 0);
    scene.add(directionalLight);

    const animate = function () {
      requestAnimationFrame(animate);
      if (!isDragging) {
        scene.rotation.x += 0.005;
        scene.rotation.y += 0.005;
      }
      renderer.render(scene, camera);
    };

    animate();

    const handleResize = () => {
        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth, window.innerHeight);
    }

    window.addEventListener('resize', handleResize);

    return () => {
      if (mountRef.current) {
        mountRef.current.removeChild(renderer.domElement);
      }
      renderer.domElement.removeEventListener('mousedown', onMouseDown);
      renderer.domElement.removeEventListener('mousemove', onMouseMove);
      window.removeEventListener('mouseup', onMouseUp);
      window.removeEventListener('resize', handleResize);
      window.removeEventListener('keydown', onKeyDown);
      window.removeEventListener('keyup', onKeyUp);
    };
  }, []);

  const handleScramble = () => {
    if (cubeRef.current) {
      cubeRef.current.scramble();
    }
  };

  const handleSolve = () => {
    if (cubeRef.current) {
      const solver = new Solver(cubeRef.current);
      const solution = solver.solve();
      console.log(solution);
    }
  };

  return (
    <div>
      <div ref={mountRef} />
      <div className="controls">
        <button onClick={handleScramble}>Scramble</button>
        <button onClick={handleSolve}>Solve</button>
      </div>
    </div>
  );
}

export default App;

