from typing import Callable, Optional, Union, overload

import numpy as np
from apicutils import get_pre_shape, par_eval, prod
from picproba.errors import MethodNotSupported
from picproba.proba import Proba
from picproba.types import SamplePoint, Samples


class DiscreteProbaInt(Proba):
    """Discrete Probability on integer space."""
    def __init__(self, proba):
        self.proba = np.asarray(proba)
        assert np.isclose(self.proba.sum(), 1.0) 
        assert (self.proba >= 0.0).all()
        self.card = len(proba)
        self.int_to_proba = dict(enumerate(proba))

        def gen(n):
            return np.random.choice(np.arange(self.card), n, p=self.proba)

        def log_dens(xs):
            return np.log(self.proba[xs])

        super().__init__(gen, log_dens, sample_shape=(), np_out=True)

    def dens(self, samples:Samples):
        """
        Compute the density of the distribution at points xs.

        Args:
            samples, a list of samples where the density is to be evaluated.

        Remark:
            The density of the distribution depends on the reference distribution used
            when defining the log_dens function.
        """
        return self.proba(samples)
    
    @overload
    def integrate(
        self,
        fun: Callable[[SamplePoint], float],
        n_sample: int,
        vectorized: bool,
        parallel: bool,
        **kwargs,
    ) -> float:
        ...

    @overload
    def integrate(
        self,
        fun: Callable[[SamplePoint], np.ndarray],
        n_sample: int,
        vectorized: bool,
        parallel: bool,
        **kwargs,
    ) -> np.ndarray:
        ...

    def integrate(
        self,
        fun: Union[Callable[[SamplePoint], float], Callable[[SamplePoint], np.ndarray]],
        n_sample: int = 100,
        vectorized: bool = False,
        parallel: bool = False,
        **kwargs,
    ) -> Union[float, np.ndarray]:
        r"""
        Estimate the expected value $E[fun(x)]$ using i.i.d. samples.

        Args:
            fun: a function of a sample outputing array like results. The function can take other
                keywords arguments
            n_sample: disregarded
            vectorized: boolean, specify if the function is vectorized (i.e. accept multiple
                samples). Default is False. If True, parallel is disregarded.
            parallel: boolean, specify if function evaluations should be parallelized
        **kwargs are passed to func
        """
        samples = np.arange(self.card)
        if vectorized:
            vals = fun(samples, **kwargs)
        else:
            vals = np.array(
                par_eval(fun=fun, xs=samples, parallel=parallel, **kwargs)
            )
        return np.tensordot(vals, self.proba, (0,0))

    def contract(self, alpha: float):
        raise MethodNotSupported("'contract' method is not supported for DiscreteProbaInt")

    def shift(self, shift: SamplePoint):
        raise MethodNotSupported("'shift' method is not supported for DiscreteProbaInt")

    def lin_transform(self, mat: np.ndarray, shift: Union[float, SamplePoint] = 0):
        raise MethodNotSupported("'shift' method is not supported for DiscreteProbaInt")

    def transform(
        self,
        transform: Callable[[Samples], Samples],
        inv_transform: Callable[[Samples], Samples],
        der_transform: Optional[Callable[[Samples], np.ndarray]] = None,
    ):
        raise MethodNotSupported("'tranform' method is not supported in DiscreteProbaInt")

class DiscreteProbaArr(Proba):
    """Discrete probability distribution on arrays."""

    TOL = 1e-8

    @classmethod
    def unique_fields(cls, fields):

        n_dim_fields = len(fields.shape[1:])
        diff_matrix = ((fields[:, np.newaxis] - fields) **2).sum(tuple(range(2, 2 + n_dim_fields)))
        assert (diff_matrix <= cls.TOL).sum() == len(fields)
        

    def __init__(self, fields, proba):
        assert len(fields) == len(proba)
        self.unique_fields(fields)
        self.fields = np.asarray(fields)
        self.cardinal = len(fields)
        self._inner_mechanism = DiscreteProbaInt(proba)

        self._sample_shape = self.fields.shape[1:]
        self._n_dim = len(self._sample_shape)
        self.flat_fields = self.fields.reshape((self.cardinal, prod(self._sample_shape)))

        def gen(n):
            return self.fields[self._inner_mechanism(n)]
        
        def log_dens(xs):

            return self._inner_mechanism.log_dens(self.match(xs))
        
        super().__init__(gen, log_dens, sample_shape = self._sample_shape, np_out=True)

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

    @overload
    def integrate(
        self,
        fun: Callable[[SamplePoint], float],
        n_sample: int,
        vectorized: bool,
        parallel: bool,
        **kwargs,
    ) -> float:
        ...

    @overload
    def integrate(
        self,
        fun: Callable[[SamplePoint], np.ndarray],
        n_sample: int,
        vectorized: bool,
        parallel: bool,
        **kwargs,
    ) -> np.ndarray:
        ...

    def integrate(
        self,
        fun: Union[Callable[[SamplePoint], float], Callable[[SamplePoint], np.ndarray]],
        n_sample: int = 100,
        vectorized: bool = False,
        parallel: bool = False,
        **kwargs,
    ) -> Union[float, np.ndarray]:
        r"""
        Estimate the expected value $E[fun(x)]$ using i.i.d. samples.

        Args:
            fun: a function of a sample outputing array like results. The function can take other
                keywords arguments
            n_sample: disregarded
            vectorized: boolean, specify if the function is vectorized (i.e. accept multiple
                samples). Default is False. If True, parallel is disregarded.
            parallel: boolean, specify if function evaluations should be parallelized
        **kwargs are passed to func
        """
        samples = self.fields
        if vectorized:
            vals = fun(samples, **kwargs)
        else:
            vals = np.array(
                par_eval(fun=fun, xs=samples, parallel=parallel, **kwargs)
            )
        return np.tensordot(vals, self._inner_mechanism.proba, (0,0))


    def contract(self, alpha: float):
        return DiscreteProbaArr(self.fields * alpha, self._inner_mechanism.proba)

    def shift(self, shift: SamplePoint):
        return DiscreteProbaArr(self.fields + shift, self._inner_mechanism.proba)

    def lin_transform(self, mat: np.ndarray, shift: Union[float, SamplePoint] = 0):
        return DiscreteProbaArr(self.fields @mat.T + shift, self._inner_mechanism.proba)

    def transform(
        self,
        transform: Callable[[Samples], Samples],
        inv_transform: Callable[[Samples], Samples],
        der_transform: Optional[Callable[[Samples], np.ndarray]] = None,
    ):
        transformed_fields = transform(self.fields)
        self.unique_fields(transformed_fields)
        return DiscreteProbaArr(transformed_fields, proba = self._inner_mechanism.proba)

    @property
    def proba(self):
        return self._inner_mechanism.proba
