from typing import Callable, Optional, Sequence, Tuple, Union

import numpy as np
from apicutils import get_pre_shape, par_eval, prod
from picproba.discrete.discrete import DiscreteProbaArr, DiscreteProbaInt
from picproba.errors import MethodNotSupported
from picproba.exponential_family.exponential_family import ExponentialFamily
from picproba.proba_map import ProbaMap
from picproba.types import ProbaParam, SamplePoint, Samples


class DiscreteProbaIntMap(ProbaMap):
    """Discrete probability map for distributions outputting int.
    Functions and methods defined in this class will be used for
    other Discrete probability map on other form of outputs
    """
    def __init__(self, card:int):
        self.card = card
        def prob_map(x:ProbaParam):
            proba = self.infer_proba(x)
            return DiscreteProbaInt(proba)
        
        def log_dens_der(x:ProbaParam):
            _x = np.asarray(x)
            self.check_param(_x)
            inv_x = 1 / _x
            inv_rest = 1 / (1 - _x.sum())
            def fun(ys:Samples):
                accu = np.zeros(ys.shape +(self.card-1,))
                for i in range(self.card -1):
                    accu[ys==i, i] = inv_x[i]
                accu[ys == (self.card-1)] = -inv_rest
                return accu
            return fun

        ref_param = np.full(card-1, 1/card)
        proba_param_shape = (card-1)
        sample_shape = ()
        super().__init__(prob_map=prob_map, log_dens_der=log_dens_der, ref_param=ref_param, proba_param_shape=proba_param_shape, sample_shape=sample_shape)

    def infer_proba(self, param:ProbaParam):
        """Infer proba from a ProbaParam"""
        proba = np.zeros(self.card)
        proba[:-1] = param
        proba[-1] = 1 - proba[:-1].sum()

        return proba
    
    def check_param(self, param:ProbaParam)->None:
        _param = np.asarray(param)
        assert (_param >= 0.0).all()
        assert _param.sum() <= 1.0
        return None

    def kl(
        self,
        param_1: ProbaParam,
        param_0: ProbaParam,
        n_sample: int = 1000,
    ) -> float:
        """Kullback Leibler divergence between two distributions
        defined by their prior parameters.

        Args:
            param_1, param_0 are 2 prior parameters
            n_sample specifies how many points are used to estimate Kullback

        Output:
            kl(param_1, param_0)

        Note:
            For a ProbaMap object obtained as the result of .reparametrize method with
            inherit_method=True, this method might be hidden behind a function attribute which
            is more efficient.
        """
        self.check_param(param_1)
        self.check_param(param_0)
        y1, y0 = self.infer_proba(param_1), self.infer_proba(param_0)
        return (np.log(y1/ y0) * y1).sum()
    
    def grad_kl(  # pylint: disable=E0202
        self, param_0: ProbaParam
    ) -> Callable[[ProbaParam, int], tuple[ProbaParam, float]]:
        """
        Approximates the gradient of the Kullback Leibler divergence between two distributions
        defined by their distribution parameters, with respect to the first distribution
        (nabla_{proba_1} kl(proba_1, proba_0))

        Args:
            param_0, a distribution parameter

        Output:
            A closure taking as arguments:
                param_1, a distribution parameter
                n_sample, an integer
            outputing a tuple with first element
                nabla_{param_1}kl(param_1, param_0) approximated using a sample
                    phi_i of predictors generated through proba_1.gen (typically i.i.d.).
                kl(param_1, param_0) approximated using the same sample of predictors

        This method should be rewritten for families with closed form expressions of KL and
        KL gradient. The closure form is used to simplify caching computations related to param_0
        (for instance inverse of covariance matrix for gaussian distributions).

        Note:
            For a ProbaMap object obtained as the result of .reparametrize method with
            inherit_method=True, this method might be hidden behind a function attribute which
            is more efficient.
        """
        _param_0 = np.asarray(param_0)
        self.check_param(_param_0)
        mass_0 = 1 - _param_0.sum()

        def fun(param_1:ProbaParam, n_sample:int=100) -> tuple[ProbaParam, float]:
            _param_1 = np.asarray(param_1)
            self.check_param(_param_1)
            mass_1 = 1 - _param_1.sum()

            log_ratio_par = np.log(_param_1/_param_0)
            log_ratio_mass = np.log(mass_1/mass_0)
            kl = (log_ratio_par * _param_1).sum() + log_ratio_mass * mass_1
            return np.log(_param_1/_param_0) - np.log(mass_1/mass_0), kl

        return fun

    def grad_right_kl(  # pylint: disable=E0202
        self, param_1: ProbaParam
    ) -> Callable[[ProbaParam, int], tuple[ProbaParam, float]]:
        """
        Compute the derivative of the Kullback--Leibler divergence with respect to the second
        distribution parameter
        """
        _param_1 = np.asarray(param_1)
        self.check_param(_param_1)
        mass_1 = 1 - _param_1.sum()


        def fun(param_0:ProbaParam, n_sample:int=100) -> tuple[ProbaParam, float]:
            _param_0 = np.asarray(param_0)
            self.check_param(_param_0)
            mass_0 = 1 - _param_0.sum()

            kl = (np.log(_param_1/_param_0) * _param_1).sum() + np.log(mass_1/mass_0) * mass_1
            grad_kl = - _param_1 /_param_0 + mass_1/ mass_0
            return grad_kl, kl

        return fun

    def f_div(  # pylint: disable=E0202
        self,
        param_1: ProbaParam,
        param_0: ProbaParam,
        f: Callable[[Sequence[float]], Sequence[float]],
        n_sample: int = 1000,
    ) -> float:
        r"""f-divergence between two distributions
        defined by their prior parameters.

        Args:
            param_1, param_0 are 2 prior parameters
            f, a convex function such that $f(1) = 0$ (No checks are performed).
            n_sample, number of points used to estimate the f-divergence (disregarded)

        Output:
            $D_f(proba_1, proba_0)$ (exact)

        Note:
            For a ProbaMap object obtained as the result of .reparametrize method with
            inherit_method=True, this method might be hidden behind a function attribute which
            is more efficient.
        """
        self.check_param(param_0)
        self.check_param(param_1)
        proba_1, proba_0 = self.infer_proba(param_1), self.infer_proba(param_0)
        return (np.asarray(f(proba_1/proba_0)) * proba_0).sum()

    def grad_f_div(  # pylint: disable=E0202
        self,
        param_0: ProbaParam,
        f: Callable[[float], float],
        f_der: Callable[[float], float],
    ) -> Callable[[ProbaParam, int], tuple[ProbaParam, float]]:
        r"""Approximates the gradient of the f-divergence between two distributions
        defined by their prior parameters, with respect to the first distribution.

        Args:
            param_0, the parameter describing the second distribution.
            f, a convex function such that $f(1) = 0$ (No checks are performed).
                Should be vectorized
            f_der, the derivative of f. Should be vectorized
        """
        _param_0 = np.asarray(param_0)
        self.check_param(_param_0)
        proba_0 = self.infer_proba(_param_0)

        def gradient_function(param_1:ProbaParam, n_sample:int = 1000) -> tuple[ProbaParam, float]:
            _param_1 = np.asarray(param_1)
            self.check_param(_param_1)
            proba_1 = self.infer_proba(_param_1)

            ratio_prob = proba_1 / proba_0
            f_s = np.asarray(f(ratio_prob))
            f_der_s = np.asarray(f_der(ratio_prob))
            return f_der_s[:-1]  - f_der_s[-1], (f_s * proba_0).sum()

        return gradient_function

    def grad_right_f_div(  # pylint: disable=E0202
        self,
        param_1: ProbaParam,
        f: Callable[[float], float],
        f_der: Callable[[float], float],
    ) -> Callable[[ProbaParam, int], tuple[ProbaParam, float]]:
        r"""Gradient of the f-divergence between two distributions
        defined by their prior parameters, with respect to the second distribution.

        Args:
            param_1, the parameter describing the first distribution.
            f, a convex function such that $f(1) = 0$ (No checks are performed).
            f_der, the derivative of f
        """
        _param_1 = np.asarray(param_1)
        self.check_param(_param_1)
        proba_1 = self.infer_proba(_param_1)
        def gradient_function(param_0:ProbaParam, n_sample:int = 1000) -> tuple[ProbaParam, float]:
            _param_0 = np.asarray(param_0)
            self.check_param(_param_0)
            proba_0 = self.infer_proba(_param_0)

            ratio_prob = proba_1 / proba_0
            f_s = np.asarray(f(ratio_prob))
            f_der_s = np.asarray(f_der(ratio_prob))
            return f_s[:-1] - f_s[-1] - ratio_prob[:-1] * f_der_s[:-1] + ratio_prob[-1] * f_der_s[-1], (f_s * proba_0).sum()
        return gradient_function

    def integrate_der(  # pylint: disable=R0913
        self,
        fun: Callable[[SamplePoint], Union[np.ndarray, float]],
        param: ProbaParam,
        n_sample: int = 1000,
        vectorized: bool = False,
        parallel: bool = False,
    ) -> Tuple[np.ndarray, Union[np.ndarray, float]]:
        r"""
        Compute the derivative of:
        F(alpha) -> \int f(x) exp(log_p(alpha, x)) dmu(x) / \int exp(log_p(alpha, x)) dmu(x)
        """
        samples = np.arange(self.card)
        param = np.asarray(param)
        self.check_param(param)
        proba = self.infer_proba(param)
        if vectorized:
            evals = np.asarray(fun(samples))
        else:
            evals = np.array(
                par_eval(fun, samples, parallel=parallel)
            )  # shape (n, out_shape)

        mean_eval = (evals * proba).sum()

        der = evals[:-1] - evals[-1]

        return der, mean_eval

    def transform(
        self,
        transform: Callable[[Samples], Samples],
        inv_transform: Callable[[Samples], Samples],
        der_transform: Optional[Callable[[Samples], np.ndarray]] = None,
    ):
        raise MethodNotSupported("Method 'transform' is not supported for DiscreteProbaIntExpMap")

