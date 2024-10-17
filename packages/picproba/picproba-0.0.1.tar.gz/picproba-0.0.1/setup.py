from setuptools import find_packages, setup

long_description = "".join(
    [
        "Probability distributions management\n",
        "This package provides classes for Probability distributions ",
        "and parametric families of probability distributions, ",
        "with a particular focus on log density and Kullback--Leibler divergence.\n",
        "Probability distributions and family of probability distributions can be easily transformed.\n",
        "NOTE: numba requirement is currently pinned to 0.58, as other versions have not yet been fully",
        " tested. This notably impacts the version of numpy (<2). This should be fixed in future versions."
    ]
)

setup(
    name="picproba",
    version="0.0.1",
    author="Antoine Picard-Weibel",
    author_email="apicard.w@gmail.com",
    description="Probability distribution management",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[
        "apicutils>=0.0.2",
        "pandas",
        "scipy>=1.7.0",
        "numpy<=1.26",
        "numba==0.58.1",
    ],
    python_requires=">=3.9",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
