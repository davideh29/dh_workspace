import { createNormalGenerator, mulberry32, PRNG } from './prng';

export type ColorMode = 'single' | 'height';

export interface RGBColor {
  r: number;
  g: number;
  b: number;
}

export interface SpherePointOptions {
  seed: number;
  numPoints: number;
  radius: number;
  noise: number;
  colorMode: ColorMode;
  color?: RGBColor;
}

export interface SpherePointCloud {
  positions: Float32Array;
  colors: Float32Array;
}

const DEFAULT_SINGLE_COLOR: RGBColor = { r: 0.376, g: 0.647, b: 0.996 };
const BLUE: RGBColor = { r: 0.121, g: 0.305, b: 0.784 };
const GREEN: RGBColor = { r: 0.102, g: 0.729, b: 0.451 };
const YELLOW: RGBColor = { r: 0.992, g: 0.871, b: 0.384 };

const clamp01 = (value: number): number => Math.min(1, Math.max(0, value));

const lerp = (start: number, end: number, t: number): number =>
  start + (end - start) * t;

const lerpColor = (start: RGBColor, end: RGBColor, t: number): RGBColor => ({
  r: lerp(start.r, end.r, t),
  g: lerp(start.g, end.g, t),
  b: lerp(start.b, end.b, t),
});

const yGradientColor = (y: number, radius: number): RGBColor => {
  if (!Number.isFinite(radius) || radius <= 0) {
    return GREEN;
  }
  const normalized = clamp01((y / radius + 1) / 2);
  if (normalized < 0.5) {
    return lerpColor(BLUE, GREEN, normalized / 0.5);
  }
  return lerpColor(GREEN, YELLOW, (normalized - 0.5) / 0.5);
};

const colorFromMode = (
  mode: ColorMode,
  y: number,
  radius: number,
  singleColor: RGBColor,
): RGBColor => {
  if (mode === 'height') {
    return yGradientColor(y, radius);
  }
  return singleColor;
};

const gaussianNoise = (normal: PRNG, amount: number): number => {
  if (amount <= 0) {
    return 0;
  }
  return normal() * amount;
};

const directionOnSphere = (prng: PRNG): [number, number, number] => {
  const u = prng();
  const v = prng();
  const theta = 2 * Math.PI * u;
  const cosPhi = 2 * v - 1;
  const sinPhi = Math.sqrt(Math.max(0, 1 - cosPhi * cosPhi));
  const x = sinPhi * Math.cos(theta);
  const y = cosPhi;
  const z = sinPhi * Math.sin(theta);
  return [x, y, z];
};

export function generateSpherePoints({
  seed,
  numPoints,
  radius,
  noise,
  colorMode,
  color,
}: SpherePointOptions): SpherePointCloud {
  const prng = mulberry32(seed);
  const normal = createNormalGenerator(prng);

  const positions = new Float32Array(numPoints * 3);
  const colors = new Float32Array(numPoints * 3);
  const singleColor = color ?? DEFAULT_SINGLE_COLOR;

  for (let index = 0; index < numPoints; index += 1) {
    const offset = index * 3;
    const [dirX, dirY, dirZ] = directionOnSphere(prng);
    const radial = Math.max(0, radius + gaussianNoise(normal, noise));

    positions[offset] = dirX * radial;
    positions[offset + 1] = dirY * radial;
    positions[offset + 2] = dirZ * radial;

    const colorValue = colorFromMode(colorMode, positions[offset + 1], radius, singleColor);
    colors[offset] = colorValue.r;
    colors[offset + 1] = colorValue.g;
    colors[offset + 2] = colorValue.b;
  }

  return { positions, colors };
}

export function hexToRgb(hex: string): RGBColor {
  const normalized = hex.replace('#', '').trim();
  if (normalized.length !== 3 && normalized.length !== 6) {
    return DEFAULT_SINGLE_COLOR;
  }

  const expand = normalized.length === 3;
  const value = expand
    ? normalized
        .split('')
        .map((char) => char + char)
        .join('')
    : normalized;

  const r = Number.parseInt(value.slice(0, 2), 16) / 255;
  const g = Number.parseInt(value.slice(2, 4), 16) / 255;
  const b = Number.parseInt(value.slice(4, 6), 16) / 255;

  if ([r, g, b].some((component) => Number.isNaN(component))) {
    return DEFAULT_SINGLE_COLOR;
  }

  return { r, g, b };
}

export { DEFAULT_SINGLE_COLOR };
