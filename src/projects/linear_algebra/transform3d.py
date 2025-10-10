"""Three-dimensional rigid transformation utilities."""

from __future__ import annotations

import numpy as np
from numpy.typing import ArrayLike, NDArray

Vector3 = NDArray[np.float64]
Quaternion = NDArray[np.float64]
Matrix3 = NDArray[np.float64]
Matrix4 = NDArray[np.float64]


def _normalize_quaternion(quaternion: ArrayLike) -> Quaternion:
    """Return a unit quaternion from any four-vector."""
    quat = np.asarray(quaternion, dtype=float).reshape(-1)
    if quat.shape != (4,):
        raise ValueError("Quaternion must be a four-element vector.")

    norm = np.linalg.norm(quat)
    if norm == 0:
        raise ValueError("Quaternion must have a non-zero magnitude.")
    return quat / norm


def _quaternion_from_matrix(matrix: ArrayLike) -> Quaternion:
    """Convert a 3x3 rotation matrix into a quaternion."""
    mat = np.asarray(matrix, dtype=float)
    if mat.shape != (3, 3):
        raise ValueError("Rotation matrix must have shape (3, 3).")

    trace = np.trace(mat)
    if trace > 0.0:
        s = 0.5 / np.sqrt(trace + 1.0)
        w = 0.25 / s
        x = (mat[2, 1] - mat[1, 2]) * s
        y = (mat[0, 2] - mat[2, 0]) * s
        z = (mat[1, 0] - mat[0, 1]) * s
    else:
        diag = np.array([mat[0, 0], mat[1, 1], mat[2, 2]])
        idx = int(np.argmax(diag))
        if idx == 0:
            s = 2.0 * np.sqrt(1.0 + mat[0, 0] - mat[1, 1] - mat[2, 2])
            x = 0.25 * s
            y = (mat[0, 1] + mat[1, 0]) / s
            z = (mat[0, 2] + mat[2, 0]) / s
            w = (mat[2, 1] - mat[1, 2]) / s
        elif idx == 1:
            s = 2.0 * np.sqrt(1.0 + mat[1, 1] - mat[0, 0] - mat[2, 2])
            x = (mat[0, 1] + mat[1, 0]) / s
            y = 0.25 * s
            z = (mat[1, 2] + mat[2, 1]) / s
            w = (mat[0, 2] - mat[2, 0]) / s
        else:
            s = 2.0 * np.sqrt(1.0 + mat[2, 2] - mat[0, 0] - mat[1, 1])
            x = (mat[0, 2] + mat[2, 0]) / s
            y = (mat[1, 2] + mat[2, 1]) / s
            z = 0.25 * s
            w = (mat[1, 0] - mat[0, 1]) / s
    return _normalize_quaternion(np.array([x, y, z, w]))


def _matrix_from_quaternion(quaternion: Quaternion) -> Matrix3:
    """Return the rotation matrix associated with ``quaternion``."""
    x, y, z, w = quaternion
    xx, yy, zz = x * x, y * y, z * z
    xy, xz, yz = x * y, x * z, y * z
    xw, yw, zw = x * w, y * w, z * w

    return np.array(
        [
            [1.0 - 2.0 * (yy + zz), 2.0 * (xy - zw), 2.0 * (xz + yw)],
            [2.0 * (xy + zw), 1.0 - 2.0 * (xx + zz), 2.0 * (yz - xw)],
            [2.0 * (xz - yw), 2.0 * (yz + xw), 1.0 - 2.0 * (xx + yy)],
        ]
    )


def _quaternion_multiply(lhs: Quaternion, rhs: Quaternion) -> Quaternion:
    """Return the Hamilton product ``lhs * rhs``."""
    x1, y1, z1, w1 = lhs
    x2, y2, z2, w2 = rhs
    x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
    y = w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2
    z = w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2
    w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
    return _normalize_quaternion(np.array([x, y, z, w]))


def _quaternion_conjugate(quaternion: Quaternion) -> Quaternion:
    """Return the conjugate of ``quaternion``."""
    x, y, z, w = quaternion
    return np.array([-x, -y, -z, w])


def _coerce_quaternion(rotation: ArrayLike) -> Quaternion:
    """Parse supported rotation formats into a quaternion."""
    rotation_arr = np.asarray(rotation, dtype=float)
    if rotation_arr.shape == (4,):
        return _normalize_quaternion(rotation_arr)
    if rotation_arr.shape == (3, 3):
        return _quaternion_from_matrix(rotation_arr)
    raise TypeError("Rotation must be provided as a quaternion or 3x3 rotation matrix.")


