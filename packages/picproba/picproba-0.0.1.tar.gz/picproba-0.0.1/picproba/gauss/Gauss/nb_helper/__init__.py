""" Numba functions used for Gauss submodule
Functions are defined in _aot_comp.py and exported by running the scrip to gauss_nb
Loaded functions are loaded and wrapped in __init__

NOTE: the compiled functions in *.so file SHOULD NOT be accessible by default!
Indeed, these functions may cause the kernel to crash if used with improper arguments.

"""

# import numpy as np
from picproba.gauss.Gauss.nb_helper._aot_comp import (
    _g,
    _grad_g,
    _grad_kl,
    _grad_right_kl,
    _kl,
    _T_to_param,
    inverse_cov,
    make_cov,
)

# from picproba.gauss.Gauss.nb_helper.gauss_nb import _g as __g
# from picproba.gauss.Gauss.nb_helper.gauss_nb import _grad_g as __grad_g
# from picproba.gauss.Gauss.nb_helper.gauss_nb import _grad_kl as __grad_kl
# from picproba.gauss.Gauss.nb_helper.gauss_nb import _grad_right_kl as __grad_right_kl
# from picproba.gauss.Gauss.nb_helper.gauss_nb import _kl as __kl
# from picproba.gauss.Gauss.nb_helper.gauss_nb import _T_to_param as __T_to_param  # pylint: disable=E0401
# from picproba.gauss.Gauss.nb_helper.gauss_nb import make_cov as __make_cov


# def _T_to_param(
#     t_val: np.ndarray, sample_size: int, good_indexes: np.ndarray
# ) -> np.ndarray:
#     """Wrapper around AOT compiled through numba T_to_param conversion helper"""
#     if (
#         (not isinstance(t_val, np.ndarray))
#         or not (t_val.dtype == float)
#         or not (t_val.ndim == 1)
#         or not isinstance(sample_size, int)
#         or not isinstance(good_indexes, np.ndarray)
#         or not (good_indexes.dtype == int)
#         or not (good_indexes.ndim == 1)
#     ):
#         raise TypeError("Not happy with type")
#     return __T_to_param(t_val, sample_size, good_indexes)


# def _g(t_par: np.ndarray, sample_size: int, good_indexes: np.ndarray) -> float:
#     if (
#         not isinstance(t_par, np.ndarray)
#         or not (t_par.dtype == float)
#         or not (t_par.ndim == 1)
#     ):
#         raise TypeError("Expected t_par format to be a 1D np.ndarray of float dtype")
#     if not isinstance(sample_size, int):
#         raise TypeError("Expected sample_size to be int")
#     if (
#         not isinstance(good_indexes, np.ndarray)
#         or not good_indexes.dtype == int
#         or not good_indexes.ndim == 1
#     ):
#         raise TypeError("Expected good_indexes format to be 1D np.ndarray of int dtype")
#     return __g(t_par, sample_size, good_indexes)

#     _grad_g,
#     make_cov,
#     _kl,
#     _grad_kl,
#     _grad_right_kl,


# def _grad_g(
#     t_par: np.ndarray, sample_size: int, good_indexes: np.ndarray
# ) -> np.ndarray:
#     if (
#         not isinstance(t_par, np.ndarray)
#         or not (t_par.dtype == float)
#         or not (t_par.ndim == 1)
#     ):
#         raise TypeError("Expected t_par format to be a 1D np.ndarray of float dtype")
#     if not isinstance(sample_size, int):
#         raise TypeError("Expected sample_size to be int")
#     if (
#         not isinstance(good_indexes, np.ndarray)
#         or not good_indexes.dtype == int
#         or not good_indexes.ndim == 1
#     ):
#         raise TypeError("Expected good_indexes format to be 1D np.ndarray of int dtype")
#     return __grad_g(t_par, sample_size, good_indexes)


# def make_cov(pre_cov: np.ndarray) -> np.ndarray:
#     """Make covariance matrix from pre_cov array"""
#     if (
#         not isinstance(pre_cov, np.ndarray)
#         or not (pre_cov.dtype == float)
#         or not (pre_cov.ndim == 2)
#     ):
#         raise TypeError("Expected pre_cov format to be a 2D np.ndarray of float dtype")
#     return __make_cov(pre_cov)


