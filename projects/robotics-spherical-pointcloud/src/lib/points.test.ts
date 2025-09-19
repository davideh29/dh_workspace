import { describe, expect, it } from 'vitest';

import { generateSpherePoints } from './points';

const BASE_CONFIG = {
  seed: 12345,
  numPoints: 2048,
  radius: 1.5,
  noise: 0,
  colorMode: 'height' as const,
};

describe('generateSpherePoints', () => {
  it('produces deterministic point clouds for the same inputs', () => {
    const first = generateSpherePoints(BASE_CONFIG);
    const second = generateSpherePoints(BASE_CONFIG);

    expect(Array.from(second.positions.slice(0, 30))).toStrictEqual(
      Array.from(first.positions.slice(0, 30)),
    );
  });

  it('creates the expected number of coordinates', () => {
    const { positions } = generateSpherePoints({ ...BASE_CONFIG, numPoints: 4096 });
    expect(positions.length).toBe(4096 * 3);
  });

  it('generates points close to the specified radius when noise is zero', () => {
    const radius = 2.5;
    const { positions } = generateSpherePoints({ ...BASE_CONFIG, radius });
    let total = 0;
    const sampleSize = positions.length / 3;
    for (let index = 0; index < sampleSize; index += 1) {
      const offset = index * 3;
      const x = positions[offset];
      const y = positions[offset + 1];
      const z = positions[offset + 2];
      total += Math.sqrt(x * x + y * y + z * z);
    }
    const meanRadius = total / sampleSize;
    expect(meanRadius).toBeGreaterThan(radius - 0.02);
    expect(meanRadius).toBeLessThan(radius + 0.02);
  });
});
