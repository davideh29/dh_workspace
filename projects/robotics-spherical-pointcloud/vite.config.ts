import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

const repoBase = '/dh_workspace/projects/robotics-spherical-pointcloud/';

export default defineConfig({
  base: repoBase,
  build: {
    outDir: 'docs',
    emptyOutDir: true,
  },
  plugins: [react()],
  test: {
    environment: 'jsdom',
    setupFiles: './src/setupTests.ts',
  },
});