# Define an exponential family view of this family (note that for this parametrization
# there can not be 0 weights)
class DiscreteProbaIntExpMap(ExponentialFamily):
    """Discrete Probability on integers, as subclass of ExponentialFamily"""
    def __init__(self, n:int):
        self.card = n
        def proba_map(proba_param:ProbaParam):
            return DiscreteProbaInt(self.infer_proba(proba_param))
        def T(xs:Samples):
            xs = np.asarray(xs)
            res = np.zeros(xs.shape + (self.card -1,))
            res[xs != self.card-1, xs[xs != self.card -1]] = 1
            return res
        def g(proba_param:ProbaParam):
            return np.log(1 + np.exp(proba_param).sum())
        def der_g(proba_param:ProbaParam):
            exp_proba_param = np.exp(proba_param)
            return exp_proba_param / (1 + exp_proba_param.sum())

        def der_der_g(proba_param:ProbaParam):
            exp_proba_param = np.exp(proba_param)
            exp_pp_renorm = exp_proba_param / (exp_proba_param.sum() + 1)
            return np.diag(exp_pp_renorm) - np.outer(exp_pp_renorm, exp_pp_renorm)

        # Dummy gen function (not used)
        def gen(proba_param, n):
            return proba_map(proba_param)(n)

        super().__init__(gen=gen, T=T, g=g, der_g=der_g, der_der_g=der_der_g, der_T=None, h=None, der_h=None, proba_param_shape=(self.card-1,), sample_shape=(), ref_param = np.zeros(self.card-1))

        self._map = proba_map
        
    def infer_proba(self, x:ProbaParam)->np.ndarray:
        proba = np.zeros(self.card)
        proba[:-1] = x
        proba = np.exp(proba)
        return proba / proba.sum()
    
    def f_div(  # pylint: disable=E0202
        self,
        param_1: ProbaParam,
        param_0: ProbaParam,
        f: Callable[[Sequence[float]], Sequence[float]],
        n_sample: int = 1000,
    ) -> float:
        r"""f-divergence between two distributions
        defined by their prior parameters.

        Args:
            param_1, param_0 are 2 prior parameters
            f, a convex function such that $f(1) = 0$ (No checks are performed).
            n_sample, number of points used to estimate the f-divergence (disregarded)

        Output:
            $D_f(proba_1, proba_0)$ (exact)

        Note:
            For a ProbaMap object obtained as the result of .reparametrize method with
            inherit_method=True, this method might be hidden behind a function attribute which
            is more efficient.
        """

        proba_1, proba_0 = self.infer_proba(param_1), self.infer_proba(param_0)
        return (np.asarray(f(proba_1/proba_0)) * proba_0).sum()

    def grad_f_div(  # pylint: disable=E0202
        self,
        param_0: ProbaParam,
        f: Callable[[float], float],
        f_der: Callable[[float], float],
    ) -> Callable[[ProbaParam, int], tuple[ProbaParam, float]]:
        r"""Approximates the gradient of the f-divergence between two distributions
        defined by their prior parameters, with respect to the first distribution.

        Args:
            param_0, the parameter describing the second distribution.
            f, a convex function such that $f(1) = 0$ (No checks are performed).
                Should be vectorized
            f_der, the derivative of f. Should be vectorized
        """
        _param_0 = np.asarray(param_0)
        proba_0 = self.infer_proba(_param_0)

        def gradient_function(param_1:ProbaParam, n_sample:int = 1000) -> tuple[ProbaParam, float]:
            _param_1 = np.asarray(param_1)

            proba_1 = self.infer_proba(_param_1)

            ratio_prob = proba_1 / proba_0
            f_s = np.asarray(f(ratio_prob))
            f_der_s = np.asarray(f_der(ratio_prob))
            return proba_1[:-1] *f_der_s[:-1]  - np.outer(proba_1[:-1], proba_1) @ f_der_s, (f_s * proba_0).sum()
            # return f_der_s[:-1] * (proba_1[:-1] - proba_1[:-1] ** 2)  - f_der_s[-1] * proba_1[:-1] / (1 + np.exp(_param_1).sum()), (f_s * proba_0).sum()

        return gradient_function

    def integrate_der(  # pylint: disable=R0913
        self,
        fun: Callable[[SamplePoint], Union[np.ndarray, float]],
        param: ProbaParam,
        n_sample: int = 1000,
        vectorized: bool = False,
        parallel: bool = False,
    ) -> Tuple[np.ndarray, Union[np.ndarray, float]]:
        r"""
        Compute the derivative of:
        F(alpha) -> \int f(x) exp(log_p(alpha, x)) dmu(x) / \int exp(log_p(alpha, x)) dmu(x)
        """
        samples = np.arange(self.card)
        param = np.asarray(param)
        proba = self.infer_proba(param)
        if vectorized:
            evals = np.asarray(fun(samples))
        else:
            evals = np.array(
                par_eval(fun, samples, parallel=parallel)
            )  # shape (n, out_shape)

        mean_eval = (evals * proba).sum()

        der = evals[:-1] * proba[:-1] - np.outer(proba[:-1], proba) @ evals
        return der, mean_eval

    def transform(
        self,
        transform: Callable[[Samples], Samples],
        inv_transform: Callable[[Samples], Samples],
        der_transform: Optional[Callable[[Samples], np.ndarray]] = None,
    ):
        raise MethodNotSupported("Method 'transform' is not supported for DiscreteProbaIntExpMap")

