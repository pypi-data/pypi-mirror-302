"""Test sparse histogram behavior."""

import numpy as np
import numpy.testing as npt
import pytest
from scipy.sparse import csr_array

from hats_import.catalog.sparse_histogram import SparseHistogram


def test_read_write_round_trip(tmp_path):
    """Test that we can read what we write into a histogram file."""
    file_name = tmp_path / "round_trip.npz"
    histogram = SparseHistogram.make_from_counts([11], [131], 0)
    histogram.to_file(file_name)

    read_histogram = SparseHistogram.from_file(file_name)

    npt.assert_array_equal(read_histogram.to_array(), histogram.to_array())


def test_add_same_order():
    """Test that we can add two histograms created from the same order, and get
    the expected results."""
    partial_histogram_left = SparseHistogram.make_from_counts([11], [131], 0)

    partial_histogram_right = SparseHistogram.make_from_counts([10, 11], [4, 15], 0)

    partial_histogram_left.add(partial_histogram_right)

    expected = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 146]
    npt.assert_array_equal(partial_histogram_left.to_array(), expected)


def test_add_different_order():
    """Test that we can NOT add histograms of different healpix orders."""
    partial_histogram_left = SparseHistogram.make_from_counts([11], [131], 0)

    partial_histogram_right = SparseHistogram.make_from_counts([10, 11], [4, 15], 1)

    with pytest.raises(ValueError, match="partials have incompatible sizes"):
        partial_histogram_left.add(partial_histogram_right)


def test_add_different_type():
    """Test that we can NOT add histograms of different healpix orders."""
    partial_histogram_left = SparseHistogram.make_from_counts([11], [131], 0)

    with pytest.raises(ValueError, match="addends should be SparseHistogram"):
        partial_histogram_left.add(5)

    with pytest.raises(ValueError, match="addends should be SparseHistogram"):
        partial_histogram_left.add([1, 2, 3, 4, 5])


def test_init_bad_inputs():
    """Test that the SparseHistogram type requires a compressed sparse column
    as its sole `sparse_array` argument."""
    with pytest.raises(ValueError, match="must be a scipy sparse array"):
        SparseHistogram(5)

    with pytest.raises(ValueError, match="must be a Compressed Sparse Column"):
        row_sparse_array = csr_array((1, 12), dtype=np.int64)
        SparseHistogram(row_sparse_array)
