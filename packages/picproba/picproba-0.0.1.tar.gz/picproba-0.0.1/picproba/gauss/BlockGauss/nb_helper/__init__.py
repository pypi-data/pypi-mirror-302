import numpy as np

from picproba.gauss.BlockGauss.nb_helper.aot import (
    _block_kl,
    _par_to_mu_M,
    _pre_grad_g,
    _quadra_to_param,
    _T_to_quadra_loc,
    loc_param_to_T,
)

# from picproba.gauss.BlockGauss.nb_helper.nb_funcs import _block_kl as __block_kl
# from picproba.gauss.BlockGauss.nb_helper.nb_funcs import _par_to_mu_M as __par_to_mu_M
# from picproba.gauss.BlockGauss.nb_helper.nb_funcs import _pre_grad_g as __pre_grad_g
# from picproba.gauss.BlockGauss.nb_helper.nb_funcs import _quadra_to_param as __quadra_to_param
# from picproba.gauss.BlockGauss.nb_helper.nb_funcs import (
#     _T_to_quadra_loc as __T_to_quadra_loc,  # pylint: disable=E0401
# )
# from picproba.gauss.BlockGauss.nb_helper.nb_funcs import loc_param_to_T as __loc_param_to_T


# def _T_to_quadra_loc(t_val_loc: np.ndarray, sample_size: int, good_index: np.ndarray):
#     return __T_to_quadra_loc(t_val_loc, sample_size, good_index)


# def loc_param_to_T(
#     loc_param: np.ndarray, good_index: list[int], sample_size: int, t_dim: int
# ):
#     return __loc_param_to_T(loc_param, good_index, sample_size, t_dim)


# def _quadra_to_param(center, H, sample_size):
#     return __quadra_to_param(center, H, sample_size)


# def _par_to_mu_M(loc_par: np.ndarray, good_index: np.ndarray, sample_size: int):
#     """Compute mu = Cov^{-1} mean and M = Cov^{-1} from parameter"""
#     return __par_to_mu_M(loc_par, good_index, sample_size)


# def _pre_grad_g(loc_par: np.ndarray, good_index: np.ndarray, sample_size: int):
#     return __pre_grad_g(loc_par, good_index, sample_size)


# def _block_kl(param_1: np.ndarray, param_0: np.ndarray, ds: int, cuts: np.ndarray):
#     """
#     Computes the Kullback Leibler divergence between two Block diagonal
#     gaussian distributions defined by their meta parameters.

#     Args:
#         proba_1, proba_0 are 2 meta parameters
#         dim: number of dimensions

#     Output:
#         kl(proba_1, proba_0)
#     """
#     return __block_kl(param_1, param_0, ds, cuts)