class DiscreteProbaArrMap(ProbaMap):
    """Discrete Probability Map for distributions outputing arrays of identical shape"""

    TOL = 1e-8
    def __init__(self, fields: np.ndarray):
        self.fields = np.asarray(fields)

        def prob_map(x:ProbaParam):
            proba = self._inner_mechanism.infer_proba(x)
            return DiscreteProbaArr(self.fields, proba)
        
        def log_dens_der(x:ProbaParam):
            _x = np.asarray(x)
            self._inner_mechanism.check_param(_x)
            inv_x = 1 / _x
            inv_rest = 1 / (1 - _x.sum())
            def fun(ys:Samples):
                accu = np.zeros(ys.shape +(self._card-1,))
                for i in range(self._card -1):
                    accu[ys==i, i] = inv_x[i]
                accu[ys == (self._card-1)] = -inv_rest
                return accu
            return fun


        super().__init__(prob_map=prob_map, log_dens_der=log_dens_der, ref_param=self._ref_param, proba_param_shape=self._proba_param_shape, sample_shape=self._sample_shape)

    @property
    def fields(self):
        return self._fields

    @fields.setter
    def fields(self, values):
        self._fields = np.asarray(values)
        self.sample_shape =self._fields.shape[1:]
        self.card = len(self._fields)

    @property
    def card(self):
        return self._card

    @card.setter
    def card(self, value:int):
        self._card = value
        self._proba_param_shape = (self._card-1, )
        self._ref_param = np.full(self._card -1, 1/self._card)
        self._inner_mechanism = DiscreteProbaIntMap(self._card)

    @property
    def sample_shape(self)->tuple[int, ...]:
        return self._sample_shape

    @sample_shape.setter
    def sample_shape(self, value):
        self._sample_shape = value
        self._sample_size = prod(self._sample_shape)
        self._n_dim = len(self._sample_shape)
    
    def match(self, xs:Samples)->np.ndarray:
        """Match samples to index in fields"""
        pre_shape = get_pre_shape(xs, self._sample_shape)
        xs_flat = xs.reshape((prod(pre_shape), )+self._sample_shape)
        diff_matrix = ((xs_flat[:, np.newaxis] - self.fields) **2).sum(tuple(range(2, 2 + self._n_dim)))
        best_idxs = diff_matrix.argmin(1)
        if diff_matrix[range(len(best_idxs)), best_idxs].max() > self.TOL:
            raise ValueError("Match failed for some values")
        idxs = best_idxs.reshape(pre_shape)
        return idxs

    def kl(
        self,
        param_1: ProbaParam,
        param_0: ProbaParam,
        n_sample: int = 1000,):
        return self._inner_mechanism.kl(param_1, param_0, n_sample)
    
    def grad_kl(  # pylint: disable=E0202
        self, param_0: ProbaParam
    ) -> Callable[[ProbaParam, int], tuple[ProbaParam, float]]:
        return self._inner_mechanism.grad_kl(param_0)

    def grad_right_kl(self, param_1: ProbaParam) -> Callable[[ProbaParam, int], tuple[ProbaParam, float]]:
        return self._inner_mechanism.grad_right_kl(param_1)
    
    def f_div(self, param_1: ProbaParam, param_0: ProbaParam, f: Callable[[Sequence[float]], Sequence[float]], n_sample: int = 1000) -> float:
        return self._inner_mechanism.f_div(param_1, param_0, f, n_sample)

    def grad_f_div(self, param_0: ProbaParam, f: Callable[[float], float], f_der: Callable[[float], float]) -> Callable[[ProbaParam, int], tuple[ProbaParam, float]]:
        return self._inner_mechanism.grad_f_div(param_0, f, f_der)

    def grad_right_f_div(self, param_1: ProbaParam, f: Callable[[float], float], f_der: Callable[[float], float]) -> Callable[[ProbaParam, int], tuple[ProbaParam, float]]:
        return self._inner_mechanism.grad_right_f_div(param_1, f, f_der)

    def integrate_der(  # pylint: disable=R0913
        self,
        fun: Callable[[SamplePoint], Union[np.ndarray, float]],
        param: ProbaParam,
        n_sample: int = 1000,
        vectorized: bool = False,
        parallel: bool = False,
    ) -> Tuple[np.ndarray, Union[np.ndarray, float]]:
        r"""
        Compute the derivative of:
        F(alpha) -> \int f(x) exp(log_p(alpha, x)) dmu(x) / \int exp(log_p(alpha, x)) dmu(x)
        """
        def comp_fun(i):
            return fun(self.fields[i])
        
        return self._inner_mechanism.integrate_der(comp_fun, param=param, n_sample=n_sample, vectorized=vectorized, parallel=parallel)

    def transform(
        self,
        transform: Callable[[Samples], Samples],
        inv_transform: Callable[[Samples], Samples],
        der_transform: Optional[Callable[[Samples], np.ndarray]] = None,
    ):
        r"""
        Transform the Class of probability $X_\theta \sim \mathbb{P}_{\theta}$ to the class of
            probability $transform(X_\theta)$

        Important:
            At this point, transform MUST be bijective


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
            If proba outputs samples of shape (s1, ..., sk), and transforms maps them to
            (t1, ..., tl),
            then the derivative should be shaped
                (s1, ..., sk, t1, ..., tl).
            The new distribution will output samples of shape (t1, ..., tl).

            Moreover, transform, inv_transform and der_transform are assumed to be vectorized, i.e.
            inputs of shape (n1, ..., np, s1, ..., sk) will result in outputs of shape
                (n1, ..., np, t1, ..., tl ) for transform, (n1, ..., np, s1, ..., sk, t1, ..., tl ) for
                der_transform

        Output formating:
            The format of the output depends on the behavior of transform. If transform outputs np.ndarray,
            then the resulting distribution will have np_out==True.

        Future:
            Decide whether der_transform must output np.ndarray or not. Currently, does not have to (but could be less
            efficient since reforce array creation.)
        """

        new_fields = transform(self.fields)
        return DiscreteProbaArrMap(new_fields)

