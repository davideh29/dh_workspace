"""Tests for the :mod:`projects.linear_algebra.transform3d` module."""

from __future__ import annotations

import numpy as np
from numpy.testing import assert_allclose

from projects.linear_algebra import Transform3d, interpolate_transform


def rotation_matrix_x(angle_deg: float) -> np.ndarray:
    angle = np.deg2rad(angle_deg)
    c, s = np.cos(angle), np.sin(angle)
    return np.array([[1.0, 0.0, 0.0], [0.0, c, -s], [0.0, s, c]])


def rotation_matrix_y(angle_deg: float) -> np.ndarray:
    angle = np.deg2rad(angle_deg)
    c, s = np.cos(angle), np.sin(angle)
    return np.array([[c, 0.0, s], [0.0, 1.0, 0.0], [-s, 0.0, c]])


def rotation_matrix_z(angle_deg: float) -> np.ndarray:
    angle = np.deg2rad(angle_deg)
    c, s = np.cos(angle), np.sin(angle)
    return np.array([[c, -s, 0.0], [s, c, 0.0], [0.0, 0.0, 1.0]])


def axis_angle_quaternion(axis: np.ndarray, angle_deg: float) -> np.ndarray:
    axis = np.asarray(axis, dtype=float)
    axis = axis / np.linalg.norm(axis)
    angle = np.deg2rad(angle_deg)
    half_angle = angle / 2.0
    sin_half = np.sin(half_angle)
    return np.concatenate((axis * sin_half, [np.cos(half_angle)]))


def test_identity_does_not_modify_points() -> None:
    transform = Transform3d.identity()
    point = np.array([1.0, -2.0, 3.0])
    assert_allclose(transform.apply(point), point)

    cloud = np.array([[0.0, 0.0, 0.0], [1.0, 2.0, 3.0]])
    assert_allclose(transform.apply(cloud), cloud)


def test_as_matrix_and_from_matrix_roundtrip() -> None:
    rotation = rotation_matrix_z(25.0) @ rotation_matrix_x(-10.0)
    translation = np.array([3.0, -4.0, 5.0])
    transform = Transform3d.from_translation_rotation(translation, rotation)

    matrix = transform.as_matrix()
    rebuilt = Transform3d.from_matrix(matrix)

    assert_allclose(rebuilt.translation, translation)
    assert_allclose(rebuilt.rotation_matrix, rotation, atol=1e-12)


def test_compose_matches_matrix_product() -> None:
    base = Transform3d.from_translation_rotation(
        [1.0, 0.0, 0.0], rotation_matrix_z(90.0)
    )
    offset = Transform3d.from_translation_rotation(
        [0.0, 1.0, 0.0], rotation_matrix_x(45.0)
    )

    composed = base.compose(offset)

    matrix_product = base.as_matrix() @ offset.as_matrix()
    expected = Transform3d.from_matrix(matrix_product)

    assert_allclose(composed.translation, expected.translation)
    assert_allclose(composed.rotation_matrix, expected.rotation_matrix, atol=1e-12)


def test_inverse_recovers_identity() -> None:
    quaternion = axis_angle_quaternion(np.array([1.0, 2.0, 3.0]), 67.0)
    transform = Transform3d.from_translation_rotation([-3.0, 2.0, 5.0], quaternion)

    identity = transform.compose(transform.inverse())
    assert_allclose(identity.translation, np.zeros(3), atol=1e-12)
    assert_allclose(identity.rotation_matrix, np.eye(3), atol=1e-12)


def test_quaternion_matches_rotation() -> None:
    quaternion = axis_angle_quaternion(np.array([0.0, 0.0, 1.0]), 90.0)
    transform = Transform3d.from_translation_rotation([0.0, 0.0, 0.0], quaternion)

    assert_allclose(transform.quaternion, quaternion)


def test_translate_and_rotate_helpers() -> None:
    transform = Transform3d.identity()
    translated = transform.translate([1.0, 2.0, 3.0])
    assert_allclose(translated.translation, np.array([1.0, 2.0, 3.0]))

    quarter_turn = axis_angle_quaternion(np.array([0.0, 1.0, 0.0]), 90.0)
    rotated = transform.rotate(quarter_turn)
    expected_matrix = rotation_matrix_y(90.0)
    assert_allclose(rotated.rotation_matrix, expected_matrix, atol=1e-12)


def test_interpolate_transform_blends_translation_and_rotation() -> None:
    start = Transform3d.identity()
    end = Transform3d.from_translation_rotation(
        np.array([4.0, -2.0, 0.0]), rotation_matrix_z(90.0)
    )

    halfway = interpolate_transform(start, end, 0.5)

    assert_allclose(halfway.translation, np.array([2.0, -1.0, 0.0]))

    expected_rotation = rotation_matrix_z(45.0)
    assert_allclose(halfway.rotation_matrix, expected_rotation, atol=1e-12)


def test_interpolate_transform_extremes_match_inputs() -> None:
    start = Transform3d.from_translation_rotation(
        np.array([-1.0, 0.5, 2.0]),
        axis_angle_quaternion(np.array([1.0, 0.0, 0.0]), 30.0),
    )
    end = Transform3d.from_translation_rotation(
        np.array([2.0, -1.5, -2.0]),
        axis_angle_quaternion(np.array([0.0, 0.0, 1.0]), 120.0),
    )

    assert_allclose(
        interpolate_transform(start, end, 0.0).translation, start.translation
    )
    assert_allclose(
        interpolate_transform(start, end, 0.0).rotation_matrix,
        start.rotation_matrix,
        atol=1e-12,
    )

    assert_allclose(interpolate_transform(start, end, 1.0).translation, end.translation)
    assert_allclose(
        interpolate_transform(start, end, 1.0).rotation_matrix,
        end.rotation_matrix,
        atol=1e-12,
    )


def test_interpolate_transform_rejects_fraction_outside_unit_interval() -> None:
    start = Transform3d.identity()
    end = Transform3d.identity()

    with np.testing.assert_raises(ValueError):
        interpolate_transform(start, end, -0.1)

    with np.testing.assert_raises(ValueError):
        interpolate_transform(start, end, 1.1)

    with np.testing.assert_raises(TypeError):
        interpolate_transform(start, end, "0.5")