# def _kl(par1: np.ndarray, par0: np.ndarray, dim: int):
#     if (
#         not isinstance(par1, np.ndarray)
#         or not (par1.dtype == float)
#         or not (par1.ndim == 2)
#     ):
#         raise TypeError("Expected par1 format to be a 2D np.ndarray of float dtype")
#     if (
#         not isinstance(par0, np.ndarray)
#         or not (par0.dtype == float)
#         or not (par0.ndim == 2)
#     ):
#         raise TypeError("Expected par0 format to be a 2D np.ndarray of float dtype")
#     if not isinstance(dim, int):
#         raise TypeError("Excepted dim to be an int")
#     return __kl(par1, par0, dim)


# def _grad_kl(
#     param_0: np.ndarray,
#     means_0: np.ndarray,
#     inv_cov_0: np.ndarray,
#     dim: int,
#     param_1: np.ndarray,
# ):
#     """
#     Approximates the gradient of the Kullback Leibler divergence between two distributions
#     defined by their distribution parameters, with respect to the first distribution
#     (nabla_{param_1} KL(param_1, param_0))

#     Args:
#         param_1, param_0 are 2 distribution parameters
#         n_sample is disregarded (exact computations used instead)

#     Output:
#         nabla_{param_1}KL(param_1, param_0)
#     """
#     if (
#         not isinstance(param_0, np.ndarray)
#         or not (param_0.dtype == float)
#         or not (param_0.ndim == 2)
#     ):
#         raise TypeError("Expected param_0 format to be a 2D np.ndarray of float dtype")
#     if (
#         not isinstance(param_1, np.ndarray)
#         or not (param_1.dtype == float)
#         or not (param_1.ndim == 2)
#     ):
#         raise TypeError("Expected param_1 format to be a 2D np.ndarray of float dtype")

#     if (
#         not isinstance(means_0, np.ndarray)
#         or not (means_0.dtype == float)
#         or not (means_0.ndim == 1)
#     ):
#         raise TypeError("Expected means_0 format to be a 1D np.ndarray of float dtype")

#     if (
#         not isinstance(inv_cov_0, np.ndarray)
#         or not (inv_cov_0.dtype == float)
#         or not (inv_cov_0.ndim == 2)
#     ):
#         raise TypeError(
#             "Expected inv_cov_0 format to be a 2D np.ndarray of float dtype"
#         )

#     if not isinstance(dim, int):
#         raise TypeError("Expected dim to be an integer")

#     return __grad_kl(
#         param_0,
#         means_0,
#         inv_cov_0,
#         dim,
#         param_1,
#     )


# def _grad_right_kl(
#     param_1: np.ndarray,
#     means_1: np.ndarray,
#     cov_1: np.ndarray,
#     dim: int,
#     param_0: np.ndarray,
# ):
#     if (
#         not isinstance(param_0, np.ndarray)
#         or not (param_0.dtype == float)
#         or not (param_0.ndim == 2)
#     ):
#         raise TypeError("Expected param_0 format to be a 2D np.ndarray of float dtype")
#     if (
#         not isinstance(param_1, np.ndarray)
#         or not (param_1.dtype == float)
#         or not (param_1.ndim == 2)
#     ):
#         raise TypeError("Expected param_1 format to be a 2D np.ndarray of float dtype")

#     if (
#         not isinstance(means_1, np.ndarray)
#         or not (means_1.dtype == float)
#         or not (means_1.ndim == 1)
#     ):
#         raise TypeError("Expected means_1 format to be a 1D np.ndarray of float dtype")

#     if (
#         not isinstance(cov_1, np.ndarray)
#         or not (cov_1.dtype == float)
#         or not (cov_1.ndim == 2)
#     ):
#         raise TypeError("Expected cov_1 format to be a 2D np.ndarray of float dtype")

#     if not isinstance(dim, int):
#         raise TypeError("Expected dim to be an integer")

#     return __grad_right_kl(param_1, means_1, cov_1, dim, param_0)
