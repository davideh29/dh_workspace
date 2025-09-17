const TAU = Math.PI * 2;
const SINGLE_COLOR = [0x22, 0xcc, 0xff];
const HEIGHT_GRADIENT = {
  low: [34, 102, 255],
  mid: [34, 197, 94],
  high: [250, 204, 21],
};

export function mulberry32(seed) {
  let t = seed >>> 0;
  return function rng() {
    t += 0x6d2b79f5;
    let r = Math.imul(t ^ (t >>> 15), 1 | t);
    r = (r + Math.imul(r ^ (r >>> 7), 61 | r)) ^ r;
    return ((r ^ (r >>> 14)) >>> 0) / 4294967296;
  };
}

function gaussianSample(rng) {
  let u = 0;
  let v = 0;
  // Avoid log(0)
  while (u === 0) {
    u = rng();
  }
  while (v === 0) {
    v = rng();
  }
  return Math.sqrt(-2.0 * Math.log(u)) * Math.cos(TAU * v);
}

function lerp(a, b, t) {
  return a + (b - a) * t;
}

function lerpColor(a, b, t) {
  return [
    Math.round(lerp(a[0], b[0], t)),
    Math.round(lerp(a[1], b[1], t)),
    Math.round(lerp(a[2], b[2], t)),
  ];
}

function computeHeightColor(height, radius) {
  const span = Math.max(radius, 1e-6);
  const normalized = (height + span) / (2 * span);
  const t = Math.min(1, Math.max(0, normalized));

  if (t <= 0.5) {
    const localT = t / 0.5;
    return lerpColor(HEIGHT_GRADIENT.low, HEIGHT_GRADIENT.mid, localT);
  }

  const localT = (t - 0.5) / 0.5;
  return lerpColor(HEIGHT_GRADIENT.mid, HEIGHT_GRADIENT.high, localT);
}

export function generateSpherePoints({
  seed = 0,
  n = 1,
  R = 1,
  noise = 0,
  colorMode = 'single',
}) {
  const count = Math.max(1, Math.floor(n));
  const radius = Math.max(0, R);
  const rng = mulberry32(seed);
  const positions = new Float32Array(count * 3);
  const colors = new Uint8Array(count * 3);

  for (let i = 0; i < count; i += 1) {
    const u = rng();
    const v = rng();

    const theta = TAU * u;
    const phi = Math.acos(2 * v - 1);

    const sinPhi = Math.sin(phi);
    const x = Math.cos(theta) * sinPhi;
    const y = Math.cos(phi);
    const z = Math.sin(theta) * sinPhi;

    const noiseOffset = noise > 0 ? gaussianSample(rng) * noise : 0;
    const pointRadius = Math.max(0, radius + noiseOffset);

    const baseIndex = i * 3;
    positions[baseIndex] = x * pointRadius;
    positions[baseIndex + 1] = y * pointRadius;
    positions[baseIndex + 2] = z * pointRadius;

    let color = SINGLE_COLOR;
    if (colorMode === 'height') {
      color = computeHeightColor(y * radius, radius);
    }

    colors[baseIndex] = color[0];
    colors[baseIndex + 1] = color[1];
    colors[baseIndex + 2] = color[2];
  }

  console.assert(positions.length === count * 3, 'Positions length mismatch');
  console.assert(colors.length === count * 3, 'Colors length mismatch');

  return { positions, colors, count };
}
