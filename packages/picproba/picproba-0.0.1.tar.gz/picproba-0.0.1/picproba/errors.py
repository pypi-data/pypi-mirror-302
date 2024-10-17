"""
Exceptions for probability module
"""

class IncoherentInputs(Exception):
    """Exception when multiple input arguments are incompatible"""

class RenormError(Exception):
    """Exception when trying to compute Gaussian distribution from unnormalisable quadratic form"""


class NegativeKL(Exception):
    """Exception when KL computation yields negative value"""

class MethodNotSupported(Exception):
    """Exception when trying to access a method in a subclass which is no longer supported"""
