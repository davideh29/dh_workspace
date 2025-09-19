export type PRNG = () => number;

const UINT32_MAX = 0xffffffff;

/**
 * Deterministic pseudo-random number generator based on mulberry32.
 * @param seed Numeric seed.
 * @returns Function returning a float in [0, 1).
 */
export function mulberry32(seed: number): PRNG {
  let t = (seed >>> 0) || 0x6d2b79f5;
  return () => {
    t += 0x6d2b79f5;
    let x = Math.imul(t ^ (t >>> 15), t | 1);
    x ^= x + Math.imul(x ^ (x >>> 7), x | 61);
    return ((x ^ (x >>> 14)) >>> 0) / (UINT32_MAX + 1);
  };
}

/**
 * Returns a PRNG that yields normally distributed values using the Box-Muller
 * transform.
 */
export function createNormalGenerator(prng: PRNG): PRNG {
  let spare: number | null = null;
  return () => {
    if (spare !== null) {
      const value = spare;
      spare = null;
      return value;
    }

    let u = 0;
    let v = 0;
    while (u === 0) {
      u = prng();
    }
    while (v === 0) {
      v = prng();
    }

    const mag = Math.sqrt(-2.0 * Math.log(u));
    const theta = 2.0 * Math.PI * v;
    spare = mag * Math.sin(theta);
    return mag * Math.cos(theta);
  };
}

export function seededRandom(seed: number): PRNG {
  return mulberry32(seed);
}
