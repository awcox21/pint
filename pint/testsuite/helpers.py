# -*- coding: utf-8 -*-

import doctest
from distutils.version import StrictVersion
import re
import unittest

from ..compat import HAS_NUMPY, HAS_BABEL, HAS_UNCERTAINTIES, NUMPY_VER


def requires_numpy18():
    if not HAS_NUMPY:
        return unittest.skip('Requires NumPy')
    return unittest.skipUnless(StrictVersion(NUMPY_VER) >= StrictVersion('1.8'), 'Requires NumPy >= 1.8')


def requires_numpy_previous_than(version):
    if not HAS_NUMPY:
        return unittest.skip('Requires NumPy')
    return unittest.skipUnless(StrictVersion(NUMPY_VER) < StrictVersion(version), 'Requires NumPy < %s' % version)


def requires_numpy():
    return unittest.skipUnless(HAS_NUMPY, 'Requires NumPy')


def requires_not_numpy():
    return unittest.skipIf(HAS_NUMPY, 'Requires NumPy is not installed.')


def requires_babel():
    return unittest.skipUnless(HAS_BABEL, 'Requires Babel with units support')


def requires_uncertainties():
    return unittest.skipUnless(HAS_UNCERTAINTIES, 'Requires Uncertainties')


def requires_not_uncertainties():
    return unittest.skipIf(HAS_UNCERTAINTIES, 'Requires Uncertainties is not installed.')


_number_re = r'([-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?)'
_q_re = re.compile(r'<Quantity\(' + r'\s*' + r'(?P<magnitude>%s)' % _number_re +
                   r'\s*,\s*' + r"'(?P<unit>.*)'" + r'\s*' + r'\)>')

_sq_re = re.compile(r'\s*' + r'(?P<magnitude>%s)' % _number_re +
                    r'\s' + r"(?P<unit>.*)")

_unit_re = re.compile(r'<Unit\((.*)\)>')


class PintOutputChecker(doctest.OutputChecker):

    def check_output(self, want, got, optionflags):
        check = super().check_output(want, got, optionflags)
        if check:
            return check

        try:
            if eval(want) == eval(got):
                return True
        except:
            pass

        for regex in (_q_re, _sq_re):
            try:
                parsed_got = regex.match(got.replace(r'\\', '')).groupdict()
                parsed_want = regex.match(want.replace(r'\\', '')).groupdict()

                v1 = float(parsed_got['magnitude'])
                v2 = float(parsed_want['magnitude'])

                if abs(v1 - v2) > abs(v1) / 1000:
                    return False

                if parsed_got['unit'] != parsed_want['unit']:
                    return False

                return True
            except:
                pass

        cnt = 0
        for regex in (_unit_re, ):
            try:
                parsed_got, tmp = regex.subn('\1', got)
                cnt += tmp
                parsed_want, temp = regex.subn('\1', want)
                cnt += tmp

                if parsed_got == parsed_want:
                    return True

            except:
                pass

        if cnt:
            # If there was any replacement, we try again the previous methods.
            return self.check_output(parsed_want, parsed_got, optionflags)

        return False

