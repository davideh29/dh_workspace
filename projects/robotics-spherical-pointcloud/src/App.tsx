import { Suspense, useMemo, useState } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, Preload } from '@react-three/drei';

import ControlsPanel from './components/ControlsPanel';
import PointCloud from './components/PointCloud';
import { ColorMode, hexToRgb } from './lib/points';

const DEFAULT_SEED = 42;
const DEFAULT_POINTS = 5000;
const DEFAULT_RADIUS = 1;
const DEFAULT_NOISE = 0.02;
const DEFAULT_COLOR = '#60a5fa';

function App(): JSX.Element {
  const [seed, setSeed] = useState<number>(DEFAULT_SEED);
  const [numPoints, setNumPoints] = useState<number>(DEFAULT_POINTS);
  const [radius, setRadius] = useState<number>(DEFAULT_RADIUS);
  const [noise, setNoise] = useState<number>(DEFAULT_NOISE);
  const [colorMode, setColorMode] = useState<ColorMode>('height');
  const [color, setColor] = useState<string>(DEFAULT_COLOR);
  const [rotate, setRotate] = useState<boolean>(true);

  const rgbColor = useMemo(() => hexToRgb(color), [color]);

  return (
    <>
      <Canvas camera={{ position: [0, 0, 4], fov: 45 }} dpr={[1, 2]}>
        <color attach="background" args={["#020617"]} />
        <ambientLight intensity={0.8} />
        <Suspense fallback={null}>
          <PointCloud
            seed={seed}
            numPoints={numPoints}
            radius={radius}
            noise={noise}
            colorMode={colorMode}
            color={rgbColor}
            rotate={rotate}
          />
        </Suspense>
        <OrbitControls enableDamping dampingFactor={0.15} />
        <Preload all />
      </Canvas>
      <ControlsPanel
        seed={seed}
        onSeedChange={setSeed}
        numPoints={numPoints}
        onNumPointsChange={setNumPoints}
        radius={radius}
        onRadiusChange={setRadius}
        noise={noise}
        onNoiseChange={setNoise}
        colorMode={colorMode}
        onColorModeChange={setColorMode}
        color={color}
        onColorChange={setColor}
        rotate={rotate}
        onRotateChange={setRotate}
      />
    </>
  );
}

export default App;
