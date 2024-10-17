r"""
Class for Exponential families using a different parametrisation than the standard one

This class is designed with bayes module in view. It is basically a standard ProbaMap with
two more (functional) attributes:
- T
- T_to_param

It is assumed that the probability distributions have log_density of form T(x) . F(param) .
T_to_param is the function F^{-1}.

In the case where the probability map (and hence F) is not injective, $T_to_param$ should map to
any parameter outputing the distribution.

Used while no better solution is found.
"""

from typing import Callable, Optional

import numpy as np

from picproba.types import ProbaParam, Samples
from picproba.proba import Proba
from picproba.proba_map import ProbaMap


class PreExpFamily(ProbaMap):
    # Indicate that this is a ExponentialFamily object
    map_type = "PreExpFamily"

    def __init__(
        self,
        prob_map: Callable[[ProbaParam], Proba],
        log_dens_der: Callable[[ProbaParam], Callable[[Samples], np.ndarray]],
        T: Callable[[Samples], np.ndarray],
        param_to_T: Callable[[ProbaParam], np.ndarray],
        T_to_param: Callable[[np.ndarray], ProbaParam],
        der_T_to_param: Optional[Callable[[np.ndarray], np.ndarray]] = None,
        g: Optional[Callable[[np.ndarray], np.ndarray]] = None,
        grad_g: Optional[Callable[[np.ndarray], np.ndarray]] = None,
        ref_param: Optional[ProbaParam] = None,
        proba_param_shape: Optional[tuple[int, ...]] = None,
        sample_shape: Optional[tuple[int, ...]] = None,
        t_shape: Optional[tuple[int, ...]] = None,
    ):
        super().__init__(
            prob_map, log_dens_der, ref_param, proba_param_shape, sample_shape
        )
        self._T = T
        self._param_to_T = param_to_T
        self._T_to_param = T_to_param
        self._der_T_to_param = der_T_to_param

        self._g = g
        self._grad_g = grad_g

        if t_shape is None:
            if ref_param is not None:
                t_shape = prob_map(ref_param).sample_shape
            else:  # pylint: disable= W0702
                raise ValueError("Could not infer t_shape")
        self._t_shape = t_shape

    @property
    def t_shape(self):
        return self._t_shape

    @property
    def g(self):
        return self._g

    @property
    def grad_g(self):
        return self._grad_g

    @property
    def T(self):
        return self._T

    @property
    def param_to_T(self):
        return self._param_to_T

    @property
    def T_to_param(self):
        return self._T_to_param

    @property
    def der_T_to_param(self):
        return self._der_T_to_param

    def transform(
        self,
        transform: Callable[[Samples], Samples],
        inv_transform: Callable[[Samples], Samples],
        der_transform: Optional[Callable[[Samples], np.ndarray]] = None,
        new_sample_shape: Optional[tuple[int, ...]] = None,
    ):
        r"""
        Transform the Class of probability $X_\theta \sim \mathbb{P}_{\theta}$ to the class of probability
            $transform(X_\theta)$

        Important:
            transform MUST be bijective, else computations for log_dens_der, kl, grad_kl, grad_right_kl will fail.


        CAUTION:
            Everything possible is done to insure that the reference distribution remains
            Lebesgue IF the original reference distribution is Lebesgue. This requires access
            to the derivative of the transform (more precisely its determinant). If this can
            not be computed, then the log_density attribute will no longer be with reference to
            the standard Lebesgue measure.

            Still,
                proba_1.transform(f, inv_f).log_dens(x) - proba_2.transform(f, inv_f).log_dens(x)
            acccurately describes
                log (d proba_1 / d proba_2 (x)).

            If only ratios of density are to be investigated, der_transform can be disregarded.

            Due to this, log_dens_der, kl, grad_kl, grad_right_kl will perform satisfactorily.

        Dimension formating:
            If proba outputs samples of shape (s1, ..., sk), and transforms maps them to (t1, ..., tl)
             then the derivative should be shaped
                (s1, ..., sk, t1, ..., tl).
            The new distribution will output samples of shape (t1, ..., tl).

            Moreover, transform, inv_transform and der_transform are assumed to be vectorized, i.e.
            inputs of shape (n1, ..., np, s1, ..., sk) will result in outputs of shape
                (n1, ..., np, t1, ..., tl ) for transform, (n1, ..., np, s1, ..., sk, t1, ..., tl ) for
                der_transform

        Future:
            Decide whether der_transform must output np.ndarray or not. Currently, does not have to (but could be less
            efficient since reforce array creation.)
        """

        def new_map(x: ProbaParam) -> Proba:
            return self._map(x).transform(transform, inv_transform, der_transform)

        if new_sample_shape is None:
            if self.ref_param is None:
                raise ValueError("Could not infer new sample shape")
            new_sample_shape = new_map(self.ref_param).sample_shape

        def new_log_dens_der(
            x: ProbaParam,
        ) -> Callable[[Samples], np.ndarray]:
            log_dens_der_fun = self._log_dens_der(x)

            def new_func(samples: Samples) -> np.ndarray:
                return log_dens_der_fun(inv_transform(samples))

            return new_func

        def new_T(samples: Samples):
            return self.T(inv_transform(samples))

        return TransformedPreExpFamily(
            prob_map=new_map,
            log_dens_der=new_log_dens_der,
            T=new_T,
            param_to_T=self.param_to_T,
            T_to_param=self.T_to_param,
            der_T_to_param=self.der_T_to_param,
            g=self.g,
            grad_g=self.grad_g,
            ref_param=self.ref_param,
            proba_param_shape=self.proba_param_shape,
            sample_shape=new_sample_shape,
            t_shape=self.t_shape,
            kl=self.kl,
            grad_kl=self.grad_kl,
            grad_right_kl=self.grad_right_kl,
            f_div=self.f_div,
            grad_f_div=self.grad_f_div,
            grad_right_f_div=self.grad_right_f_div,
        )


