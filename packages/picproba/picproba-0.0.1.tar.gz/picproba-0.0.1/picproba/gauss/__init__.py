"""
Gaussian distributions and related
"""

from picproba.gauss.BlockGauss import BlockDiagGauss, BlockDiagGaussMap
from picproba.gauss.fixed_cov_gaussian_map import (
    FactCovGaussianMap,
    FixedCovGaussianMap,
)
from picproba.gauss.Gauss import Gaussian, GaussianMap
from picproba.gauss.gauss_hyperball import GaussHyperballMap
from picproba.gauss.gauss_hypercube import GaussHypercubeMap
from picproba.gauss.TGauss import (
    TensorizedGaussian,
    TensorizedGaussianMap,
    tgauss_to_gauss_param,
)