def interpolate_transform(
    start: "Transform3d", end: "Transform3d", fraction: float
) -> "Transform3d":
    """Return the transform fractionally between ``start`` and ``end``.

    Parameters
    ----------
    start
        The initial transform.
    end
        The final transform.
    fraction
        Interpolation factor in ``[0, 1]`` where ``0`` returns ``start`` and
        ``1`` returns ``end``.
    """

    if not isinstance(fraction, (int, float)):
        raise TypeError("fraction must be a real number.")

    fraction = float(fraction)

    if not 0.0 <= fraction <= 1.0:
        raise ValueError("fraction must be within [0, 1].")

    start_translation = start.translation
    end_translation = end.translation
    translation = (1.0 - fraction) * start_translation + fraction * end_translation

    start_quaternion = start.quaternion
    end_quaternion = end.quaternion

    dot = float(np.dot(start_quaternion, end_quaternion))
    if dot < 0.0:
        end_quaternion = -end_quaternion
        dot = -dot

    if dot > 0.9995:
        interpolated = start_quaternion + fraction * (end_quaternion - start_quaternion)
        rotation = _normalize_quaternion(interpolated)
    else:
        dot = np.clip(dot, -1.0, 1.0)
        theta_0 = np.arccos(dot)
        sin_theta_0 = np.sin(theta_0)
        theta = theta_0 * fraction
        sin_theta = np.sin(theta)
        scale_start = np.sin(theta_0 - theta) / sin_theta_0
        scale_end = sin_theta / sin_theta_0
        rotation = scale_start * start_quaternion + scale_end * end_quaternion
        rotation = _normalize_quaternion(rotation)

    return Transform3d(translation=translation, rotation=rotation)


class Transform3d:
    """Represents a 3D rigid transform with rotation and translation."""

    __slots__ = ("_translation", "_quaternion")

    def __init__(self, translation: ArrayLike, rotation: ArrayLike) -> None:
        translation_arr = np.asarray(translation, dtype=float).reshape(-1)
        if translation_arr.shape != (3,):
            raise ValueError("Translation must be a three-dimensional vector.")
        self._translation = translation_arr
        self._quaternion = _coerce_quaternion(rotation)

    @property
    def translation(self) -> Vector3:
        """Return the translation component."""
        return self._translation.copy()

    @property
    def quaternion(self) -> Quaternion:
        """Return the rotation encoded as ``[x, y, z, w]``."""
        return self._quaternion.copy()

    @property
    def rotation_matrix(self) -> Matrix3:
        """Return the 3x3 rotation matrix."""
        return _matrix_from_quaternion(self._quaternion)

    @classmethod
    def identity(cls) -> "Transform3d":
        """Return the identity transform."""
        return cls(translation=np.zeros(3), rotation=np.array([0.0, 0.0, 0.0, 1.0]))

    @classmethod
    def from_translation_rotation(
        cls, translation: ArrayLike, rotation: ArrayLike
    ) -> "Transform3d":
        """Construct a transform from translation and rotation components."""
        return cls(translation=translation, rotation=rotation)

    @classmethod
    def from_matrix(cls, matrix: ArrayLike) -> "Transform3d":
        """Build a transform from a 4x4 homogeneous transformation matrix."""
        mat = np.asarray(matrix, dtype=float)
        if mat.shape != (4, 4):
            raise ValueError("Matrix must have shape (4, 4).")
        rotation = mat[:3, :3]
        translation = mat[:3, 3]
        return cls(translation=translation, rotation=rotation)

    def as_matrix(self) -> Matrix4:
        """Return the 4x4 homogeneous transformation matrix."""
        matrix = np.eye(4)
        matrix[:3, :3] = self.rotation_matrix
        matrix[:3, 3] = self._translation
        return matrix

    def apply(self, points: ArrayLike) -> NDArray[np.float64]:
        """Apply the transform to a single point or an array of points."""
        pts = np.asarray(points, dtype=float)
        rot_matrix = self.rotation_matrix
        if pts.ndim == 1:
            if pts.shape != (3,):
                raise ValueError("Point must have shape (3,).")
            return rot_matrix @ pts + self._translation
        if pts.ndim == 2 and pts.shape[1] == 3:
            return pts @ rot_matrix.T + self._translation
        raise ValueError("Points must be a 3-vector or array with shape (N, 3).")

    def compose(self, other: "Transform3d") -> "Transform3d":
        """Return the transform equivalent to applying ``other`` then ``self``."""
        composed_quaternion = _quaternion_multiply(self._quaternion, other._quaternion)
        composed_translation = (
            self.rotation_matrix @ other._translation + self._translation
        )
        return Transform3d(
            translation=composed_translation, rotation=composed_quaternion
        )

    def inverse(self) -> "Transform3d":
        """Return the inverse transformation."""
        inv_quaternion = _quaternion_conjugate(self._quaternion)
        inv_rotation = _matrix_from_quaternion(inv_quaternion)
        inv_translation = -inv_rotation @ self._translation
        return Transform3d(translation=inv_translation, rotation=inv_quaternion)

    def translate(self, offset: ArrayLike) -> "Transform3d":
        """Return a copy with an additional translation applied."""
        offset_vec = np.asarray(offset, dtype=float).reshape(-1)
        if offset_vec.shape != (3,):
            raise ValueError("Offset must be a three-dimensional vector.")
        return Transform3d(
            translation=self._translation + offset_vec,
            rotation=self._quaternion,
        )

    def rotate(self, rotation: ArrayLike) -> "Transform3d":
        """Return a copy rotated by the provided quaternion or matrix."""
        rot_quaternion = _coerce_quaternion(rotation)
        combined = _quaternion_multiply(rot_quaternion, self._quaternion)
        return Transform3d(translation=self._translation, rotation=combined)

    def __repr__(self) -> str:
        """Return a developer-friendly representation."""
        translation = np.array2string(self._translation, precision=5)
        quaternion = np.array2string(self._quaternion, precision=5)
        return f"Transform3d(translation={translation}, quaternion={quaternion})"
