import { ChangeEvent } from 'react';

import { ColorMode } from '../lib/points';

interface ControlsPanelProps {
  seed: number;
  onSeedChange: (value: number) => void;
  numPoints: number;
  onNumPointsChange: (value: number) => void;
  radius: number;
  onRadiusChange: (value: number) => void;
  noise: number;
  onNoiseChange: (value: number) => void;
  colorMode: ColorMode;
  onColorModeChange: (mode: ColorMode) => void;
  color: string;
  onColorChange: (value: string) => void;
  rotate: boolean;
  onRotateChange: (value: boolean) => void;
}

const formatNumber = (value: number, fractionDigits = 2): string =>
  value.toLocaleString(undefined, {
    maximumFractionDigits: fractionDigits,
  });

function ControlsPanel({
  seed,
  onSeedChange,
  numPoints,
  onNumPointsChange,
  radius,
  onRadiusChange,
  noise,
  onNoiseChange,
  colorMode,
  onColorModeChange,
  color,
  onColorChange,
  rotate,
  onRotateChange,
}: ControlsPanelProps): JSX.Element {
  const handleSeedChange = (event: ChangeEvent<HTMLInputElement>) => {
    const value = Number.parseInt(event.target.value, 10);
    if (!Number.isNaN(value)) {
      onSeedChange(value);
    }
  };

  return (
    <section className="controls-panel">
      <h2>Point Cloud Settings</h2>
      <label>
        Seed
        <input
          type="number"
          value={seed}
          min={0}
          step={1}
          onChange={handleSeedChange}
        />
      </label>
      <label>
        Number of points
        <div className="range-input">
          <input
            type="range"
            min={1000}
            max={100000}
            step={500}
            value={numPoints}
            onChange={(event) => onNumPointsChange(Number(event.target.value))}
          />
          <span>{numPoints.toLocaleString()}</span>
        </div>
      </label>
      <label>
        Radius
        <div className="range-input">
          <input
            type="range"
            min={0.1}
            max={5}
            step={0.05}
            value={radius}
            onChange={(event) => onRadiusChange(Number(event.target.value))}
          />
          <span>{formatNumber(radius)}</span>
        </div>
      </label>
      <label>
        Noise
        <div className="range-input">
          <input
            type="range"
            min={0}
            max={0.2}
            step={0.005}
            value={noise}
            onChange={(event) => onNoiseChange(Number(event.target.value))}
          />
          <span>{formatNumber(noise, 3)}</span>
        </div>
      </label>
      <label>
        Color mode
        <select
          value={colorMode}
          onChange={(event) => onColorModeChange(event.target.value as ColorMode)}
        >
          <option value="single">Single</option>
          <option value="height">Height gradient</option>
        </select>
      </label>
      {colorMode === 'single' ? (
        <label>
          Point color
          <input
            type="color"
            value={color}
            onChange={(event) => onColorChange(event.target.value)}
            aria-label="Point color picker"
          />
        </label>
      ) : null}
      <div className="checkbox-row">
        <input
          id="rotate-toggle"
          type="checkbox"
          checked={rotate}
          onChange={(event) => onRotateChange(event.target.checked)}
        />
        <label htmlFor="rotate-toggle">Auto-rotate</label>
      </div>
    </section>
  );
}

export default ControlsPanel;
