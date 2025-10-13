
import * as THREE from 'three';

const CUBIE_SIZE = 1;
const CUBIE_SPACING = 0.1;

const COLORS = {
  FRONT: 'blue',
  BACK: 'green',
  UP: 'white',
  DOWN: 'yellow',
  LEFT: 'orange',
  RIGHT: 'red',
};

class Cube {
  constructor(scene) {
    this.scene = scene;
    this.cubies = [];
    this.pivot = new THREE.Object3D();
    this.scene.add(this.pivot);
    this.init();
  }

  init() {
    for (let x = -1; x <= 1; x++) {
      for (let y = -1; y <= 1; y++) {
        for (let z = -1; z <= 1; z++) {
          if (x === 0 && y === 0 && z === 0) continue;
          const cubie = this.createCubie(x, y, z);
          this.cubies.push(cubie);
          this.scene.add(cubie);
        }
      }
    }
  }

  createCubie(x, y, z) {
    const geometry = new THREE.BoxGeometry(CUBIE_SIZE, CUBIE_SIZE, CUBIE_SIZE);
    const materials = [
      new THREE.MeshBasicMaterial({ color: x === 1 ? COLORS.RIGHT : 0x1a1a1a }),
      new THREE.MeshBasicMaterial({ color: x === -1 ? COLORS.LEFT : 0x1a1a1a }),
      new THREE.MeshBasicMaterial({ color: y === 1 ? COLORS.UP : 0x1a1a1a }),
      new THREE.MeshBasicMaterial({ color: y === -1 ? COLORS.DOWN : 0x1a1a1a }),
      new THREE.MeshBasicMaterial({ color: z === 1 ? COLORS.FRONT : 0x1a1a1a }),
      new THREE.MeshBasicMaterial({ color: z === -1 ? COLORS.BACK : 0x1a1a1a }),
    ];
    const cubie = new THREE.Mesh(geometry, materials);
    cubie.position.set(
      x * (CUBIE_SIZE + CUBIE_SPACING),
      y * (CUBIE_SIZE + CUBIE_SPACING),
      z * (CUBIE_SIZE + CUBIE_SPACING)
    );
    cubie.userData = { x, y, z };
    return cubie;
  }

  rotateLayer(axis, layer, angle) {
    this.pivot.rotation.set(0, 0, 0);
    this.pivot.updateMatrixWorld(true);

    const cubiesToRotate = this.cubies.filter(cubie => {
      return Math.abs(cubie.userData[axis] - layer) < 0.1;
    });

    cubiesToRotate.forEach(cubie => {
      this.pivot.attach(cubie);
    });

    if (axis === 'x') this.pivot.rotation.x = angle;
    if (axis === 'y') this.pivot.rotation.y = angle;
    if (axis === 'z') this.pivot.rotation.z = angle;

    this.pivot.updateMatrixWorld(true);

    cubiesToRotate.forEach(cubie => {
      this.scene.attach(cubie);
      this.updateCubieLogicalState(cubie, axis, angle);
    });
  }

  updateCubieLogicalState(cubie, axis, angle) {
    const { x, y, z } = cubie.userData;
    const direction = Math.sign(angle);

    if (axis === 'y') {
      cubie.userData.x = direction * z;
      cubie.userData.z = -direction * x;
    } else if (axis === 'x') {
      cubie.userData.y = -direction * z;
      cubie.userData.z = direction * y;
    } else if (axis === 'z') {
      cubie.userData.x = -direction * y;
      cubie.userData.y = direction * x;
    }
  }

  scramble() {
    const moves = [
      { axis: 'x', layer: 1 }, { axis: 'x', layer: -1 },
      { axis: 'y', layer: 1 }, { axis: 'y', layer: -1 },
      { axis: 'z', layer: 1 }, { axis: 'z', layer: -1 },
    ];

    for (let i = 0; i < 30; i++) {
        const move = moves[Math.floor(Math.random() * moves.length)];
        const angle = (Math.random() < 0.5 ? 1 : -1) * Math.PI / 2;
        this.rotateLayer(move.axis, move.layer, angle);
    }
  }
}

export default Cube;