class DiscreteProbaArrExpMap(ExponentialFamily):
    TOL = 1e-8
    def __init__(self, fields: np.ndarray):
        self.fields = np.asarray(fields)

        def prob_map(x:ProbaParam):
            proba = self._inner_mechanism.infer_proba(x)
            return DiscreteProbaArr(self.fields, proba)
        
        def gen(proba_param, n):
            return self.fields[self._inner_mechanism.gen(proba_param, n)]

        def T(xs):
            idxs = self.match(xs)
            return self._inner_mechanism.T(idxs)

        super().__init__(
            gen=gen, T=T, g=self._inner_mechanism.g, der_g=self._inner_mechanism.der_g, der_der_g=self._inner_mechanism._H_g, der_T=None, h=None,
            der_h=None,
            proba_param_shape=self._inner_mechanism.proba_param_shape,
            sample_shape=self._sample_shape,
            ref_param=self._inner_mechanism.ref_param,)
        self._map = prob_map


    @property
    def fields(self):
        return self._fields

    @fields.setter
    def fields(self, values):
        self._fields = np.asarray(values)
        self.sample_shape =self._fields.shape[1:]
        self.card = len(self._fields)

    @property
    def card(self):
        return self._card

    @card.setter
    def card(self, value:int):
        self._card = value
        self._proba_param_shape = (self._card-1, )
        self._ref_param = np.full(self._card -1, 1/self._card)
        self._inner_mechanism = DiscreteProbaIntExpMap(self._card)

    @property
    def sample_shape(self)->tuple[int, ...]:
        return self._sample_shape

    @sample_shape.setter
    def sample_shape(self, value):
        self._sample_shape = value
        self._sample_size = prod(self._sample_shape)
        self._n_dim = len(self._sample_shape)
    
    def match(self, xs:Samples)->np.ndarray:
        """Match samples to index in fields"""
        pre_shape = get_pre_shape(xs, self._sample_shape)
        xs_flat = xs.reshape((prod(pre_shape), )+self._sample_shape)
        diff_matrix = ((xs_flat[:, np.newaxis] - self.fields) **2).sum(tuple(range(2, 2 + self._n_dim)))
        best_idxs = diff_matrix.argmin(1)
        if diff_matrix[range(len(best_idxs)), best_idxs].max() > self.TOL:
            raise ValueError("Match failed for some values")
        idxs = best_idxs.reshape(pre_shape)
        return idxs

    def f_div(self, param_1: ProbaParam, param_0: ProbaParam, f: Callable[[Sequence[float]], Sequence[float]], n_sample: int = 1000) -> float:
        return self._inner_mechanism.f_div(param_1, param_0, f, n_sample)

    def grad_f_div(self, param_0: ProbaParam, f: Callable[[float], float], f_der: Callable[[float], float]) -> Callable[[ProbaParam, int], tuple[ProbaParam, float]]:
        return self._inner_mechanism.grad_f_div(param_0, f, f_der)

    def grad_right_f_div(self, param_1: ProbaParam, f: Callable[[float], float], f_der: Callable[[float], float]) -> Callable[[ProbaParam, int], tuple[ProbaParam, float]]:
        return self._inner_mechanism.grad_right_f_div(param_1, f, f_der)

    def integrate_der(  # pylint: disable=R0913
        self,
        fun: Callable[[SamplePoint], Union[np.ndarray, float]],
        param: ProbaParam,
        n_sample: int = 1000,
        vectorized: bool = False,
        parallel: bool = False,
    ) -> Tuple[np.ndarray, Union[np.ndarray, float]]:
        r"""
        Compute the derivative of:
        F(alpha) -> \int f(x) exp(log_p(alpha, x)) dmu(x) / \int exp(log_p(alpha, x)) dmu(x)
        """

        # Define function taking int as input
        def comp_fun(i):
            return fun(self.fields[i])
        
        return self._inner_mechanism.integrate_der(comp_fun, param=param, n_sample=n_sample, vectorized=vectorized, parallel=parallel)

    def transform(
        self,
        transform: Callable[[Samples], Samples],
        inv_transform: Callable[[Samples], Samples],
        der_transform: Optional[Callable[[Samples], np.ndarray]] = None,
    ):
        r"""
        Transform the Class of probability $X_\theta \sim \mathbb{P}_{\theta}$ to the class of
            probability $transform(X_\theta)$

        Important:
            At this point, transform MUST be bijective


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
            If proba outputs samples of shape (s1, ..., sk), and transforms maps them to
            (t1, ..., tl),
            then the derivative should be shaped
                (s1, ..., sk, t1, ..., tl).
            The new distribution will output samples of shape (t1, ..., tl).

            Moreover, transform, inv_transform and der_transform are assumed to be vectorized, i.e.
            inputs of shape (n1, ..., np, s1, ..., sk) will result in outputs of shape
                (n1, ..., np, t1, ..., tl ) for transform, (n1, ..., np, s1, ..., sk, t1, ..., tl ) for
                der_transform

        Output formating:
            The format of the output depends on the behavior of transform. If transform outputs np.ndarray,
            then the resulting distribution will have np_out==True.

        Future:
            Decide whether der_transform must output np.ndarray or not. Currently, does not have to (but could be less
            efficient since reforce array creation.)
        """

        new_fields = transform(self.fields)
        return DiscreteProbaArrExpMap(new_fields)
