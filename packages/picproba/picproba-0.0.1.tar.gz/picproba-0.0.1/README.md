This package provides classes for Probability distributions and parametric families of probability distributions, with a particular focus on log density and Kullback--Leibler divergence and their derivative (for families of probability distributions).

Overview of Proba class:
The Proba class is the abstraction for a Probability distribution. A Proba instance can:
- draw samples ('gen' and '__call__' methods)
- compute the density of samples ('dens' and 'log_dens' methods)
- approximate the Kullback Leibler divergence with another distribution
on the same space
- approximate the f-divergence with another distribution on the same space
- approximate the integral of any real or vector valued function
- be transformed into another distribution g(X) if g is bijective and smooth (with special implementation if g is affine or linear)

Moreover, Proba instances can be tensorized with one another. Mixtures can be defined as well. Partial support is given to independant addition (the log_dens of the instance is approximated).

Overview of ProbaMap class
The ProbaMap class is the abstraction for a parametric family of Probability distribution. A ProbaMap instance can:
- map a parameter (ProbaParam) to a Proba instance ('prob_map' and '__call__' method)
- Compute the derivative of the log density map (log-likelihood) with respect to the ProbaParam
- Approximate the Kullback-Leibler divergence, and the left and right derivative of the Kullback-Leibler divergence between two ProbaParam. Closed form expressions are used whenever possible in implemented subclass of ProbaMap.
- Approximate the f divergence, and the left and right derivative of the f divergence between two ProbaParam. 
- Approximate the derivative of an integral with respect to ProbaParam
- Be transformed into another ProbaMap (map \theta -> X_\theta can be transformed to map \theta -> g(\theta) if g is bijective and smooth). Special care is taken to preserve potential reimplementations of Kullbakc-Leibler related computations (e.g. the available closed-form for Gaussians).

Multiple ProbaMap instances can also be tensorized.

Important subclasses of ProbaMap are ExponentialFamily and PreExponentialFamily. For ExponentialFamily, exact formulas are used for Kullback-Leibler divergence and its derivatives. PreExponentialFamily are exponential family not necessarily using the natural parametrization. Gaussian maps are coded as a subclass of PreExponentialFamily, with exact KL computations. Transforms of these maps automatically preserve exact KL computations.

The package was written while the author conducted his PhD at Universite de Lille, with financial support from SUEZ.