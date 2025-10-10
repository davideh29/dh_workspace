# Linear algebra utilities

This package contains helpers for working with three-dimensional rigid-body
transformations. The core component is the `Transform3d` class defined in
`transform3d.py`, which encapsulates rotation (as a quaternion or rotation
matrix) and translation vectors in a single object.

## Features

- Parse rotations provided as quaternions or 3x3 rotation matrices.
- Generate homogeneous 4x4 matrices from a transform instance.
- Apply transforms to single points or batches of 3D points.
- Compose multiple transforms using quaternion multiplication with
  `Transform3d.dot`.
- Compute inverse transforms for undoing a rigid-body pose.

## Usage

```python
import numpy as np
from projects.linear_algebra.transform3d import Transform3d

base_pose = Transform3d.from_translation_rotation(
    translation=[1.0, 2.0, 3.0],
    rotation=[0.0, 0.0, 0.0, 1.0],  # identity quaternion
)

# Apply the transform to a point in space
point = np.array([0.5, -0.25, 1.0])
world_point = base_pose.apply(point)

# Compose with an additional rotation around Z
rotation = Transform3d.from_translation_rotation(
    translation=[0.0, 0.0, 0.0],
    rotation=[0.0, 0.0, np.sin(np.pi / 4), np.cos(np.pi / 4)],
)
combined = rotation.dot(base_pose)

# Convert back to a 4x4 homogeneous matrix
matrix = combined.as_matrix()
```

Run the project's tests from the repository root with:

```bash
pytest src/projects/linear_algebra/tests
```