class TransformedPreExpFamily(PreExpFamily):
    """Class for transformed PreExpFamily. Reimplementations of kl and its derivatives are preserved"""

    def __init__(
        self,
        prob_map: Callable[[ProbaParam], Proba],
        log_dens_der: Callable[[ProbaParam], Callable[[Samples], np.ndarray]],
        T: Callable[[Samples], np.ndarray],
        param_to_T: Callable[[ProbaParam], np.ndarray],
        T_to_param: Callable[[np.ndarray], ProbaParam],
        der_T_to_param: Optional[Callable[[np.ndarray], np.ndarray]] = None,
        g: Optional[Callable[[np.ndarray], np.ndarray]] = None,
        grad_g: Optional[Callable[[np.ndarray], np.ndarray]] = None,
        ref_param: Optional[ProbaParam] = None,
        proba_param_shape: Optional[tuple[int, ...]] = None,
        sample_shape: Optional[tuple[int, ...]] = None,
        t_shape: Optional[tuple[int, ...]] = None,
        kl=None,
        grad_kl=None,
        grad_right_kl=None,
        f_div=None,
        grad_f_div=None,
        grad_right_f_div=None,
    ):
        super().__init__(
            prob_map=prob_map,
            log_dens_der=log_dens_der,
            T=T,
            param_to_T=param_to_T,
            T_to_param=T_to_param,
            der_T_to_param=der_T_to_param,
            g=g,
            grad_g=grad_g,
            ref_param=ref_param,
            proba_param_shape=proba_param_shape,
            sample_shape=sample_shape,
            t_shape=t_shape,
        )

        self._kl = kl
        self._grad_kl = grad_kl
        self._grad_right_kl = grad_right_kl

        self._f_div = f_div
        self._grad_f_div = grad_f_div
        self._grad_right_f_div = grad_right_f_div

    def transform(
        self,
        transform: Callable[[Samples], Samples],
        inv_transform: Callable[[Samples], Samples],
        der_transform: Optional[Callable[[Samples], np.ndarray]] = None,
        new_sample_shape: Optional[tuple[int, ...]] = None,
    ):
        r"""
        Transform the Class of probability $X_\theta \sim \mathbb{P}_{\theta}$ to the class of probability
            $transform(X_\theta)$

        Important:
            transform MUST be bijective, else computations for log_dens_der, kl, grad_kl, grad_right_kl will fail.


        CAUTION:
            Everything possible is done to insure that the reference distribution remains
            Lebesgue IF the original reference distribution is Lebesgue. This requires access
            to the derivative of the transform (more precisely its determinant). If this can
            not be computed, then the log_density attribute will no longer be with reference to
            the standard Lebesgue measure.

            Still,
                proba_1.transform(f, inv_f).log_dens(x) - proba_2.transform(f, inv_f).log_dens(x)
            acccurately describes
                log (d proba_1 / d proba_2 (x)).

            If only ratios of density are to be investigated, der_transform can be disregarded.

            Due to this, log_dens_der, kl, grad_kl, grad_right_kl will perform satisfactorily.

        Dimension formating:
            If proba outputs samples of shape (s1, ..., sk), and transforms maps them to (t1, ..., tl)
             then the derivative should be shaped
                (s1, ..., sk, t1, ..., tl).
            The new distribution will output samples of shape (t1, ..., tl).

            Moreover, transform, inv_transform and der_transform are assumed to be vectorized, i.e.
            inputs of shape (n1, ..., np, s1, ..., sk) will result in outputs of shape
                (n1, ..., np, t1, ..., tl ) for transform, (n1, ..., np, s1, ..., sk, t1, ..., tl ) for
                der_transform

        Future:
            Decide whether der_transform must output np.ndarray or not. Currently, does not have to (but could be less
            efficient since reforce array creation.)
        """

        def new_map(x: ProbaParam) -> Proba:
            return self._map(x).transform(transform, inv_transform, der_transform)

        if new_sample_shape is None:
            if self.ref_param is None:
                raise ValueError("Could not infer new sample shape")
            new_sample_shape = new_map(self.ref_param).sample_shape

        def new_log_dens_der(
            x: ProbaParam,
        ) -> Callable[[Samples], np.ndarray]:
            log_dens_der_fun = self._log_dens_der(x)

            def new_func(samples: Samples) -> np.ndarray:
                return log_dens_der_fun(inv_transform(samples))

            return new_func

        def new_T(samples: Samples):
            return self.T(inv_transform(samples))

        return TransformedPreExpFamily(
            prob_map=new_map,
            log_dens_der=new_log_dens_der,
            T=new_T,
            param_to_T=self.param_to_T,
            T_to_param=self.T_to_param,
            der_T_to_param=self.der_T_to_param,
            g=self.g,
            grad_g=self.grad_g,
            ref_param=self.ref_param,
            proba_param_shape=self.proba_param_shape,
            sample_shape=new_sample_shape,
            t_shape=self.t_shape,
            kl=self._kl,
            grad_kl=self._grad_kl,
            grad_right_kl=self._grad_right_kl,
            f_div=self._f_div,
            grad_f_div=self._grad_f_div,
            grad_right_f_div=self._grad_right_f_div,
        )
