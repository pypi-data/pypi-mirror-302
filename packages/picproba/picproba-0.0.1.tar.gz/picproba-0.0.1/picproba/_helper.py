"""Miscallenous helper function for Gaussian distributions/Maps"""

import warnings
from typing import Optional

from apicutils import prod

from picproba.warnings import ShapeWarning


def shape_info(
    sample_size: Optional[int] = None, sample_shape: Optional[tuple[int, ...]] = None
) -> tuple[int, tuple[int, ...]]:
    """
    Check and format shape information from potentially incomplete information

    Args:
        sample_size: int (Optional)
        sample_shape: tuple of int (Optional)
    Raise:
        ValueError if both inputs are None
    Returns:
        tuple of int and tuple of int (size/shape as inferred from size/shape).
        If size is incoherent with shape, sample_size is disregarded
    """
    if (sample_size is None) and (sample_shape is None):
        raise ValueError("Either 'sample_size' or 'sample_shape' must be specified.")

    if sample_shape is None:
        sample_shape = (sample_size,)  # type: ignore

    elif sample_size is None:
        sample_size = prod(
            sample_shape
        )  # Define if sample_size is missing/Force coherence if both are specified

    elif sample_size != prod(sample_shape):  # type: ignore
        warnings.warn(  # type: ignore
            message=''.join([
                f"'sample_size' {sample_size} and 'sample_shape' {sample_shape}",
                " arguments are incoherent.",
                " Using 'sample_shape' information"]),
            category=ShapeWarning,
        )
        sample_size = prod(sample_shape)

    return sample_size, sample_shape  # type: ignore
