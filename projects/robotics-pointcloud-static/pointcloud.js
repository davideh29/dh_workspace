import { generateSpherePoints } from './utils.js';

const defaultParams = {
  seed: 12345,
  numPoints: 5000,
  radius: 1,
  noise: 0.02,
  colorMode: 'single',
  rotate: true,
};

let THREERef;
let OrbitControlsRef;
let renderer;
let scene;
let camera;
let controls;
let geometry;
let material;
let pointCloud;
let containerEl;
let currentParams = { ...defaultParams };
let animationActive = false;

function ensureDependencies(deps) {
  if (deps?.THREE) {
    THREERef = deps.THREE;
  }
  if (deps?.OrbitControls) {
    OrbitControlsRef = deps.OrbitControls;
  }
  if (!THREERef || !OrbitControlsRef) {
    throw new Error('THREE and OrbitControls must be provided.');
  }
}

function handleResize() {
  if (!renderer || !camera || !containerEl) {
    return;
  }
  const width = containerEl.clientWidth || window.innerWidth || 1;
  const height = containerEl.clientHeight || window.innerHeight || 1;
  renderer.setSize(width, height);
  camera.aspect = width / height;
  camera.updateProjectionMatrix();
}

function updatePointCloud() {
  if (!geometry || !material || !THREERef) {
    return;
  }

  const { positions, colors, count } = generateSpherePoints({
    seed: currentParams.seed,
    n: currentParams.numPoints,
    R: currentParams.radius,
    noise: currentParams.noise,
    colorMode: currentParams.colorMode,
  });

  geometry.setAttribute(
    'position',
    new THREERef.BufferAttribute(positions, 3)
  );
  geometry.setAttribute(
    'color',
    new THREERef.BufferAttribute(colors, 3, true)
  );
  geometry.setDrawRange(0, count);
  geometry.computeBoundingSphere();

  material.size = Math.max(0.0005, 0.01 * Math.max(currentParams.radius, 0.001));
  material.needsUpdate = true;

  const targetDistance = Math.max(3 * Math.max(currentParams.radius, 0.1), 3);
  if (camera) {
    const currentDistance = camera.position.length();
    if (Math.abs(currentDistance - targetDistance) > 0.01) {
      camera.position.set(targetDistance, targetDistance * 0.2, targetDistance);
    }
  }
}

function renderFrame() {
  if (!renderer || !scene || !camera) {
    return;
  }
  controls?.update();
  renderer.render(scene, camera);
}

export function setParams(newParams = {}) {
  currentParams = { ...currentParams, ...newParams };
  if (controls) {
    controls.autoRotate = !!currentParams.rotate;
  }
  updatePointCloud();
}

export function initPointCloudApp(container, initialParams = {}, deps = {}) {
  if (!container) {
    throw new Error('A container element is required to initialise the point cloud app.');
  }

  ensureDependencies(deps);
  containerEl = container;
  currentParams = { ...defaultParams, ...initialParams };

  const width = container.clientWidth || window.innerWidth || 1;
  const height = container.clientHeight || window.innerHeight || 1;

  renderer = new THREERef.WebGLRenderer({ antialias: true });
  renderer.setPixelRatio(window.devicePixelRatio || 1);
  renderer.setSize(width, height);
  renderer.outputColorSpace = THREERef.SRGBColorSpace;
  container.appendChild(renderer.domElement);

  scene = new THREERef.Scene();
  scene.background = new THREERef.Color(0x020617);

  camera = new THREERef.PerspectiveCamera(60, width / height, 0.01, 100);
  const startDistance = Math.max(3 * Math.max(currentParams.radius, 0.1), 3);
  camera.position.set(startDistance, startDistance * 0.2, startDistance);
  camera.lookAt(0, 0, 0);

  controls = new OrbitControlsRef(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.05;
  controls.autoRotate = !!currentParams.rotate;
  controls.autoRotateSpeed = 0.4;

  geometry = new THREERef.BufferGeometry();
  material = new THREERef.PointsMaterial({
    size: Math.max(0.0005, 0.01 * Math.max(currentParams.radius, 0.001)),
    sizeAttenuation: true,
    vertexColors: true,
    transparent: true,
    opacity: 0.9,
    depthWrite: false,
  });

  pointCloud = new THREERef.Points(geometry, material);
  scene.add(pointCloud);

  updatePointCloud();
  handleResize();

  if (!animationActive && renderer) {
    animationActive = true;
    renderer.setAnimationLoop(renderFrame);
  }

  window.addEventListener('resize', handleResize);

  return { setParams };
}
