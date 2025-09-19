import { memo, useEffect, useMemo, useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

import { ColorMode, RGBColor, generateSpherePoints } from '../lib/points';

interface PointCloudProps {
  seed: number;
  numPoints: number;
  radius: number;
  noise: number;
  colorMode: ColorMode;
  color: RGBColor;
  rotate: boolean;
}

function PointCloud({
  seed,
  numPoints,
  radius,
  noise,
  colorMode,
  color,
  rotate,
}: PointCloudProps): JSX.Element {
  const pointsRef = useRef<THREE.Points>(null);

  const { positions, colors } = useMemo(
    () =>
      generateSpherePoints({
        seed,
        numPoints,
        radius,
        noise,
        colorMode,
        color,
      }),
    [seed, numPoints, radius, noise, colorMode, color],
  );

  const geometry = useMemo(() => {
    const bufferGeometry = new THREE.BufferGeometry();
    bufferGeometry.setAttribute(
      'position',
      new THREE.BufferAttribute(positions, 3),
    );
    bufferGeometry.setAttribute(
      'color',
      new THREE.BufferAttribute(colors, 3),
    );
    bufferGeometry.computeBoundingSphere();
    return bufferGeometry;
  }, [positions, colors]);

  useEffect(() => () => geometry.dispose(), [geometry]);

  useFrame((_, delta) => {
    if (!rotate) {
      return;
    }
    if (pointsRef.current) {
      pointsRef.current.rotation.y += delta * 0.25;
    }
  });

  return (
    <points ref={pointsRef} geometry={geometry} frustumCulled={false}>
      <pointsMaterial
        size={0.02}
        vertexColors
        sizeAttenuation
        depthWrite={false}
      />
    </points>
  );
}

export default memo(PointCloud);
