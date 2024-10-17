"""
Types hints used throughout the package.
"""

import numpy as np

ProbaParam = np.ndarray
# class ProbaParam(np.ndarray):
#     """
#     Type hint for a parameter defining a probability distribution. Used for ProbaMap class.

#     A ProbaParam should be convertible to a np.ndarray.
#     """

ProbaParams = np.ndarray

# Type alias for a single sample
SamplePoint = np.ndarray
# class SamplePoint(np.ndarray):
#     """
#     Type hint class for a single sample point

#     A SamplePoint should be convertible to a np.ndarray of shape sample_shape
#     """

Samples = np.ndarray
# class Samples(np.ndarray):
#     """
#     Type hint class for multiple sample points stored properly in a np.ndarray object.

#     The array should be of shape (pre_shape, sample_shape) where pre_shape may be anything,
#     including (,).
#     """

