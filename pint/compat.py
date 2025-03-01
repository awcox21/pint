# -*- coding: utf-8 -*-
"""
    pint.compat
    ~~~~~~~~~~~

    Compatibility layer.

    :copyright: 2013 by Pint Authors, see AUTHORS for more details.
    :license: BSD, see LICENSE for more details.
"""
import tokenize
from io import BytesIO
from numbers import Number
from decimal import Decimal


def tokenizer(input_string):
    for tokinfo in tokenize.tokenize(BytesIO(input_string.encode('utf-8')).readline):
        if tokinfo.type == tokenize.ENCODING:
            continue
        yield tokinfo


try:
    import numpy as np
    from numpy import ndarray

    HAS_NUMPY = True
    NUMPY_VER = np.__version__
    NUMERIC_TYPES = (Number, Decimal, ndarray, np.number)

    def _to_magnitude(value, force_ndarray=False):
        if isinstance(value, (dict, bool)) or value is None:
            raise TypeError('Invalid magnitude for Quantity: {0!r}'.format(value))
        elif isinstance(value, str) and value == '':
            raise ValueError('Quantity magnitude cannot be an empty string.')
        elif isinstance(value, (list, tuple)):
            return np.asarray(value)
        if force_ndarray:
            return np.asarray(value)
        return value

except ImportError:

    np = None

    class ndarray:
        pass

    HAS_NUMPY = False
    NUMPY_VER = '0'
    NUMERIC_TYPES = (Number, Decimal)

    def _to_magnitude(value, force_ndarray=False):
        if isinstance(value, (dict, bool)) or value is None:
            raise TypeError('Invalid magnitude for Quantity: {0!r}'.format(value))
        elif isinstance(value, str) and value == '':
            raise ValueError('Quantity magnitude cannot be an empty string.')
        elif isinstance(value, (list, tuple)):
            raise TypeError('lists and tuples are valid magnitudes for '
                             'Quantity only when NumPy is present.')
        return value

try:
    from uncertainties import ufloat
    HAS_UNCERTAINTIES = True
except ImportError:
    ufloat = None
    HAS_UNCERTAINTIES = False

try:
    from babel import Locale as Loc
    from babel import units as babel_units
    HAS_BABEL = hasattr(babel_units, 'format_unit')
except ImportError:
    HAS_BABEL = False

if not HAS_BABEL:
    Loc = babel_units = None
