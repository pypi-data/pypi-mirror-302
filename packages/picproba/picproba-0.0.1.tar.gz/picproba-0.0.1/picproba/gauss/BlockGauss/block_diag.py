from typing import Optional, Sequence

import numpy as np
from picproba.gauss.BlockGauss.helper import check_blocks
from picproba.gauss.Gauss import Gaussian


def check_coherence(
    means: Sequence[np.ndarray], covs: Sequence[np.ndarray], blocks: list[list[int]]
):
    """Check if shapes of means, covariance, blocks are coherent"""
    for mu, cov, block in zip(means, covs, blocks):
        d = len(mu)
        assert cov.shape == (d, d)
        assert len(block) == d


def inv_permut(permut):
    """Fast invert a permutation
    (code from https://stackoverflow.com/questions/9185768/inverting-permutations-in-python)
    """
    inv = np.empty_like(permut)
    inv[permut] = np.arange(len(inv), dtype=inv.dtype)
    return inv


class BlockDiagGauss(Gaussian):
    """Gaussian distribution with Block Diagonal covariance matrix"""

    def __init__(
        self,
        means: Sequence[np.ndarray],
        covs: Sequence[np.ndarray],
        blocks: Optional[list[list[int]]] = None,
        check: bool = True,
    ):
        # Get lens of blocks, infer cuts in concatenated mean
        lens = [0] + [len(mu) for mu in means]
        cuts = np.cumsum(lens)  # type: ignore

        # Optional checks (these are disactivated when
        # the BlockDiagGauss is constructed by a secure
        # process)
        if check:
            check_blocks(blocks)
            check_coherence(means, covs, blocks)

        # Prepare accu for cov/eigvals/eigvect
        d_tot = cuts[-1]
        cov_tot = np.zeros((d_tot, d_tot))
        inv_covs = [np.linalg.inv(cov) for cov in covs]
        vects, vals = np.zeros((d_tot, d_tot)), np.zeros(d_tot)

        # Write means
        means_tot = np.concatenate(means)

        # Write cov/eigvals/eigvect
        for a, b, cov in zip(cuts, cuts[1:], covs):
            cov_tot[a:b, a:b] = cov
            loc_vals, loc_vects = np.linalg.eigh(cov)
            vects[a:b, a:b] = loc_vects
            vals[a:b] = loc_vals

        # Sort vals/vects
        sorter = np.argsort(vals)
        vals = vals[sorter]
        vects = vects[:, sorter]

        # If blocks are provided, rearrange
        if blocks is None:
            blocks = [list(range(a, b)) for a, b in zip(cuts, cuts[1:])]
        else:
            order = inv_permut([i for block in blocks for i in block])

            cov_tot = cov_tot[order][:, order]
            vects = vects[order]
            means_tot = means_tot[order]

        # Inherit form Gaussian
        super().__init__(
            means=means_tot,
            cov=cov_tot,
            info={"vals": vals, "vects": vects},
            sample_shape=(d_tot,),
        )

        # Store extra info
        self.list_means = means
        self.list_covs = covs
        self.blocks = blocks
        self.list_inv_covs = inv_covs
