import numpy as np
import pytest
from auro_utils.maths import (
    xyzw_to_wxyz,
    wxzy_to_xyzw,
    position_and_orientation_to_pose,
    pose_to_position_and_orientation
)

def test_xyzw_to_wxyz():
    assert xyzw_to_wxyz([1, 2, 3, 4]) == [4, 1, 2, 3]
    assert np.array_equal(xyzw_to_wxyz(np.array([1, 2, 3, 4])), np.array([4, 1, 2, 3]))

def test_wxzy_to_xyzw():
    assert wxzy_to_xyzw([4, 1, 2, 3]) == [1, 2, 3, 4]
    assert np.array_equal(wxzy_to_xyzw(np.array([4, 1, 2, 3])), np.array([1, 2, 3, 4]))

def test_position_and_orientation_to_pose():
    position = [1, 2, 3]
    orientation = [4, 5, 6, 7]
    assert position_and_orientation_to_pose(position, orientation) == [1, 2, 3, 4, 5, 6, 7]
    assert np.array_equal(position_and_orientation_to_pose(np.array(position), np.array(orientation)),
                          np.array([1, 2, 3, 4, 5, 6, 7]))

def test_pose_to_position_and_orientation():
    pose = [1, 2, 3, 4, 5, 6, 7, 8]
    position, orientation = pose_to_position_and_orientation(pose)
    assert position == [1, 2, 3]
    assert orientation == [4, 5, 6, 7]
    pose_np = np.array(pose)
    pos_np, orient_np = pose_to_position_and_orientation(pose_np)
    assert np.array_equal(pos_np, np.array([1, 2, 3]))
    assert np.array_equal(orient_np, np.array([4, 5, 6, 7]))

if __name__ == "__main__":
    pytest.main()
