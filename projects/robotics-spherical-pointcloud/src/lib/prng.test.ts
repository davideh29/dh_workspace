import { describe, expect, it } from 'vitest';

import { mulberry32 } from './prng';

describe('mulberry32', () => {
  it('generates repeatable sequences for the same seed', () => {
    const prngA = mulberry32(9876);
    const prngB = mulberry32(9876);

    const sequenceA = Array.from({ length: 5 }, () => prngA());
    const sequenceB = Array.from({ length: 5 }, () => prngB());

    expect(sequenceB).toStrictEqual(sequenceA);
  });
});
