# Robotics Point Cloud (Static)

A lightweight, single-page demo for exploring a spherical point cloud rendered with [three.js](https://threejs.org/). The page is completely static and uses CDN modules so it can be hosted on GitHub Pages without a build step.

## Features

- Seeded, reproducible sampling of points on a noisy sphere
- Toggle between a uniform colour and a height-based gradient
- Adjustable point count, sphere radius, gaussian surface noise, and auto-rotation
- Responsive layout with OrbitControls for intuitive navigation

## Local usage

No tooling is required. Clone the repository and open `projects/robotics-pointcloud-static/index.html` in any modern browser, or serve the directory with a simple static server:

```bash
python -m http.server --directory projects/robotics-pointcloud-static 8000
```

Then visit [http://localhost:8000](http://localhost:8000).

## GitHub Pages

1. Push the repository to GitHub.
2. In the repository settings, enable GitHub Pages and choose the default branch (usually `main`) as the source. Keep the root (`/`) folder selected.
3. Your site will be available at:

   ```
   https://<USER>.github.io/<REPO>/projects/robotics-pointcloud-static/
   ```

   Replace `<USER>` with your GitHub username and `<REPO>` with the repository name.
